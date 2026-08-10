import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_FILE = os.path.join(BASE_DIR, "agriculture_kb.json")
PEST_KB_FILE = os.path.join(BASE_DIR, "pest_management_kb.json")

# Load both knowledge bases
with open(KB_FILE, "r", encoding="utf-8") as f:
    agriculture_kb = json.load(f)

with open(PEST_KB_FILE, "r", encoding="utf-8") as f:
    pest_kb = json.load(f)

def get_advice(topic, crop=None, lang="en"):
    topic = topic.lower().strip()
    crop = crop.lower().strip() if crop else None
    lang = lang.lower()

    # First check if it's a pest query
    if topic in pest_kb["pest_details"]:
        return format_pest_response(pest_kb["pest_details"][topic], lang)

    # Original agriculture KB handling
    topic_info = agriculture_kb.get(topic, {})
    if not topic_info:
        return "Information not available" if lang == "en" else "जानकारी उपलब्ध नहीं"

    crop_variations = {
        'wheat': ['wheat', 'gehun', 'गेहूँ', 'गेहूं'],
        'rice': ['rice', 'chawal', 'धान', 'चावल'],
        'cotton': ['cotton', 'kapas', 'कपास'],
        'soybean': ['soybean', 'soya', 'सोयाबीन'],
        'pigeonpea': ['pigeonpea', 'arhar', 'अरहर'],
        'sorghum': ['sorghum', 'jowar', 'ज्वार', 'ज्वारी'],
        'maize': ['maize', 'makka', 'मक्का']
    }

    standard_crop = None
    if crop:
        for std_crop, variants in crop_variations.items():
            if crop in variants:
                standard_crop = std_crop
                break

        if not standard_crop and crop in topic_info:
            standard_crop = crop

    if standard_crop and standard_crop in topic_info:
        response = topic_info[standard_crop]
        return response.split('\n')[0] if lang == "en" else response.split('\n')[1] if '\n' in response else response

    if crop:
        return "Crop-specific advice not available" if lang == "en" else "फसल-विशिष्ट सलाह उपलब्ध नहीं है"

    default_response = topic_info.get("default", "")
    return default_response.split('\n')[0] if lang == "en" and '\n' in default_response else default_response.split('\n')[1] if '\n' in default_response else default_response

def format_pest_response(pest_data, lang="en"):
    """Format pest information in requested language"""
    if lang == "hi":
        hi_data = pest_data.get("hi", {})
        return (
            f"{hi_data.get('name', pest_data.get('name', 'N/A'))} ({hi_data.get('scientific_name', pest_data.get('scientific_name', 'N/A'))})\n"
            f"प्रकार: {hi_data.get('type', pest_data.get('type', 'N/A'))}\n"
            f"स्थिति: {hi_data.get('status', pest_data.get('status', 'N/A'))}\n"
            f"क्षति: {hi_data.get('damage', pest_data.get('damage', 'N/A'))}\n"
            f"आर्थिक सीमा: {hi_data.get('etl', pest_data.get('etl', 'N/A'))}\n"
            "प्रबंधन:\n" + 
            "\n".join([f"- {stage}: {advice}" for stage, advice in hi_data.get('management', pest_data.get('management', {})).items()])
        )
    else:
        return (
            f"{pest_data.get('name', 'N/A')} ({pest_data.get('scientific_name', 'N/A')})\n"
            f"Type: {pest_data.get('type', 'N/A')}\n"
            f"Status: {pest_data.get('status', 'N/A')}\n"
            f"Damage: {pest_data.get('damage', 'N/A')}\n"
            f"ETL: {pest_data.get('etl', 'N/A')}\n"
            "Management:\n" +
            "\n".join([f"- {stage}: {advice}" for stage, advice in pest_data.get('management', {}).items()])
        )