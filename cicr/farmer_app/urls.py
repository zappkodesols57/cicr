from django.urls import path
from . import views

urlpatterns = [
    # Web UI Paths
    path('login/', views.farmer_login_view, name='farmer_login'),
    path('dashboard/', views.farmer_dashboard_view, name='farmer_dashboard'),
    path('logout/', views.farmer_logout_view, name='farmer_logout'),

    # REST API Paths
    path('api/send-otp/', views.SendOTPAPIView.as_view(), name='farmer_api_send_otp'),
    path('api/verify-otp/', views.VerifyOTPAPIView.as_view(), name='farmer_api_verify_otp'),
    path('api/update-profile/', views.UpdateFarmerProfileAPIView.as_view(), name='farmer_api_update_profile'),
]
