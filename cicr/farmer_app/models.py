from django.db import models
from django.conf import settings

class FarmerOTP(models.Model):
    mobile_number = models.CharField(max_length=15, db_index=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.mobile_number} - {self.otp} - Verified: {self.is_verified}"

class FarmerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='farmer_profile')
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True, default='')
    district = models.CharField(max_length=100, blank=True, null=True, default='')
    taluka = models.CharField(max_length=100, blank=True, null=True, default='')
    village = models.CharField(max_length=100, blank=True, null=True, default='')
    gender = models.CharField(max_length=20, blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Farmer Profile: {self.first_name or ''} {self.last_name or ''} ({self.mobile_number or ''})"
