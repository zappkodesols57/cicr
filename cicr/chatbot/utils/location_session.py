# location_session.py - Improved version
def set_user_location(session, state=None, district=None):
    """Safely set location in session with validation"""
    if not district:
        return False
    
    location = session.get("location", {})
    if state:
        location["state"] = state.lower().strip()
    if district:
        location["district"] = clean_district_name(district)
    
    session["location"] = location
    session.modified = True
    return True

def get_user_location(session):
    """Get location with fallbacks"""
    location = session.get("location", {})
    return {
        "state": location.get("state", ""),
        "district": location.get("district", "")
    }