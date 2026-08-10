import os
import json
import re  # Add this with your other imports
import traceback
import pandas as pd
import requests
from functools import lru_cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from difflib import get_close_matches
from datetime import datetime, timedelta
from google.cloud import dialogflow_v2 as dialogflow
from google.protobuf import struct_pb2
from django.conf import settings
from .knowledge_base.agriculture import get_advice, pest_kb
import dateutil.parser


# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
    BASE_DIR, "rainfalladvisorybot-myed-9cd79fe2fcbe.json"
)
DIALOGFLOW_PROJECT_ID = "rainfalladvisorybot-myed"
LANGUAGE_CODE = "en"
DATA_DIR = os.path.join(BASE_DIR, "data")

# Caches
LOCATION_CACHE = {}
DATA_CACHE = {}

# Predefined week ranges for the current season
WEEK_RANGES = {
    1: ("2025-06-02", "2025-06-08"),
    2: ("2025-06-09", "2025-06-15"),
    3: ("2025-06-16", "2025-06-22"),
    4: ("2025-06-23", "2025-06-29")
}

@csrf_exempt
def weather_forecast(request):
    """Rainfall forecast endpoint - now prompts instead of showing data"""
    return JsonResponse({
        "response": "Please ask specifically about rainfall forecasts for your location. Example:",
        "examples": [
            "Will it rain tomorrow in Nagpur?",
            "What's the rainfall forecast for Wardha this week?",
            "When will it rain in Amravati district?"
        ]
    })


# Helper Functions
def clean_district_name(name):
    """Normalize district names with robust cleaning"""
    if not name:
        return ""
    
    # Ensure we're working with string
    name = str(name).lower().strip()
    
    # Remove special characters (keep only letters and spaces)
    name = re.sub(r'[^a-z\s]', '', name)
    
    # Common replacements and removals
    replacements = {
        r'\b(district|city|town|tehsil|rural|urban)\b': '',
        r'\s+': ' ',  # Multiple spaces to single space
        r'central|east|west|north|south': ''
    }
    
    for pattern, repl in replacements.items():
        name = re.sub(pattern, repl, name)
    
    # Specific known variations
    variations = {
        'nagpur': ['nagpur', 'nagpure'],
        'mumbai': ['mumbai', 'bombay'],
        'jaipur': ['jaipur', 'jeypore']
    }
    
    for standard, variants in variations.items():
        if name in variants:
            return standard
            
    return name.strip()

@lru_cache(maxsize=32)
def find_closest_district_match(all_districts, user_district):
    user_district = clean_district_name(user_district.lower())
    
    # Check exact match first
    if user_district in all_districts:
        return user_district
        
    # Try close matches with higher threshold
    closest = get_close_matches(user_district, all_districts, n=1, cutoff=0.7)
    
    return closest[0] if closest else None

def get_current_week():
    """Determine the current week based on predefined ranges"""
    today = datetime.now().date()
    for week, (start, end) in WEEK_RANGES.items():
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
        if start_date <= today <= end_date:
            return week
    return 4  # Default to last week

def get_week_from_date(date_str):
    """Safely determine week from date with fallback"""
    try:
        if not date_str:
            return get_current_week()  # Fallback to current week
        
        date_obj = datetime.strptime(date_str[:10], "%Y-%m-%d").date()
        for week, (start, end) in WEEK_RANGES.items():
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
            if start_date <= date_obj <= end_date:
                return week
    except ValueError as e:
        print(f"Invalid date format: {e}")
    
    return get_current_week()  # Fallback if date parsing fails

def validate_week_data(df):
    """Ensure loaded data has required columns"""
    required_columns = ["district", "advisory"]
    if df.empty or not all(col in df.columns for col in required_columns):
        return pd.DataFrame(columns=required_columns)
    return df

@lru_cache(maxsize=4)
def load_week_data(week_num):
    """Safely load week data with validation"""
    try:
        # Validate week number
        if week_num is None or week_num not in WEEK_RANGES:
            week_num = get_current_week()
            
        file_path = os.path.join(DATA_DIR, f"week{week_num}.csv")
        
        # Check if file exists
        if not os.path.exists(file_path):
            # Try to load default week if specified week doesn't exist
            default_week = get_current_week()
            if week_num != default_week:
                file_path = os.path.join(DATA_DIR, f"week{default_week}.csv")
            
        df = pd.read_csv(file_path)
        df["district"] = df["district"].str.lower().str.strip()
        return df
        
    except Exception as e:
        print(f"[ERROR] Failed to load week data: {str(e)}")
        # Return empty DataFrame with expected columns
        return pd.DataFrame(columns=["district", "rainfall_forecast", "advisory"])

