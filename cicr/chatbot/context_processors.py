def location_context(request):
    return {
        'user_state': request.session.get('user_state', ''),
        'user_district': request.session.get('user_district', '')
    }
