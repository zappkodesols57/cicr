# geo_location.py - Enhanced version
import requests
from django.core.cache import cache  # Use Django's cache instead of global var
import re

def get_location_from_ip(ip, timeout=3):
    """Get location with caching and better error handling"""
    cache_key = f"ip_location_{ip}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    try:
        if ip == "127.0.0.1":
            result = ("nagpur", "maharashtra")
        else:
            response = requests.get(
                f"https://ipapi.co/{ip}/json/",
                timeout=timeout
            )
            response.raise_for_status()
            data = response.json()
            result = (
                data.get("city", "").strip().lower(),
                data.get("region", "").strip().lower()
            )
        
        cache.set(cache_key, result, timeout=3600)  # Cache for 1 hour
        return result
    except Exception as e:
        print(f"IP Location Error: {str(e)}")
        return None, None
    
# utils/geo_location.py


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

def get_location_from_ip(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        data = response.json()
        city = data.get("city", "")
        region = data.get("region", "")
        return city.strip().lower(), region.strip().lower()
    except Exception as e:
        print("IP Location Error:", e)
        return None, None