def get_location_from_ip(ip):
    """Get location from IP address with caching"""
    if ip in LOCATION_CACHE:
        return LOCATION_CACHE[ip]
    
    try:
        if ip == "127.0.0.1":
            result = ("nagpur", "maharashtra")
        else:
            response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=3)
            if response.status_code == 200:
                data = response.json()
                result = (data.get("city", "").lower(), data.get("region", "").lower())
            else:
                result = (None, None)
        
        LOCATION_CACHE[ip] = result
        return result
    except:
        return (None, None)
    
# Helper Functions
@lru_cache(maxsize=1)  # Cache for 1 hour
def get_available_districts():
    """Get all unique districts from all week files"""
    districts = set()
    for week in WEEK_RANGES.keys():
        try:
            df = pd.read_csv(os.path.join(DATA_DIR, f"week{week}.csv"))
            # Ensure consistent cleaning
            df["district"] = df["district"].apply(lambda x: clean_district_name(str(x).lower()))
            districts.update(df['district'].unique())
        except Exception as e:
            print(f"⚠️ Error loading week {week} data: {str(e)}")
            continue
    
    return sorted(districts) if districts else ['nagpur', 'wardha', 'amravati']

def validate_district(requested_district):
    """Check if district exists in our data"""
    requested_district = clean_district_name(requested_district.lower())
    available_dists = get_available_districts()
    
    if requested_district in available_dists:
        return True, None
    
    # Find similar districts
    suggestions = get_close_matches(requested_district, available_dists, n=3, cutoff=0.6)
    return False, suggestions


def generate_response(intent_type, location, data, is_hindi=False, crop_type=None, date_specific=None):
    """Generate localized response based on intent"""
    lang = "hi" if is_hindi else "en"
    
    # Get localized fields
    condition = data.get(f"{lang}_crop_condition", data.get("crop_condition", "No data"))
    advisory = data.get(f"{lang}_advisory", data.get("advisory", ""))
    
    # Filter crop-specific advice
    if crop_type and advisory:
        advisory = '\n'.join([line for line in advisory.split('\n') 
                            if crop_type.lower() in line.lower()])
    
    # Date formatting
    if date_specific:
        if "today" in date_specific.lower():
            date_info = datetime.now().strftime("%b %d")
        elif "tomorrow" in date_specific.lower():
            date_info = (datetime.now() + timedelta(days=1)).strftime("%b %d")
    else:
        date_info = f"{data.get('week_start', '')} to {data.get('week_end', '')}"
    
    # Intent-specific templates
    templates = {
        "crop": {
            "hi": f"📍 {location}\n🗓️ {date_info}\n🌱 {condition}\n📅 {advisory}",
            "en": f"📍 {location}\n🗓️ {date_info}\n🌱 {condition}\n📅 {advisory}"
        },
        "sow": {
            "hi": f"📍 {location}\n🗓️ {date_info}\n🌱 बुआई सलाह:\n{advisory}",
            "en": f"📍 {location}\n🗓️ {date_info}\n🌱 Sowing Advice:\n{advisory}"
        }
    }
    
    response = templates.get(intent_type, templates["rain"])[lang]
    

import pandas as pd
from functools import lru_cache


# View Functions
def chat_page(request):
    """Render chat interface"""
    return render(request, 'chatbot/chat.html')


from functools import lru_cache
import pandas as pd
from datetime import datetime
import os
from pathlib import Path

@lru_cache(maxsize=1)
def load_daily_rainfall_data():
    """
    Load Excel with alternating actual and predicted rainfall weeks.
    Each group has date headers in row 2 (index 1), data starts from row 3.
    """
    import os
    import pandas as pd
    from pathlib import Path

    # Adjust path correctly
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir / "data" / "actualvspredictedrainfall.xlsx"
    
    # Read Excel without headers
    df_raw = pd.read_excel(file_path, header=None)

    # Get date row (index 1)
    date_row = df_raw.iloc[1]
    
    # Slice only from column C onward (index 2) — actual + predicted weeks
    date_cols = date_row[2:]  # skip A,B

    # Data starts from row 2 onwards (index 2), columns A and B are State and District
    df_data = df_raw.iloc[2:, :2].copy()  # A,B → State, District
    df_data.columns = ["State", "District"]

    # Now loop through all date columns starting from index 2
    records = []
    for col_index in range(2, len(df_raw.columns)):
        col_name = date_row[col_index]
        try:
            parsed_date = pd.to_datetime(col_name).strftime("%Y-%m-%d")
        except:
            continue  # Skip headers like "Actual Rainfall" etc.

        # Get rainfall column values
        rainfall_values = df_raw.iloc[2:, col_index].values
        districts = df_raw.iloc[2:, 1].values  # Column B → District

        for i in range(len(rainfall_values)):
            if pd.isna(rainfall_values[i]) or pd.isna(districts[i]):
                continue
            records.append({
                "date": parsed_date,
                "district": str(districts[i]).strip().lower(),
                "rainfall_mm": float(rainfall_values[i])
            })

    return pd.DataFrame(records)


