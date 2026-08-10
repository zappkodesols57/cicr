from django.urls import path
from . import views

urlpatterns = [
    # Web UI Paths
    path('', views.farmer_dashboard_view, name='farmer_home'),
    path('login/', views.farmer_login_view, name='farmer_login'),
    path('dashboard/', views.farmer_dashboard_view, name='farmer_dashboard'),
    path('advisories/', views.farmer_advisories_view, name='farmer_advisories'),
    path('advisories/<int:advisory_id>/', views.farmer_advisory_detail_view, name='farmer_advisory_detail'),
    path('calculator/', views.farmer_calculator_view, name='farmer_calculator'),
    path('pest/', views.farmer_pest_view, name='farmer_pest'),
    path('pest/<int:pest_id>/', views.farmer_pest_detail_view, name='farmer_pest_detail'),
    path('logout/', views.farmer_logout_view, name='farmer_logout'),

    # REST API Paths
    path('api/send-otp/', views.SendOTPAPIView.as_view(), name='farmer_api_send_otp'),
    path('api/verify-otp/', views.VerifyOTPAPIView.as_view(), name='farmer_api_verify_otp'),
    path('api/update-profile/', views.UpdateFarmerProfileAPIView.as_view(), name='farmer_api_update_profile'),
]
