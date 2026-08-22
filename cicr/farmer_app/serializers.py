from rest_framework import serializers
from .models import FarmerProfile, FarmerOTP

class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = ['first_name', 'last_name', 'mobile_number', 'state', 'district', 'taluka', 'village', 'gender', 'photo']

class SendOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=15)

    def validate_mobile_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Mobile number must contain only digits.")
        if len(value) < 10 or len(value) > 15:
            raise serializers.ValidationError("Mobile number must be between 10 and 15 digits.")
        return value

class VerifyOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)