def get_rainfall_from_excel(date_str, district_name, lang="en"):
    """
    Fetch rainfall amount and classify it into readable format.
    """
    try:
        df = load_daily_rainfall_data()
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

        # Clean inputs
        district_name_clean = district_name.strip().lower()
        date_str_clean = date_str.strip()

        # Filter
        df_filtered = df[
            (df["district"] == district_name_clean) &
            (df["date"] == date_str_clean)
        ]

        # Debug print
        print("🧪 Checking rainfall for:", district_name_clean, date_str_clean)
        print("🗂️ Matching rows found:", len(df_filtered))

        if df_filtered.empty:
            raise ValueError("No matching row found.")

        row = df_filtered.iloc[0]


        rain_mm = float(row.get("rainfall_mm", 0))

        if rain_mm == 0:
            intensity = "No Rain" if lang == "en" else "कोई वर्षा नहीं"
        elif rain_mm < 1:
            intensity = "Very Light Rainfall" if lang == "en" else "बहुत हल्की वर्षा"
        elif rain_mm < 4:
            intensity = "Light Rainfall" if lang == "en" else "हल्की वर्षा"
        elif rain_mm < 10:
            intensity = "Moderate Rainfall" if lang == "en" else "मध्यम वर्षा"
        else:
            intensity = "Heavy Rainfall" if lang == "en" else "भारी वर्षा"

        return (
            f"📍 {district_name.title()}\n"
            f"🗓️ {date_str}\n"
            f"🌧️ {rain_mm:.1f} mm — {intensity}"
        )

    except Exception:
        return (
            f"❌ No rainfall data available for {district_name.title()} on {date_str}"
            if lang == "en"
            else f"❌ {district_name.title()} में {date_str} के लिए वर्षा डेटा उपलब्ध नहीं है"
        )



    
def get_weather_from_weatherstack(city_name):
    """Get current weather using Weatherstack API"""
    try:
        api_key = settings.WEATHERSTACK_API_KEY
        url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city_name}"
        print("📡 Fetching Weather for:", city_name)

        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("success") is False or "current" not in data:
            print("❌ Weatherstack API error:", data.get("error"))
            return None

        current = data["current"]
        return {
            "temperature": current["temperature"],
            "humidity": current["humidity"],
            "condition": current["weather_descriptions"][0]
        }

    except Exception as e:
        print(f"[ERROR] Weatherstack failed: {e}")
        return None



