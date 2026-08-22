import random
import string
import json
import hashlib
import os
import re
import urllib.parse
import urllib.request
from functools import wraps
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# REST Framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import FarmerOTP, FarmerProfile
from .serializers import FarmerProfileSerializer, SendOTPSerializer, VerifyOTPSerializer

User = get_user_model()

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat",
    "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
    "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh",
    "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands", "Chandigarh",
    "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Jammu and Kashmir", "Ladakh",
    "Lakshadweep", "Puducherry",
]


def farmer_required(view_func):
    """Require a logged-in session belonging to a farmer account; otherwise send to farmer login."""
    @wraps(view_func)
    @login_required(login_url='/farmer/login/')
    def wrapper(request, *args, **kwargs):
        if not getattr(request.user, 'is_farmer', False):
            return redirect('farmer_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def _farmer_user_id(mobile_number):
    return f"farmer_{mobile_number}"


# =====================================================================
# WEB UI VIEWS
# =====================================================================

def farmer_login_view(request):
    """
    Farmer login using mobile number + password.
    If the farmer is already logged in, redirect them to the dashboard.
    """
    if request.user.is_authenticated and getattr(request.user, 'is_farmer', False):
        return redirect('farmer_dashboard')

    error_message = None
    if request.method == 'POST':
        mobile_number = request.POST.get('mobile_number', '').strip()
        password = request.POST.get('password', '')

        if not mobile_number or not password:
            error_message = "Please enter your mobile number and password."
        else:
            user = authenticate(request, username=_farmer_user_id(mobile_number), password=password)
            if user is not None and getattr(user, 'is_farmer', False):
                login(request, user)
                return redirect('farmer_dashboard')
            error_message = "Invalid mobile number or password."

    return render(request, 'farmer_app/farmer_login.html', {'error_message': error_message})


def farmer_register_view(request):
    """
    Farmer self-registration: Full Name, Mobile Number, Password, Confirm Password, State, District.
    """
    if request.user.is_authenticated and getattr(request.user, 'is_farmer', False):
        return redirect('farmer_dashboard')

    error_message = None
    form_data = {}

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        mobile_number = request.POST.get('mobile_number', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        state = request.POST.get('state', '').strip()
        district = request.POST.get('district', '').strip()
        form_data = {
            'full_name': full_name, 'mobile_number': mobile_number,
            'state': state, 'district': district,
        }

        if not all([full_name, mobile_number, password, confirm_password, state, district]):
            error_message = "Please fill in all required fields."
        elif not re.fullmatch(r'[6-9]\d{9}', mobile_number):
            error_message = "Please enter a valid 10-digit mobile number."
        elif password != confirm_password:
            error_message = "Password and Confirm Password do not match."
        elif len(password) < 6:
            error_message = "Password must be at least 6 characters long."
        elif User.objects.filter(mobile_number=mobile_number).exists():
            error_message = "An account with this mobile number already exists. Please login instead."
        else:
            user_id = _farmer_user_id(mobile_number)
            if User.objects.filter(user_id=user_id).exists():
                user_id = f"{user_id}_{random.randint(1000, 9999)}"

            user = User.objects.create(
                user_id=user_id,
                mobile_number=mobile_number,
                first_name=full_name,
                user_district=district,
                is_farmer=True,
                is_active=True,
                is_superuser=False,
                is_staff=False,
            )
            user.set_password(password)
            user.save()

            FarmerProfile.objects.create(
                user=user,
                first_name=full_name,
                mobile_number=mobile_number,
                state=state,
                district=district,
            )

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('farmer_dashboard')

    return render(request, 'farmer_app/farmer_register.html', {
        'error_message': error_message,
        'form_data': form_data,
        'states': INDIAN_STATES,
    })


@farmer_required
def farmer_dashboard_view(request):
    """
    Displays the public farmer dashboard.
    """
    context = {
        'active_tab': 'home',
    }
    return render(request, 'farmer_app/farmer_dashboard.html', context)


@farmer_required
def farmer_advisories_view(request):
    return render(request, 'farmer_app/farmer_advisories.html', {
        'active_tab': 'advisories',
    })


@farmer_required
def farmer_advisory_detail_view(request, advisory_id):
    return render(request, 'farmer_app/farmer_advisory_detail.html', {
        'active_tab': 'advisories',
        'advisory_id': advisory_id,
    })


@farmer_required
def farmer_calculator_view(request):
    return render(request, 'farmer_app/farmer_calculator.html', {
        'active_tab': 'calculator',
    })


@farmer_required
def farmer_calculator_detail_view(request, calculator_type):
    return render(request, 'farmer_app/farmer_calculator_detail.html', {
        'active_tab': 'calculator',
        'calculator_type': calculator_type,
    })


@farmer_required
def farmer_pest_view(request):
    return render(request, 'farmer_app/farmer_pest.html', {
        'active_tab': 'pest',
    })


@farmer_required
def farmer_pest_detail_view(request, pest_id):
    return render(request, 'farmer_app/farmer_pest_detail.html', {
        'active_tab': 'pest',
        'pest_id': pest_id,
    })


@farmer_required
def farmer_profile_view(request):
    """
    Lets a farmer view/edit their profile details and upload a profile photo.
    Uploading a new photo deletes the previously stored one from disk.
    """
    profile, _created = FarmerProfile.objects.get_or_create(
        user=request.user,
        defaults={'mobile_number': request.user.mobile_number, 'first_name': request.user.first_name},
    )

    success_message = None
    error_message = None

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        state = request.POST.get('state', '').strip()
        district = request.POST.get('district', '').strip()

        if not full_name or not state or not district:
            error_message = "Full name, state and district are required."
        else:
            profile.first_name = full_name
            profile.state = state
            profile.district = district

            new_photo = request.FILES.get('photo')
            if new_photo:
                if profile.photo and os.path.isfile(profile.photo.path):
                    os.remove(profile.photo.path)
                profile.photo = new_photo

            profile.save()

            request.user.first_name = full_name
            request.user.user_district = district
            request.user.save()

            success_message = "Profile updated successfully."

    return render(request, 'farmer_app/farmer_profile.html', {
        'active_tab': 'profile',
        'profile': profile,
        'states': INDIAN_STATES,
        'success_message': success_message,
        'error_message': error_message,
    })


def farmer_logout_view(request):
    """
    Logs out the farmer and redirects to the login page.
    """
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('farmer_login')


@csrf_exempt
@require_POST
def farmer_translate_api(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (TypeError, ValueError, UnicodeDecodeError):
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

    target = payload.get('target')
    texts = payload.get('texts', [])
    if target not in {'hi', 'mr'}:
        return JsonResponse({'translations': {text: text for text in texts if isinstance(text, str)}})
    if not isinstance(texts, list):
        return JsonResponse({'error': 'texts must be a list.'}, status=400)

    clean_texts = []
    seen = set()
    for text in texts[:80]:
        if not isinstance(text, str):
            continue
        clean = ' '.join(text.split()).strip()
        if not clean or clean in seen:
            continue
        seen.add(clean)
        clean_texts.append(clean)

    translations = {}
    missing = []
    for text in clean_texts:
        cache_key = _translation_cache_key(target, text)
        cached = cache.get(cache_key)
        if cached:
            translations[text] = cached
        else:
            missing.append(text)

    if missing:
        translated_missing = _translate_texts(missing, target)
        for text, translated in translated_missing.items():
            translations[text] = translated
            cache.set(_translation_cache_key(target, text), translated, 60 * 60 * 24 * 30)

    return JsonResponse({'translations': translations})


def _translation_cache_key(target, text):
    digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return f'farmer_translate:{target}:{digest}'


def _translate_texts(texts, target):
    separator = '\n<<<CICR_TRANSLATE_SPLIT>>>\n'
    joined = separator.join(texts)
    translated_joined = _translate_text(joined, target)
    parts = [part.strip() for part in translated_joined.split('<<<CICR_TRANSLATE_SPLIT>>>')]
    if len(parts) != len(texts):
        parts = [_translate_text(text, target) for text in texts]
    return {source: translated or source for source, translated in zip(texts, parts)}


def _translate_text(text, target):
    query = urllib.parse.urlencode({
        'client': 'gtx',
        'sl': 'en',
        'tl': target,
        'dt': 't',
        'q': text,
    })
    url = f'https://translate.googleapis.com/translate_a/single?{query}'
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request, timeout=4) as response:
            data = json.loads(response.read().decode('utf-8'))
        translated = ''.join(part[0] for part in data[0] if part and part[0])
        return translated or text
    except Exception:
        return text


# =====================================================================
# REST API ENDPOINTS
# =====================================================================

class SendOTPAPIView(APIView):
    """
    API endpoint to send/generate an OTP for a given mobile number.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        mobile_number = serializer.validated_data['mobile_number']
        
        # Generate 6-digit OTP
        otp = "".join(random.choices(string.digits, k=6))
        
        # Update or create OTP record
        otp_record, created = FarmerOTP.objects.update_or_create(
            mobile_number=mobile_number,
            defaults={
                'otp': otp,
                'created_at': timezone.now(),
                'is_verified': False
            }
        )

        # Simulate sending OTP (Print to server console/logs)
        print("\n" + "=" * 50)
        print(f"SMS OTP SENT TO FARMER: {mobile_number}")
        print(f"OTP CODE: {otp}")
        print("=" * 50 + "\n")

        # For ease of testing, we return the OTP in the API response.
        # In production, this OTP would NOT be returned in JSON response.
        return Response({
            'message': 'OTP sent successfully (simulated).',
            'mobile_number': mobile_number,
            'otp': otp  # Provided for easy frontend development and API testing
        }, status=status.HTTP_200_OK)


class VerifyOTPAPIView(APIView):
    """
    API endpoint to verify OTP.
    Logs in the user on verification success.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        mobile_number = serializer.validated_data['mobile_number']
        otp = serializer.validated_data['otp']

        # Expiry time check (valid for 5 minutes)
        expiry_limit = timezone.now() - timedelta(minutes=5)
        
        otp_record = FarmerOTP.objects.filter(
            mobile_number=mobile_number,
            otp=otp,
            created_at__gte=expiry_limit,
            is_verified=False
        ).first()

        if not otp_record:
            return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        # Mark OTP as verified
        otp_record.is_verified = True
        otp_record.save()

        # Check if user with this mobile number exists
        user = User.objects.filter(mobile_number=mobile_number).first()
        is_new_user = False

        if not user:
            is_new_user = True
            # Create user account
            user_id = f"farmer_{mobile_number}"
            # Check if this user_id is already taken (rare case)
            if User.objects.filter(user_id=user_id).exists():
                user_id = f"farmer_{mobile_number}_{random.randint(1000, 9999)}"

            user = User.objects.create(
                user_id=user_id,
                mobile_number=mobile_number,
                first_name="Farmer",
                is_farmer=True,
                is_active=True,
                is_superuser=False,
                is_staff=False
            )
            # Set a random unusable password
            random_password = "".join(random.choices(string.ascii_letters + string.digits, k=15))
            user.set_password(random_password)
            user.save()

        # Update user's is_farmer flag if not already set
        if not getattr(user, 'is_farmer', False):
            user.is_farmer = True
            user.save()

        # Ensure FarmerProfile exists
        profile, profile_created = FarmerProfile.objects.get_or_create(
            user=user,
            defaults={'mobile_number': mobile_number}
        )

        # Manually attach ModelBackend and log user in for session authentication
        if not hasattr(user, 'backend'):
            user.backend = 'django.contrib.auth.backends.ModelBackend'
        
        login(request, user)

        return Response({
            'message': 'Login successful.',
            'is_new_user': is_new_user,
            'user_id': user.user_id,
            'mobile_number': user.mobile_number,
            'profile': FarmerProfileSerializer(profile).data
        }, status=status.HTTP_200_OK)


class UpdateFarmerProfileAPIView(APIView):
    """
    API endpoint for farmers to view and update their profile details.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not getattr(request.user, 'is_farmer', False):
            return Response({'error': 'Only farmers can access this profile API.'}, status=status.HTTP_403_FORBIDDEN)
            
        profile, created = FarmerProfile.objects.get_or_create(
            user=request.user,
            defaults={'mobile_number': request.user.mobile_number}
        )
        serializer = FarmerProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if not getattr(request.user, 'is_farmer', False):
            return Response({'error': 'Only farmers can update this profile API.'}, status=status.HTTP_403_FORBIDDEN)

        profile, created = FarmerProfile.objects.get_or_create(
            user=request.user,
            defaults={'mobile_number': request.user.mobile_number}
        )
        serializer = FarmerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Synchronize name/district with Auth User model
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            district = serializer.validated_data.get('district')
            
            if first_name is not None:
                request.user.first_name = first_name
            if last_name is not None:
                request.user.last_name = last_name
            if district is not None:
                request.user.user_district = district
            
            if first_name is not None or last_name is not None or district is not None:
                request.user.save()
                
            return Response({
                'message': 'Profile updated successfully.',
                'profile': serializer.data
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
