from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('add-district/',district_info,name="add-district"),
    path('display_district/',display_district,name="display_district"),
	path('delete-district/<int:id>/',delete_district, name="delete-district"),
    path('edit-district/<int:id>/',edit_district, name="edit-district"),
    path('display_all_district/',display_all_district, name="display_all_district"),
    path('investigator_list/',investigator_list, name="investigator_list"),

    path('sandard_week/', sandard_week, name='sandard_week'),
    
    
    path('api/districts/', DistrictList.as_view(), name='district-list'),
    path('api/standardweek/', StandardWeekList.as_view(), name='standard-week'),
    path('api/servey_info/', FarmerListCreateAPIView.as_view(), name='serveyinfo_list_create_api'),
    path('api/servey_info/<int:pk>/', FarmerDetailAPIView.as_view(), name='serveyinfo_detail_api'),
    path('api/investigator_entries/', InvestigatorEntriesAPIView.as_view(), name='investigator_entries'),
    path('api/basicservey_update/<int:pk>/', InvestigatorEntryEditAPIView.as_view(), name='edit_investigator_entry'),
    path('api/weeklyreports_entries/', ReportsEntriesAPIView.as_view(), name='weeklyreports_entries'),
    path('api/managereports_update/<int:pk>/', ManageReportsEditAPIView.as_view(), name='edit_managereports'),
    path('api/represented_photographs/', RepresentedPhotographListCreateAPIView.as_view(), name='represented_photographs'),
    path('api/assessment_season/', AssessmentSeasonListCreateAPIView.as_view(), name='assessment_season'),
    path('api/year_progress_report/', YearlyProgressReportCreateAPIView.as_view(), name='year_progress_report'),

    path('api/basic_servey_info/', BasicServeyInfoView.as_view(), name='basic_servey_info'),

    path('api/basic_servey_data/', basic_servey_data_view, name='basic_servey_data'),

    path('api/news-articles/', NewsArticleCreateAPIView.as_view(), name='news-article-create'),
    path('api/news-articles/list/', NewsArticleListAPIView.as_view(), name='news-article-list'),  # GET all articles
    path('api/news-articles/<int:id>/', NewsArticleDetailAPIView.as_view(), name='news-article-detail'),  # GET a specific article


]