@csrf_exempt
def webhook(request):

    """Main Dialogflow webhook handler"""
    try:
        body = json.loads(request.body)
        session = body.get("session", "")
        query_text = body.get("queryResult", {}).get("queryText", "").lower()
        
        # Safely get parameters with proper fallback
        query_result = body.get("queryResult", {})
        params = query_result.get("parameters", {}) if query_result else {}
        if not isinstance(params, dict):
            params = {}
            
        intent_name = body.get("queryResult", {}).get("intent", {}).get("displayName", "").lower()

        # Detect language early (before any returns)
        is_hindi = (body.get("queryResult", {}).get("languageCode", "") == "hi" or 
                   any("\u0900" <= c <= "\u097F" for c in str(query_text)))

        if intent_name == "default fallback intent":
            fallback_hi = (
                "🤖 मुझे समझ नहीं आया। कृपया इन विषयों पर पूछें:\n"
                "• 🌧️ बारिश (जैसे: 'नागपुर में बारिश होगी?')\n"
                "• 🌾 फसल सलाह (जैसे: 'कपास के लिए पानी')\n"
                "• 📍 स्थान बताएं (जैसे: 'मैं वर्धा में हूँ')"
            )
            fallback_en = (
                "🤖 I didn't understand that. Please ask about:\n"
                "• 🌧️ Rainfall (e.g., 'Will it rain in Nagpur?')\n"
                "• 🌾 Crop advisory (e.g., 'Water needed for cotton')\n"
                "• 📍 Share your location (e.g., 'I am in Wardha')"
            )
            return JsonResponse({
                "fulfillmentText": fallback_hi if is_hindi else fallback_en,
                "outputContexts": []
            })

        # Handle agricultural KB queries
        is_hindi = (body.get("queryResult", {}).get("languageCode", "") == "hi" or 
                    any("\u0900" <= c <= "\u097F" for c in str(query_text)))

        # Safely get parameters with proper fallback
        query_result = body.get("queryResult", {})
        params = query_result.get("parameters", {}) if query_result else {}
        if not isinstance(params, dict):
            params = {}

        # Handle agricultural KB queries

        # Add this helper function at the top
        def is_pest_query(text):
            pest_terms = ["pest", "कीट", "insect", "bug", "symptoms", "control", "manage"]
            return any(term in text.lower() for term in pest_terms)

        # Then modify the pest handling block:
        if is_pest_query(query_text) or any(pest in query_text.lower() for pest in pest_kb["pest_details"]):
            # First try to match Hindi pest names
            matched_pest = None
            query_lower = query_text.lower()
            
            # Check Hindi names first
            for pest, details in pest_kb["pest_details"].items():
                hi_name = details.get("hi", {}).get("name", "").lower()
                if hi_name and hi_name in query_lower:
                    matched_pest = pest
                    break
            
            # If no Hindi match, check English names
            if not matched_pest:
                for pest in pest_kb["pest_details"]:
                    if pest.lower() in query_lower:
                        matched_pest = pest
                        break
            
            if matched_pest:
                advice = get_advice(matched_pest, None, "hi" if is_hindi else "en")
                if advice:
                    return JsonResponse({
                        "fulfillmentText": advice,
                        "outputContexts": []
                    })

            # Initialize variables for general agricultural queries
            crop = None
            category = None
            query_lower = query_text.lower()

            # Try to extract from hindi parameters first
            params = extract_hindi_parameters(query_text)
            if params:
                crop, category = params

            # If hindi params didn't work, detect from keywords
            if not category:
                # Map query keywords to categories
                keyword_to_category = {
                    "water": ["water", "पानी", "जल"],
                    "soil": ["soil", "मिट्टी"],
                    "pest": ["pest", "कीट"],
                    "fertilizer": ["fertilizer", "उर्वरक"],
                    "sowing": ["sowing", "बुवाई"],
                    "cost": ["cost", "expense", "लागत", "खर्च", "कीमत"]
                }
                
                for cat, keywords in keyword_to_category.items():
                    if any(keyword in query_lower for keyword in keywords):
                        category = cat
                        break

            # Combined crop mapping (English + Hindi)
            crop_mapping = {
                'cotton': ['cotton', 'kapas', 'कपास'],
                'soybean': ['soybean', 'soya', 'सोयाबीन'],
                'pigeonpea': ['pigeonpea', 'arhar', 'अरहर'],
                'sorghum': ['sorghum', 'jowar', 'ज्वार', 'ज्वारी'],
                'wheat': ['wheat', 'gehun', 'गेहूँ', 'गेहूं'],
                'rice': ['rice', 'chawal', 'चावल'],
                'maize': ['maize', 'makka', 'मक्का']
            }

            # First check for rice specifically (needs special handling)
            rice_terms = ['rice', 'chawal', 'चावल']
            if any(term in query_lower for term in rice_terms):
                crop = 'rice'
            else:
                # Check other crops normally
                for crop_name, terms in crop_mapping.items():
                    if any(term in query_lower for term in terms):
                        crop = crop_name
                        break

            # Only proceed if both crop and category are found
            if crop and category:
                advice = get_advice(category, crop, "hi" if is_hindi else "en")
                if advice:
                    return JsonResponse({
                        "fulfillmentText": advice.split("\n\n")[0] + "\n\nFor location-specific advice, share your district.",
                        "outputContexts": []
                    })
                else:
                    return JsonResponse({
                        "fulfillmentText": "No advice available for this query" if not is_hindi else "इस प्रश्न के लिए कोई सलाह उपलब्ध नहीं है",
                        "outputContexts": []
                    })
                
        # for live weather 
        if "weather" in intent_name or "मौसम" in query_text:
            city = params.get("district") or params.get("city")
            if not city:
                return JsonResponse({
                    "fulfillmentText": "📍 कृपया अपना शहर या जिला बताएं।" if is_hindi else "📍 Please specify your city or district.",
                    "outputContexts": []
                })

            weather = get_weather_from_weatherstack(city)
            if not weather:
                return JsonResponse({
                    "fulfillmentText": f"❌ {city.title()} के लिए मौसम डेटा नहीं मिला" if is_hindi else f"❌ No weather data found for {city.title()}",
                    "outputContexts": []
                })

            # 📦 Choose language dynamically
            if is_hindi:
                reply = (
                    f"📍 {city.title()}\n"
                    f"🌡️ तापमान: {weather.get('temperature', 'N/A')}°C\n"
                    f"💧 आर्द्रता: {weather.get('humidity', 'N/A')}%\n"
                    f"🌤️ स्थिति: {weather.get('condition', '-')}"
                )
            else:
                reply = (
                    f"📍 {city.title()}\n"
                    f"🌡️ Temperature: {weather.get('temperature', 'N/A')}°C\n"
                    f"💧 Humidity: {weather.get('humidity', 'N/A')}%\n"
                    f"🌤️ Condition: {weather.get('condition', '-')}"
                )

            return JsonResponse({
                "fulfillmentText": reply,
                "outputContexts": []
            })

        # Extract location
        state = params.get("state", "").strip().lower()
        district = params.get("district", "").strip().lower()
        
        # Check session for location
        session_data = request.session.get("location", {})
        state = state or session_data.get("state", "")
        district = district or session_data.get("district", "")
        
        # Fallback to IP geolocation
        if not state and not district:
            ip = request.META.get("REMOTE_ADDR", "")
            city, region = get_location_from_ip(ip)
            state = region or state
            district = city or district
        
        # Validate location
        print(f"🔍 Extracted District: '{district}' | Cleaned: '{clean_district_name(district.lower())}'")
        print(f"📋 Available Districts: {get_available_districts()}")
        if not district:
            return JsonResponse({
                "fulfillmentText": "📍 कृपया अपना स्थान बताएं (जैसे 'वर्धा' या 'महाराष्ट्र, वर्धा')" 
                if is_hindi else "📍 Please share your location (e.g., 'Wardha' or 'Maharashtra, Wardha')",
                "outputContexts": []
            })
        
        available_districts = get_available_districts()
        cleaned_district = clean_district_name(district)

        # BLOCK 1: Strict district validation
        if cleaned_district not in available_districts:
            # ✅ Try live forecast from Weatherstack instead of error
            weather = get_weather_from_weatherstack(cleaned_district)
            if weather:
                if is_hindi:
                    reply = (
                        f"📍 {cleaned_district.title()}\n"
                        f"🌡️ तापमान: {weather.get('temperature', 'N/A')}°C\n"
                        f"💧 आर्द्रता: {weather.get('humidity', 'N/A')}%\n"
                        f"🌤️ स्थिति: {weather.get('condition', '-')}"
                    )
                else:
                    reply = (
                        f"📍 {cleaned_district.title()}\n"
                        f"🌡️ Temperature: {weather.get('temperature', 'N/A')}°C\n"
                        f"💧 Humidity: {weather.get('humidity', 'N/A')}%\n"
                        f"🌤️ Condition: {weather.get('condition', '-')}"
                    )

                return JsonResponse({
                    "fulfillmentText": reply,
                    "outputContexts": []
                })

            # ❌ If even weatherstack fails, suggest default districts
            suggestions = get_close_matches(cleaned_district, available_districts, n=3, cutoff=0.5) or ['Nagpur', 'Wardha', 'Amravati']

            if is_hindi:
                msg = (f"❌ {district.title()} के लिए डेटा उपलब्ध नहीं है\n"
                    f"कृपया इन जिलों के बारे में पूछें: {', '.join([d.title() for d in suggestions])}")
            else:
                msg = (f"❌ Data not available for {district.title()}\n"
                    f"Please ask about: {', '.join([d.title() for d in suggestions])}")
            
            return JsonResponse({
                "fulfillmentText": msg,
                "outputContexts": []
            })

        # BLOCK 2: Only proceed if district is valid
        request.session["location"] = {
            "state": state,
            "district": cleaned_district  # Use cleaned version
        }
        request.session.modified = True
        
        # Save location to session
        request.session["location"] = {"state": state, "district": district}
        request.session.modified = True
        
        # Determine week
        date_str = params.get("date", "")
        week_term = params.get("week_term", "").lower()
        week_num = params.get("number")
        
        target_week = (get_week_from_date(date_str) if date_str else
                      min(get_current_week() + 1, 4) if week_term == "next" else
                      max(get_current_week() - 1, 1) if week_term == "last" else
                      int(week_num) if week_num and 1 <= int(week_num) <= 4 else
                      get_current_week())
        
        # Load week data
        df = load_week_data(target_week)
        if df is None:
            return JsonResponse({
                "fulfillmentText": "❌ डेटा उपलब्ध नहीं है" if is_hindi else "❌ Data not available",
                "outputContexts": []
            })
        
        # Find district match
        all_districts = tuple(df["district"].unique().tolist())  # Convert to tuple for lru_cache
        matched_district = find_closest_district_match(all_districts, district)
        # After district matching fails:
        # After finding district match fails:
        if not matched_district:
            available_dists = list(get_available_districts())
            if is_hindi:
                msg = (f"❌ {district.title()} के लिए मौसम डेटा उपलब्ध नहीं है\n"
                    f"कृपया इन जिलों में से पूछें: {', '.join([d.title() for d in available_dists[:3]])}")
            else:
                msg = (f"❌ Weather data not available for {district.title()}\n"
                    f"Please ask about these districts: {', '.join([d.title() for d in available_dists[:3]])}")
            
            return JsonResponse({
                "fulfillmentText": msg,
                "outputContexts": []
            })
                        
        
        # Get district record
        try:
            record = df[df["district"] == matched_district].iloc[0].to_dict()
        except:
            return JsonResponse({
                "fulfillmentText": f"❌ {district.title()}, {state.title()} के लिए कोई डेटा नहीं" 
                if is_hindi else f"❌ No data for {district.title()}, {state.title()}",
                "outputContexts": []
            })
        
        # Handle daily rainfall with Excel file
        if "rain" in intent_name:
            from datetime import datetime, timedelta

            query_lower = query_text.lower()

            # Get district from user input
            # Fallback: Extract city from text if not found in parameters
            district = params.get("district") or params.get("city")

            # Try fallback extraction from query
            if not district:
                import re
                match = re.search(r"in\s+([a-zA-Z\u0900-\u097F\s]+)", query_text)
                if match:
                    district = match.group(1).strip()

            # Hindi format: "<city> में"
            if not district:
                match_hi = re.search(r"([^\s]+)\s+में", query_text)
                if match_hi:
                    district = match_hi.group(1).strip()

            # Still not found?
            if not district:
                return JsonResponse({
                    "fulfillmentText": "📍 कृपया कोई शहर या ज़िले का नाम बताएं (जैसे 'नागपुर', 'वर्धा')" if is_hindi
                    else "📍 Please mention a district or city name (e.g., 'Nagpur', 'Akola')",
                    "outputContexts": []
                })

            # Normalize and translate Hindi city names (after district is found)
            def normalize_city(city_name):
                import unicodedata
                return unicodedata.normalize("NFKD", city_name).encode("ascii", "ignore").decode("utf-8")

            hindi_to_english_cities = {
                "जयपुर": "Jaipur",
                "नागपुर": "Nagpur",
                "अमरावती": "Amravati",
                "गुंटूर": "Guntur",
                "मुंबई": "Mumbai",
                "गोंदिया": "Gondia",
            }

            district_ascii = hindi_to_english_cities.get(district.strip(), normalize_city(district.strip()))

            # Date handling: today, tomorrow, yesterday, or date entity
            if "tomorrow" in query_lower or "कल" in query_lower:
                target_date = datetime.today() + timedelta(days=1)
            elif "yesterday" in query_lower or ("कल" in query_lower and "tomorrow" not in query_lower):
                target_date = datetime.today() - timedelta(days=1)
            else:
                date_str = params.get("date", "").strip()

                try:
                    if date_str:
                        target_date = dateutil.parser.parse(date_str)
                    elif "tomorrow" in query_text or "कल" in query_text:
                        target_date = datetime.today() + timedelta(days=1)
                    elif "yesterday" in query_text or ("कल" in query_text and "tomorrow" not in query_text):
                        target_date = datetime.today() - timedelta(days=1)
                    else:
                        target_date = datetime.today()
                except:
                    target_date = datetime.today()


            date_formatted = target_date.strftime("%Y-%m-%d")

            # Fetch rainfall from Excel
            rainfall_reply = get_rainfall_from_excel(
                date_formatted,
                district_name=district,
                lang="hi" if is_hindi else "en"
            )

            # If rainfall data was not found in Excel (starts with ❌), use Weatherstack instead
            if rainfall_reply.startswith("❌"):
                # 🌦️ Try Weatherstack for live weather
                live_weather = get_weather_from_weatherstack(district_ascii)
                if live_weather:
                    if is_hindi:
                        rainfall_reply = (
                            f"📍 {district.title()}\n"
                            f"🌡️ तापमान: {live_weather.get('temperature', 'N/A')}°C\n"
                            f"💧 आर्द्रता: {live_weather.get('humidity', 'N/A')}%\n"
                            f"🌤️ स्थिति: {live_weather.get('condition', '-')}"
                        )
                    else:
                        rainfall_reply = (
                            f"📍 {district.title()}\n"
                            f"🌡️ Temperature: {live_weather.get('temperature', 'N/A')}°C\n"
                            f"💧 Humidity: {live_weather.get('humidity', 'N/A')}%\n"
                            f"🌤️ Condition: {live_weather.get('condition', '-')}"
                        )

            return JsonResponse({
                "fulfillmentText": rainfall_reply,
                "outputContexts": []
            })
        
        # Generate response
        location = (f"{matched_district.title()}, {state.title()}" if state else 
                   matched_district.title())
        crop_type = params.get("crop", "").lower()
        
        response = f"📍 {location}\n🗓️ {record['week_start']} to {record['week_end']}\n"

        if is_hindi:
            response += f"🌱 {record['hi_crop_condition']}\n📋 {record['hi_advisory']}"
        else:
            response += f"🌱 {record['crop_condition']}\n📋 {record['advisory']}"


        
        # Prepare output contexts
        output_contexts = [{
            "name": f"{session}/contexts/location_context",
            "lifespanCount": 30,
            "parameters": {
                "state": state,
                "district": district,
                "week": target_week,
                "crop": crop_type
            }
        }]
        
        return JsonResponse({
            "fulfillmentText": response,
            "outputContexts": output_contexts
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            "fulfillmentText": "⚠️ Invalid request",
            "outputContexts": []
        }, status=400)
    except Exception as e:
        print(f"[ERROR] Webhook failed: {str(e)}")
        traceback.print_exc()
        return JsonResponse({
            "fulfillmentText": "⚠️ तकनीकी समस्या" if "hi" in body.get("queryResult", {}).get("languageCode", "") 
                            else "⚠️ Technical issue",
            "outputContexts": []
        }, status=500)
    
