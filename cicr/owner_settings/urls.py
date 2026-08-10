from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('add-user-district/',view_district, name="add-user-district"),
    path('view-user/<str:district_user>/',view_user, name="view-user"),
    path('users/<str:district_user>/',user_management,name="users"),
    path('investigator_district/',investigator_district,name="investigator_district"),
    path('investigator_details/<str:district_name>/',investigator_details,name="investigator_details"),
    path('delete_investigator/<str:user_id>/',delete_investigator,name="delete_investigator"),

    path('admin_district/',admin_district,name="admin_district"),
    path('admin_user/<str:district_name>/',admin_user,name="admin_user"),

    path('edit_admin/<int:id>/',edit_admin,name="edit_admin"),
    path('delete_admin/<int:id>/',delete_admin,name="delete_admin"),

    # monthly report for admin
    path('monthly_report_month/<str:district_name>/',monthly_report_month, name="monthly_report_month"),
    path('monthly_progress_report/<str:district_name>/<str:month>/',monthly_progress_report, name="monthly_progress_report"),

    path('basic_district/',basic_district, name="basic_district"),
    path('basic_servery_report/<str:district_name>/',basic_servery_report, name="basic_servery_report"),

    path('admin_basic_servery/<str:district_name>/',admin_basic_servery, name="admin_basic_servery"),
    path('admin_weekly_report/<str:district_name>/',admin_weekly_report,name="admin_weekly_report"),

    path('weekly_district/',weekly_district, name="weekly_district"),
    path('pest_weekly_report/<str:district_name>/',pest_weekly_report,name="pest_weekly_report"),

    path('display_weeks/',display_weeks,name="display_weeks"),

    # monthly report for super admin
    path('monthly_district/',monthly_district, name="monthly_district"),
    path('super_monthly_report/<str:district_name>/',super_monthly_report,name="super_monthly_report"),
    path('super_monthly_progress/<str:district_name>/<str:month>/',super_monthly_progress, name="super_monthly_progress"),

    # Weekly report for admin
    path('admin_weeks/<str:district_name>/',admin_weeks, name="admin_weeks"),
    path('weekly_pestincident_admin/<str:district_name>/<str:standard_number>/',weekly_pestincident_admin,name="weekly_pestincident_admin"),

    # Yearly report for admin
    path('admin_year/<str:district_name>/',admin_year,name="admin_year"),
    path('yearly_admin_report/<str:district_name>/<str:year>/',yearly_admin_report,name="yearly_admin_report"),

    # Yearly report for super admin
    path('yearly_district/',yearly_district,name="yearly_district"),
    path('superadmin_year/<str:district_name>/',superadmin_year,name="superadmin_year"),
    path('yearly_super_report/<str:district_name>/<str:year>/',yearly_super_report,name="yearly_super_report"),

    path('delete_servey_report/<str:district_name>/<int:id>/',delete_servey_report,name='delete_servey_report'),
    path('edit_servey_report/<str:district_name>/<int:id>/',edit_servey_report,name='edit_servey_report'),

    path('detailed_report/<str:district_name>/<str:month>/',detailed_report,name="detailed_report"),
    path('update_pest_incidence/<str:district_name>/<str:month>/<int:week_number>/', update_pest_incidence, name='update_pest_incidence'),
    

    
    # All API's 
    path('api/pest_incidence_data/', PestIncidenceDataListCreateAPIView.as_view(), name='pest_incidence_data_list_create'),
    path('api/pest_incidence_data/<int:pk>/', PestIncidenceDataDetailAPIView.as_view(), name='pest_incidence_data_detail'),
    path('api/monthly_physical_progress/', MonthlyPhysicalProgressListCreateAPIView.as_view(), name='monthly_physical_progress_list_create'),
    path('api/monthly_physical_progress/<int:pk>/', MonthlyPhysicalProgressDetailAPIView.as_view(), name='monthly_physical_progress_detail'),
    path('api/extension_activities/', ExtensionActivitiesListCreateAPIView.as_view(), name='extension_activities_list_create'),
    path('api/extension_activities/<int:pk>/', ExtensionActivitiesDetailAPIView.as_view(), name='extension_activities_detail'),

    path('api/monthly-progress-report/<str:district_name>/<str:month>/', monthly_progress_report_api, name='monthly-progress-report-api'),
    
]
