def farmer_profile_photo(request):
    user = getattr(request, 'user', None)
    if user and user.is_authenticated and getattr(user, 'is_farmer', False):
        profile = getattr(user, 'farmer_profile', None)
        if profile and profile.photo:
            return {'farmer_profile_photo_url': profile.photo.url}
    return {'farmer_profile_photo_url': None}