# helper function for hindi 
def is_hindi_query(text):
    """
    Check if text contains Hindi characters or is likely a Hindi query
    
    Args:
        text (str): Input text to check
        
    Returns:
        bool: True if text contains Hindi characters or common Hindi words
        
    Examples:
        >>> is_hindi_query("कपास के लिए पानी")
        True
        >>> is_hindi_query("cotton water needs")
        False
    """
    # Check for Devanagari Unicode block
    if any("\u0900" <= c <= "\u097F" for c in str(text)):
        return True
    
    # Check for common Hindi words even if mixed with English
    common_hindi_words = {"के", "लिए", "में", "की", "है"}
    return any(word in str(text).lower() for word in common_hindi_words)

@csrf_exempt
def live_weather(request):
    try:
        data = json.loads(request.body)
        city = data.get("city") or data.get("district")
        
        if not city:
            return JsonResponse({"error": "City is required"}, status=400)

        weather = get_weather_from_weatherstack(city)
        if not weather:
            return JsonResponse({"error": f"No weather found for {city}"}, status=404)

        return JsonResponse({
            "city": city.title(),
            "temperature": f"{weather['temperature']} °C",
            "humidity": f"{weather['humidity']}%",
            "condition": weather['condition']
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def extract_crop_from_query(query):
    crop_keywords = {
        'wheat': ['wheat', 'gehun', 'गेहूं', 'गेहूँ'],
        'rice': ['rice', 'chawal', 'चावल', 'धान'],
        'cotton': ['cotton', 'kapas', 'कपास'],
        'soybean': ['soybean', 'soyabean', 'soya', 'सोयाबीन', 'सोया'],
        'sorghum': ['sorghum', 'jowar', 'jawar', 'jovar', 'ज्वार', 'ज्वारी'],
        'pigeonpea': ['pigeonpea', 'arhar', 'tur', 'toor', 'तुअर', 'अरहर', 'तूर'],
        'maize': ['maize', 'corn', 'मक्का', 'मकई', 'bhutta', 'भुट्टा'],
    }


def extract_hindi_parameters(query_text):
    """Improved version that handles both English and Hindi crop names"""
    query_text = query_text.lower().strip()
    
    # Combined crop mapping (English + Hindi)
    crop_map = {
        'cotton': ['cotton', 'kapas', 'कपास'],
        'soybean': ['soybean', 'soya', 'सोयाबीन'],
        'pigeonpea': ['pigeonpea', 'arhar', 'अरहर'],
        'sorghum': ['sorghum', 'jowar', 'ज्वार', 'ज्वारी'],
        'wheat': ['wheat', 'gehun', 'गेहूँ', 'गेहूं'],
        'rice': ['rice', 'chawal', 'चावल', 'धान'],  # Added 'धान' for paddy
        'maize': ['maize', 'makka', 'मक्का'],
        'cost': ['cost', 'cultivation cost', 'farming cost', 'लागत', 
                'खेती की लागत', 'कृषि लागत', 'कितनी लागत', 
                'उत्पादन लागत', 'कीमत', 'फसल की लागत']
    }
    
    # Category mapping
    category_map = {
        'water': ['water', 'पानी', 'सिंचाई', 'जल'],  # Added 'जल' for water
        'soil': ['soil', 'मिट्टी'],
        'pest': ['pest', 'कीट'],
        'fertilizer': ['fertilizer', 'उर्वरक'],
        'sowing': ['sowing', 'बुवाई'], #idhar
        'cost': ['cost', 'cultivation cost', 'farming cost', 'लागत', 'खेती की लागत', 'कृषि लागत', 'कितनी लागत', 'उत्पादन लागत', 'कीमत', 'फसल की लागत'],
    }
    
    # Find crop - prioritize longer matches first
    crop = None
    for eng_name, terms in crop_map.items():
        # Check if any term appears in the query
        if any(term in query_text for term in terms):
            crop = eng_name
            break
    
    # Find category
    category = None
    for eng_name, terms in category_map.items():
        if any(term in query_text for term in terms):
            category = eng_name
            break
    
    return (crop, category) if (crop and category) else None


def handle_agricultural_query(query_text, is_hindi=False):
    """Improved query handler"""
    params = extract_hindi_parameters(query_text)
    if not params:
        return None

    crop, category = params
    lang = "hi" if is_hindi else "en"

    # ✅ Use the new get_advice
    advice = get_advice(category, crop, lang)

    # ✅ Return only the first chunk if needed
    return advice.split("\n\n")[0] if advice else None


# View Functions
@csrf_exempt
def rainfall_forecast(request):
    try:
        district = request.GET.get('district') or json.loads(request.body).get('district')
        if not district:
            return JsonResponse({
                "error": "Please specify a district",
                "example": "What's the rainfall forecast for Nagpur?"
            })
        
        is_valid, suggestions = validate_district(district)
        
        if not is_valid:
            response = {
                "error": f"No rainfall data available for {district.title()}",
                "available_locations": "Try these districts instead:",
                "suggestions": suggestions or list(get_available_districts())[:3]
            }
            return JsonResponse(response, status=404)
        
        # If valid district, proceed with forecast logic
        return JsonResponse({
            "response": f"Rainfall forecast for {district.title()}",
            "data": "..."  # Your forecast data here
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
def reverse_geocode(request):
    """Handle reverse geocoding requests from lat/long coordinates"""
    try:
        if request.method != "GET":
            return JsonResponse({"error": "Only GET requests are allowed"}, status=405)

        lat = request.GET.get("lat")
        lon = request.GET.get("lon")

        if not lat or not lon:
            return JsonResponse({"error": "Missing latitude or longitude parameters"}, status=400)

        # Use OpenCage Data API for reverse geocoding
        api_key = "6376cc17fac34e0696b69471a745066d"  # Replace with your actual API key
        response = requests.get(
            f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={api_key}"
        )

        if response.status_code != 200:
            return JsonResponse({"error": "Failed to fetch location data"}, status=500)

        data = response.json()
        if not data.get("results"):
            return JsonResponse({"error": "No location found for these coordinates"}, status=404)

        # Extract location components
        components = data["results"][0]["components"]
        state = components.get("state", "").lower()
        district = (components.get("county") or 
                  components.get("city") or 
                  components.get("town", "")).lower()

        if not state or not district:
            return JsonResponse({"error": "Incomplete location data"}, status=400)

        return JsonResponse({
            "state": state,
            "district": district
        })

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({
            "error": f"Server error: {str(e)}",
            "details": "Please check server logs"
        }, status=500)

@csrf_exempt
def chatbot_response(request):
    """Direct chat API endpoint"""
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        body = json.loads(request.body)
        user_message = body.get("message", "").strip().lower()
        if not user_message:
            return JsonResponse({"error": "Message required"}, status=400)

        # ✅ Detect language early
        is_hindi = is_hindi_query(user_message)

        # ✅ Initialize session
        if not request.session.session_key:
            request.session.save()
        session_id = request.session.session_key

        # ✅ Agricultural KB matching
        topics = ['water', 'soil', 'pest', 'fertilizer', 'sowing', 'cost']
        crops = ['cotton', 'soybean', 'pigeonpea', 'sorghum', 'rice', 'wheat', 'maize']

        detected_topic = next((t for t in topics if t in user_message), None)
        detected_crop = next((c for c in crops if c in user_message), None)

        if detected_topic and detected_crop:
            advice = get_advice(detected_topic, detected_crop, "hi" if is_hindi else "en")
            return JsonResponse({
                "response": f"{advice}\n\nFor location-specific advice, share your district."
            })

        # ✅ Fallback to Dialogflow for complex queries
        LANGUAGE_CODE = "en"  # always use English for NLP compatibility

        session_client = dialogflow.SessionsClient()
        session_path = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)

        text_input = dialogflow.TextInput(text=user_message, language_code=LANGUAGE_CODE)
        query_input = dialogflow.QueryInput(text=text_input)

        try:
            response = session_client.detect_intent(
                request={"session": session_path, "query_input": query_input}
            )

            bot_reply = response.query_result.fulfillment_text.strip()

            if not bot_reply or "I specialize in agricultural advice" in bot_reply:
                bot_reply = (
                    "⚠️ माफ कीजिए, मैं आपकी बात नहीं समझ पाया। कृपया फसल या वर्षा के बारे में पूछें।"
                    if is_hindi else
                    "⚠️ Sorry, I couldn't understand that. Please ask about crops or rainfall."
                )

            return JsonResponse({
                "response": bot_reply,
                "intent": response.query_result.intent.display_name
            })

        except Exception as e:
            print(f"[ERROR] Dialogflow failed: {str(e)}")
            return JsonResponse({
                "response": (
                    "⚠️ तकनीकी समस्या। कृपया पुनः प्रयास करें।"
                    if is_hindi else
                    "⚠️ I'm having trouble processing your request. Please try again."
                )
            })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        print(f"[ERROR] Chat failed: {str(e)}")
        return JsonResponse({
            "response": "⚠️ Temporary system issue. Please try again.",
            "error": str(e)
        }, status=500)

# Optional timing print for debugging
import time
start = time.time()
print("Time taken:", time.time() - start)

    
import time
start = time.time()
# your code
print("Time taken:", time.time() - start)

@csrf_exempt
def set_location(request):
    """Manual location setting endpoint"""
    try:
        if request.method != "POST":
            return JsonResponse({"error": "Only POST allowed"}, status=405)
        
        data = json.loads(request.body)
        state = data.get("state", "").strip().lower()
        district = data.get("district", "").strip().lower()
        
        if not district:
            return JsonResponse({"error": "District is required"}, status=400)
        
        request.session["location"] = {"state": state, "district": district}
        request.session.modified = True
        
        location_str = f"{district.title()}"
        if state:
            location_str += f", {state.title()}"
        
        return JsonResponse({
            "message": f"✅ Location set to {location_str}",
            "location": {"state": state, "district": district}
        })
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    


