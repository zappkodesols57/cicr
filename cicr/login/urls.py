from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from .views import get_csrf_token


urlpatterns = [
    path('', super_login, name='super_login'),
    path('web_aap/', web_aap, name='web_aap'),
    path('super_dashboard/', super_dashboard, name='super_dashboard'),
    path('create-investigator/', create_investigator, name='create_investigator'),
    path('login_investigator/', login_investigator, name='login_investigator'),
    path('success/', success_page, name='success_page'),
    path('investigator_dashboard/', investigator_dashboard, name='investigator_dashboard'),
    path('login/', login_view, name='admin_login'),
    path('dashboard_admin/', dashboard_admin, name='dashboard_admin'),
    path('logout/', logout_view,name="logout"),
    path('logout_admin/', logout_admin,name="logout_admin"),


    path('admin_profile/', admin_profile,name="admin_profile"),

    path('create/', advisory_create, name='advisory_create'),
    path('update/<int:id>/', advisory_update, name='advisory_update'),
    path('delete/<int:id>/', advisory_delete, name='advisory_delete'),
    path('advisory_list/',advisory_list, name='advisory_list'),
    
    path('api/create_investigator/', create_investigator_api, name='create_investigator_api'),
    path('api/login_investigator/', login_investigator_api, name='login_investigator_api'),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),

    path('api/advisory/', AdvisoryCreateAPIView.as_view(), name='advisory-create'),
    path('api/advisory/<int:pk>/', AdvisoryDetailAPIView.as_view(), name='advisory-detail'),

    path('banners/', banner_list, name='banner_list'),
    path('banners/add/', banner_add, name='banner_add'),
    path('banners/edit/<int:banner_id>/', banner_edit, name='banner_edit'),
    path('banners/delete/<int:banner_id>/', banner_delete, name='banner_delete'),
    
    path('api/banners/', banner_list_api, name='banner_list_api'),

    path('change-financial-year/', change_financial_year, name='change_financial_year'),
    
    path('financial_year_list/', financial_year_list, name='financial_year_list'),
    path('year_delete/<int:year_id>/', year_delete, name='year_delete'),
    
]
    
