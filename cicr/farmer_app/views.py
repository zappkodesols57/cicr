import random
import string
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

# REST Framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import FarmerOTP, FarmerProfile
from .serializers import FarmerProfileSerializer, SendOTPSerializer, VerifyOTPSerializer

User = get_user_model()

# =====================================================================
# WEB UI VIEWS
# =====================================================================

def farmer_login_view(request):
    """
    Renders the farmer OTP login web page.
    If the farmer is already logged in, redirect them to the dashboard.
    """
    if request.user.is_authenticated and getattr(request.user, 'is_farmer', False):
        return redirect('farmer_dashboard')
    return render(request, 'farmer_app/farmer_login.html')

def farmer_dashboard_view(request):
    """
    Displays the public farmer dashboard.
    """
    context = {
        'active_tab': 'home',
    }
    return render(request, 'farmer_app/farmer_dashboard.html', context)


def farmer_advisories_view(request):
    return render(request, 'farmer_app/farmer_advisories.html', {
        'active_tab': 'advisories',
    })


def farmer_advisory_detail_view(request, advisory_id):
    return render(request, 'farmer_app/farmer_advisory_detail.html', {
        'active_tab': 'advisories',
        'advisory_id': advisory_id,
    })


def farmer_calculator_view(request):
    return render(request, 'farmer_app/farmer_calculator.html', {
        'active_tab': 'calculator',
    })


def farmer_pest_view(request):
    return render(request, 'farmer_app/farmer_pest.html', {
        'active_tab': 'pest',
    })


def farmer_pest_detail_view(request, pest_id):
    return render(request, 'farmer_app/farmer_pest_detail.html', {
        'active_tab': 'pest',
        'pest_id': pest_id,
    })


def farmer_logout_view(request):
    """
    Logs out the farmer and redirects to the login page.
    """
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('farmer_login')


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
