from django.shortcuts import get_object_or_404, render,redirect
from investigator_app.models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import monthly_physical_progress
from .serializers import MonthlyPhysicalProgressSerializer
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from .serializers import ExtensionActivitiesSerializer

from django.db.models import Avg
from django.shortcuts import render
from login.models import *
from investigator_app.models import *
from owner_settings.models import *

from django.urls import reverse
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.db.models import Sum, F, ExpressionWrapper, IntegerField
import random
import string
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from login.models import *
from login.models import User as CustomUser

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from django.shortcuts import render
from django.db.models import Avg
from django.db.models import Avg
from datetime import datetime, timedelta


from django.shortcuts import render
from django.db.models import Avg
from django.db.models import Sum


def safe_numeric_sums(queryset, fields):
    totals = {f'sum_{field}': 0 for field in fields}
    for row in queryset.values(*fields):
        for field in fields:
            value = row.get(field)
            if value in (None, ''):
                continue
            try:
                totals[f'sum_{field}'] += int(float(value))
            except (TypeError, ValueError):
                continue
    return totals


def safe_numeric_averages(queryset, field_map):
    totals = {output_key: 0.0 for output_key in field_map}
    counts = {output_key: 0 for output_key in field_map}

    for row in queryset.values(*field_map.values()):
        for output_key, field in field_map.items():
            value = row.get(field)
            if value in (None, ''):
                continue
            try:
                totals[output_key] += float(value)
                counts[output_key] += 1
            except (TypeError, ValueError):
                continue

    return {
        output_key: (totals[output_key] / counts[output_key] if counts[output_key] else None)
        for output_key in field_map
    }


# Create your views here.
@login_required(login_url='/')
def view_district(request):
    dis=district.objects.all().order_by('district_name')
    context={
        'dis':dis,
    }
    return render(request,'owner/district_user.html',context)

def view_user(request,district_user):
    user_data=district.objects.get(district_name=district_user)
    dis=district.objects.values('district_name').distinct().order_by('district_name')
    context={
        'dis':dis,
        'user_data':user_data,
    }
    return render(request,'owner/user_information.html',context)


from django.db.models import Case, When, Value, IntegerField
from django.core.mail import send_mail
from login.models import User

@login_required(login_url='/')
def user_management(request, district_user):
    admin_data = User.objects.filter(user_district=district_user, is_admin=True)
    
    if request.method == 'POST':
        user_district = request.POST.get('user_district')
        salutation = request.POST.get('salutation')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        email_id = request.POST.get('email_id')
        mobile_number = request.POST.get('mobile_number')

        if User.objects.filter(mobile_number=mobile_number).exists():
            return render(request, 'owner/admin_info.html', {
                'error_message': 'User with this Mobile Number already exists.',
                'district_user': district_user,
            })

        # Generate a unique user_id using only the first_name
        base_user_id = f'{first_name}'
        last_admin = User.objects.filter(user_district=district_user, is_admin=True).order_by('-user_id').first()
        
        if last_admin:
            # Split the last user_id to get the number part, then increment it
            try:
                last_user_id_number = int(last_admin.user_id.split('@')[-1])
            except ValueError:
                last_user_id_number = 0
            new_user_id_number = last_user_id_number + 1
        else:
            new_user_id_number = 1

        user_id = f'{base_user_id}@{new_user_id_number}'
        
        # Check for uniqueness in user_id and adjust if necessary
        while User.objects.filter(user_id=user_id).exists():
            new_user_id_number += 1
            user_id = f'{base_user_id}@{new_user_id_number}'

        # Create the admin user with the generated unique user_id
        admin = User(
            user_id=user_id,
            user_district=district_user,
            salutation=salutation,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email_id=email_id,
            mobile_number=mobile_number,
            is_superuser=False,
            is_admin=True,
            is_active=True,
            is_staff=True,
            is_user=True  # Adjust these fields as per your User model
        )

        # Generate password in the same format as user_id
        password = f'{first_name}@{new_user_id_number}'
        admin.set_password(password)
        admin.generated_pass = password
        
        admin.save()

        # admin_value = admin_user.objects.create(
        #     user=admin,
        #     first_name=first_name,
        #     last_name=last_name,
        #     email=email_id,
        #     mobile_number=mobile_number,
        #     district=district_user,
        #     is_admin=True,
        #     is_active=True,
        # )
        # admin_value.save()

    user = district.objects.get(district_name=district_user)
    context = {
        'admin_data': admin_data,    
        'user': user,
        'role': 'District Admin',
        'district_user': district_user,
    } 

    return render(request, 'owner/admin_info.html', context)



# def user_management(request, district_user):
    # admin_data = User.objects.filter(user_district=district_user, is_admin=True)
    
    # if request.method == 'POST':
    #     user_district = request.POST.get('user_district')
    #     salutation = request.POST.get('salutation')
    #     first_name = request.POST.get('first_name')
    #     middle_name = request.POST.get('middle_name')
    #     last_name = request.POST.get('last_name')
    #     email_id = request.POST.get('email_id')
    #     mobile_number = request.POST.get('mobile_number')

    #     if User.objects.filter(mobile_number=mobile_number).exists():
    #         return render(request, 'owner/admin_info.html', {
    #             'error_message': 'User with this Mobile Number already exists.',
    #             'district_user': district_user,
    #         })

    #     # Generate a unique user_id using only the first_name
    #     base_user_id = f'{first_name}'
    #     last_admin = User.objects.filter(user_district=district_user, is_admin=True).order_by('-user_id').first()
        
    #     if last_admin:
    #         # Split the last user_id to get the number part, then increment it
    #         try:
    #             last_user_id_number = int(last_admin.user_id.split('@')[-1])
    #         except ValueError:
    #             last_user_id_number = 0
    #         new_user_id_number = last_user_id_number + 1
    #     else:
    #         new_user_id_number = 1

    #     user_id = f'{base_user_id}@{new_user_id_number:02}'

    #     # Check for uniqueness in user_id and adjust if necessary
    #     while User.objects.filter(user_id=user_id).exists():
    #         new_user_id_number += 1
    #         user_id = f'{base_user_id}@{new_user_id_number:02}'

    #     # Create the admin user with the generated unique user_id
    #     admin = User(
    #         user_id=user_id,
    #         user_district=district_user,
    #         salutation=salutation,
    #         first_name=first_name,
    #         middle_name=middle_name,
    #         last_name=last_name,
    #         email_id=email_id,
    #         mobile_number=mobile_number,
    #         is_superuser=False,
    #         is_admin=True,
    #         is_active=True,
    #         is_staff=True,
    #         is_user=True  # Adjust these fields as per your User model
    #     )

    #     password = f'{first_name}@{new_user_id_number:02}'
    #     admin.set_password(password)
    #     admin.generated_pass = password
        
    #     admin.save()

    #     admin_value = admin_user.objects.create(
    #         user=admin,
    #         first_name=first_name,
    #         last_name=last_name,
    #         email=email_id,
    #         mobile_number=mobile_number,
    #         district=district_user,
    #         is_admin=True,
    #         is_active=True,
    #     )
    #     admin_value.save()

    # user = district.objects.get(district_name=district_user)
    # context = {
    #     'admin_data': admin_data,    
    #     'user': user,
    #     'role': 'District Admin',
    #     'district_user': district_user,
    # } 

    # return render(request, 'owner/admin_info.html', context)






@login_required(login_url='/')
def admin_district(request):
    dis=district.objects.all().order_by('district_name')
    context={
        'dis':dis,
    }
    return render(request,'owner/admin_district.html',context)


@login_required(login_url='/')
def admin_user(request,district_name):
    admin = User.objects.filter(is_admin=True,user_district=district_name)

    context={
    'admin_data':admin,
    'district_name':district_name,
    }
    return render(request, 'owner/admin_user.html', context)



@login_required(login_url='/')
def edit_admin(request,id):
    data = User.objects.get(id=id)

    if request.method == 'POST':
        data.first_name = request.POST.get('first_name')
        data.last_name = request.POST.get('last_name')
        data.email_id = request.POST.get('email_id')
        data.save()

        name1=data.user_district
    
        url=reverse('admin_user',args=[name1])
        return redirect(url)


    context={
    'data':data,
    }
    return render(request, 'owner/edit_admin.html', context)

@login_required(login_url='/')
def delete_admin(request,id):
    data = User.objects.get(id=id)

    data.delete()

    name1=data.user_district
    
    url=reverse('admin_user',args=[name1])
    return redirect(url)



@login_required(login_url='/')
def display_weeks(request):
    week = standard_weeks.objects.all().annotate(
            standard_number_int=Cast('standard_number', IntegerField())
        ).order_by('standard_number_int')

    # week = standard_weeks.objects.all().order_by('standard_number')

    context={
    'week':week,
    }
    return render(request, 'owner/display_weeks.html', context)


# monthly report for admin

@login_required(login_url='/login/')
def monthly_report_month(request,district_name):
    data = pest_incidence_data.objects.filter(district=district_name)
    unique_months = data.values_list('month', flat=True).distinct().order_by('month')
    print('ffffffffffffffff',data)
    print('unique_months',unique_months)
    for i in unique_months:
        print('nnnnnnnnnnn',i)
    context={
    'unique_months':unique_months,
    'district_name':district_name,
    }
    return render(request,'owner/monthly_report_month.html',context)




@login_required(login_url='/login/')
def monthly_progress_report(request, district_name, month):
    
    financial_years = Financial_Year.objects.order_by('-id').first()
    selected_fin_year = request.session.get(
        'financial_year',
        financial_years.financial_year if financial_years else '2024-2025'
    )

    # FY -> date range (01-Apr to 31-Mar)
    start_year, end_year = map(int, selected_fin_year.split('-'))
    start_date = date(start_year, 4, 1)     # 01-Apr
    end_date   = date(end_year, 3, 31)      # 31-Mar
    # print('FY:', selected_fin_year, 'Range:', start_date, '->', end_date)

    # ---------- 2) Month -> integer ----------
    target_month = datetime.strptime(month, "%B").month

    # ---------- 3) Standard weeks (month based) ----------
    standard_weeks_data = standard_weeks.objects.filter(month_data=month)
    
    print('standard_weeks_data',standard_weeks_data)

    # Initialize a dictionary to hold week-wise averages
    # ---------- 4) Week-wise pest averages (FY + month + district) ----------
    weekwise_averages = {}
    for standard in standard_weeks_data:
        # NOTE: Agar aapke pest_incidence_data me `week` numeric field hai,
        # to usko match kar rahe hain + district + FY range + month
        pest_data = (
            pest_incidence_data.objects
            .filter(
                district=district_name,
                week=standard.standard_number,
                date_field__range=(start_date, end_date),   # FY filter
                date_field__month=target_month              # Month filter
            )
        )

        averages = pest_data.aggregate(
            avg_jassid_irm=Avg('jassid_irm_average'),
            avg_jassid_nonirm=Avg('jassid_nonirm_average'),
            avg_whitefly_irm=Avg('whitefly_irm_average'),
            avg_whitefly_nonirm=Avg('whitefly_nonirm_average'),
            avg_thrips_irm=Avg('thrips_irm_average'),
            avg_thrips_nonirm=Avg('thrips_nonirm_average'),
            avg_flowers_irm=Avg('flowers_irm_average'),
            avg_flowers_nonirm=Avg('flowers_nonirm_average'),
            avg_green_irm=Avg('green_irm_average'),
            avg_green_nonirm=Avg('green_nonirm_average'),
            avg_locule_irm=Avg('locule_irm_average'),
            avg_locule_nonirm=Avg('locule_nonirm_average'),
            avg_open_ball_irm=Avg('open_ball_irm_average'),
            avg_open_ball_nonirm=Avg('open_ball_nonirm_average'),
            avg_pheromone_irm=Avg('pheromone_irm_average'),
            avg_pheromone_nonirm=Avg('pheromone_nonirm_average'),
            avg_incidence_irm=Avg('incidence_irm_average'),
            avg_incidence_nonirm=Avg('incidence_nonirm_average'),
            avg_locular_damage_irm=Avg('locular_damage_irm_average'),
            avg_locular_damage_nonirm=Avg('locular_damage_nonirm_average')
        )

        # Key: (standard_number, standard_week)
        weekwise_averages[(standard.standard_number, standard.standard_week)] = averages

    # ---------- 5) Monthly physical progress (FY + month + district) ----------
    progress_data = monthly_physical_progress.objects.filter(
        district=district_name,
        date_field__range=(start_date, end_date),  # FY
        date_field__month=target_month,            # Month
    )

    progress_count = safe_numeric_averages(progress_data, {
        'avg_pheromone_traps': 'pheromone_traps',
        'avg_splat': 'splat',
        'avg_pb_rope': 'pb_rope',
        'avg_neem_insecticides': 'neem_insecticides',
        'avg_flonicamid': 'flonicamid',
        'avg_trichocards': 'trichocards',
        'avg_quinalphos': 'quinalphos',
        'avg_chlorpyriphos': 'chlorpyriphos',
        'avg_profenophos': 'profenophos',
    })

    # ---------- 6) Extension activities carried out (FY + month + district) ----------
    activities_data = extension_activities_carried_out.objects.filter(
        district=district_name,
        date_field__range=(start_date, end_date),  # FY
        date_field__month=target_month,            # Month
    )

    extension_activity_sum_fields = [
        'popular_artical_number', 'popular_artical_beneficiary_male', 'popular_artical_beneficiary_female',
        'press_release_number', 'press_release_beneficiary_male', 'press_release_beneficiary_female',
        'extension_material_booklet_number', 'extension_material_booklet_beneficiary_male', 'extension_material_booklet_beneficiary_female',
        'extension_material_leaflet_number', 'extension_material_leaflet_beneficiary_male', 'extension_material_leaflet_beneficiary_female',
        'extension_material_pamphlet_number', 'extension_material_pamphlet_beneficiary_male', 'extension_material_pamphlet_beneficiary_female',
        'extension_material_poster_number', 'extension_material_poster_beneficiary_male', 'extension_material_poster_beneficiary_female',
        'literature_distributed_booklet_number', 'literature_distributed_booklet_beneficiary_male', 'literature_distributed_booklet_beneficiary_female',
        'literature_distributed_leaflet_number', 'literature_distributed_leaflet_beneficiary_male', 'literature_distributed_leaflet_beneficiary_female',
        'literature_distributed_pamphlet_number', 'literature_distributed_pamphlet_beneficiary_male', 'literature_distributed_pamphlet_beneficiary_female',
        'voice_messages_number', 'voice_messages_beneficiary_male', 'voice_messages_beneficiary_female',
        'field_visit_number', 'field_visit_beneficiary_male', 'field_visit_beneficiary_female',
        'farmer_mela_number', 'farmer_mela_beneficiary_male', 'farmer_mela_beneficiary_female',
        'exhibition_arranged_number', 'exhibition_arranged_beneficiary_male', 'exhibition_arranged_beneficiary_female',
        'farmer_training_number', 'farmer_training_beneficiary_male', 'farmer_training_beneficiary_female',
        'training_number', 'training_beneficiary_male', 'training_beneficiary_female',
        'tv_show_number', 'tv_show_beneficiary_male', 'tv_show_beneficiary_female',
        'radio_talks_numbers', 'radio_talks_beneficiary_male', 'radio_talks_beneficiary_female',
        'sensitization_workshop_number', 'sensitization_workshop_beneficiary_male', 'sensitization_workshop_beneficiary_female',
        'farmers_queries_number', 'farmers_queries_beneficiary_male', 'farmers_queries_beneficiary_female',
        'lectures_delivered_number', 'lectures_delivered_beneficiary_male', 'lectures_delivered_beneficiary_female',
        'news_clips_number', 'news_clips_beneficiary_male', 'news_clips_beneficiary_female',
        'visit_of_farmers_numbers', 'visit_of_farmers_beneficiary_male', 'visit_of_farmers_beneficiary_female',
    ]
    activities_sums = safe_numeric_sums(activities_data, extension_activity_sum_fields)

    # ---------- 7) Photographs (FY + month + district) ----------
    photograph_data = RepresentedPhotograph.objects.filter(
        district=district_name,
        date_field__range=(start_date, end_date),  # FY
        date_field__month=target_month,            # Month
    )

    # ---------- 8) Assessment (FY + month + district) ----------
    assesment_data = AssessmentSeason.objects.filter(
        district=district_name,
        date_field__range=(start_date, end_date),  # FY
        date_field__month=target_month,            # Month
    )

    context = {
        'weekwise_averages': weekwise_averages,
        'month': month,
        'progress_count': progress_count,
        'activities_sums': activities_sums,
        'photograph_data': photograph_data,
        'assesment_data': assesment_data,
        'district_name': district_name,
        'selected_fin_year': selected_fin_year,
        'fy_start_date': start_date,
        'fy_end_date': end_date,
    }

    return render(request, 'owner/monthly_progress_report.html', context)
   
   

# @login_required(login_url='/login/')
# def monthly_progress_report(request, district_name, month):
#     # Filter standard_weeks by the specified month and year
#     standard_weeks_data = standard_weeks.objects.filter(month_data=month)

#     print('standard_weeks_data',standard_weeks_data)

#     # Initialize a dictionary to hold week-wise averages
#     weekwise_averages = {}

#     for standard in standard_weeks_data:
#         # Filter pest incidence data where week matches the standard number
#         pest_data = pest_incidence_data.objects.filter(week=standard.standard_number,district=district_name)

#         print('pest_data',pest_data)

#         # Calculate the averages
#         averages = pest_data.aggregate(
#             avg_jassid_irm=Avg('jassid_irm_average'),
#             avg_jassid_nonirm=Avg('jassid_nonirm_average'),
#             avg_whitefly_irm=Avg('whitefly_irm_average'),
#             avg_whitefly_nonirm=Avg('whitefly_nonirm_average'),
#             avg_thrips_irm=Avg('thrips_irm_average'),
#             avg_thrips_nonirm=Avg('thrips_nonirm_average'),
#             avg_flowers_irm=Avg('flowers_irm_average'),
#             avg_flowers_nonirm=Avg('flowers_nonirm_average'),
#             avg_green_irm=Avg('green_irm_average'),
#             avg_green_nonirm=Avg('green_nonirm_average'),
#             avg_locule_irm=Avg('locule_irm_average'),
#             avg_locule_nonirm=Avg('locule_nonirm_average'),
#             avg_open_ball_irm=Avg('open_ball_irm_average'),
#             avg_open_ball_nonirm= Avg('open_ball_nonirm_average'),
#             avg_pheromone_irm=Avg('pheromone_irm_average'),
#             avg_pheromone_nonirm=Avg('pheromone_nonirm_average'),
#             avg_incidence_irm=Avg('incidence_irm_average'),
#             avg_incidence_nonirm=Avg('incidence_nonirm_average'),
#             avg_locular_damage_irm=Avg('locular_damage_irm_average'),
#             avg_locular_damage_nonirm=Avg('locular_damage_nonirm_average')

#         )

#         # Store in the dictionary
#         # weekwise_averages[standard.standard_week] = averages
#         weekwise_averages[(standard.standard_number, standard.standard_week)] = averages

#     # print('weekwise_averages',weekwise_averages)



#     # For B. Physical progress average

#     target_month = datetime.strptime(month, "%B").month
#     print('target_month',target_month)

#     progress_data = monthly_physical_progress.objects.filter(
#         district=district_name,
#         date_field__month=target_month
#     )

#     print('progress_data',progress_data)

#     # Calculate the averages
#     progress_count = progress_data.aggregate(
#         avg_pheromone_traps=Avg('pheromone_traps'),
#         avg_splat=Avg('splat'),
#         avg_pb_rope=Avg('pb_rope'),
#         avg_neem_insecticides=Avg('neem_insecticides'),
#         avg_flonicamid=Avg('flonicamid'),
#         avg_trichocards=Avg('trichocards'),
#         avg_quinalphos=Avg('quinalphos'),
#         avg_chlorpyriphos=Avg('chlorpyriphos'),
#         avg_profenophos=Avg('profenophos'),
#     )


#     # For Extension activities carried out average

#     activities_data = extension_activities_carried_out.objects.filter(
#         district=district_name,
#         date_field__month=target_month,
#     )


#     # Calculate the averages for the specified fields
#     activities_sums = activities_data.aggregate(
#         sum_popular_artical_number=Sum(ExpressionWrapper(F('popular_artical_number'), output_field=IntegerField())),
#         sum_popular_artical_beneficiary_male=Sum(ExpressionWrapper(F('popular_artical_beneficiary_male'), output_field=IntegerField())),
#         sum_popular_artical_beneficiary_female=Sum(ExpressionWrapper(F('popular_artical_beneficiary_female'), output_field=IntegerField())),
#         sum_press_release_number=Sum(ExpressionWrapper(F('press_release_number'), output_field=IntegerField())),
#         sum_press_release_beneficiary_male=Sum(ExpressionWrapper(F('press_release_beneficiary_male'), output_field=IntegerField())),
#         sum_press_release_beneficiary_female=Sum(ExpressionWrapper(F('press_release_beneficiary_female'), output_field=IntegerField())),
#         sum_extension_material_booklet_number=Sum(ExpressionWrapper(F('extension_material_booklet_number'), output_field=IntegerField())),
#         sum_extension_material_booklet_beneficiary_male=Sum(ExpressionWrapper(F('extension_material_booklet_beneficiary_male'), output_field=IntegerField())),
#         sum_extension_material_booklet_beneficiary_female=Sum(ExpressionWrapper(F('extension_material_booklet_beneficiary_female'), output_field=IntegerField())),
#         sum_extension_material_leaflet_number=Sum(ExpressionWrapper(F('extension_material_leaflet_number'), output_field=IntegerField())),
#         sum_extension_material_leaflet_beneficiary_male=Sum(ExpressionWrapper(F('extension_material_leaflet_beneficiary_male'), output_field=IntegerField())),
#         sum_extension_material_leaflet_beneficiary_female=Sum(ExpressionWrapper(F('extension_material_leaflet_beneficiary_female'), output_field=IntegerField())),
#         sum_extension_material_pamphlet_number=Sum(ExpressionWrapper(F('extension_material_pamphlet_number'), output_field=IntegerField())),
#         sum_extension_material_pamphlet_beneficiary_male=Sum(ExpressionWrapper(F('extension_material_pamphlet_beneficiary_male'), output_field=IntegerField())),
#         sum_extension_material_pamphlet_beneficiary_female=Sum(ExpressionWrapper(F('extension_material_pamphlet_beneficiary_female'), output_field=IntegerField())),
#         sum_extension_material_poster_number=Sum(ExpressionWrapper(F('extension_material_poster_number'), output_field=IntegerField())),
#         sum_extension_material_poster_beneficiary_male=Sum(ExpressionWrapper(F('extension_material_poster_beneficiary_male'), output_field=IntegerField())),
#         sum_extension_material_poster_beneficiary_female=Sum(ExpressionWrapper(F('extension_material_poster_beneficiary_female'), output_field=IntegerField())),
#         sum_literature_distributed_booklet_number=Sum(ExpressionWrapper(F('literature_distributed_booklet_number'), output_field=IntegerField())),
#         sum_literature_distributed_booklet_beneficiary_male=Sum(ExpressionWrapper(F('literature_distributed_booklet_beneficiary_male'), output_field=IntegerField())),
#         sum_literature_distributed_booklet_beneficiary_female=Sum(ExpressionWrapper(F('literature_distributed_booklet_beneficiary_female'), output_field=IntegerField())),
#         sum_literature_distributed_leaflet_number=Sum(ExpressionWrapper(F('literature_distributed_leaflet_number'), output_field=IntegerField())),
#         sum_literature_distributed_leaflet_beneficiary_male=Sum(ExpressionWrapper(F('literature_distributed_leaflet_beneficiary_male'), output_field=IntegerField())),
#         sum_literature_distributed_leaflet_beneficiary_female=Sum(ExpressionWrapper(F('literature_distributed_leaflet_beneficiary_female'), output_field=IntegerField())),
#         sum_literature_distributed_pamphlet_number=Sum(ExpressionWrapper(F('literature_distributed_pamphlet_number'), output_field=IntegerField())),
#         sum_literature_distributed_pamphlet_beneficiary_male=Sum(ExpressionWrapper(F('literature_distributed_pamphlet_beneficiary_male'), output_field=IntegerField())),
#         sum_literature_distributed_pamphlet_beneficiary_female=Sum(ExpressionWrapper(F('literature_distributed_pamphlet_beneficiary_female'), output_field=IntegerField())),
#         sum_voice_messages_number=Sum(ExpressionWrapper(F('voice_messages_number'), output_field=IntegerField())),
#         sum_voice_messages_beneficiary_male=Sum(ExpressionWrapper(F('voice_messages_beneficiary_male'), output_field=IntegerField())),
#         sum_voice_messages_beneficiary_female=Sum(ExpressionWrapper(F('voice_messages_beneficiary_female'), output_field=IntegerField())),
#         sum_field_visit_number=Sum(ExpressionWrapper(F('field_visit_number'), output_field=IntegerField())),
#         sum_field_visit_beneficiary_male=Sum(ExpressionWrapper(F('field_visit_beneficiary_male'), output_field=IntegerField())),
#         sum_field_visit_beneficiary_female=Sum(ExpressionWrapper(F('field_visit_beneficiary_female'), output_field=IntegerField())),
#         sum_farmer_mela_number=Sum(ExpressionWrapper(F('farmer_mela_number'), output_field=IntegerField())),
#         sum_farmer_mela_beneficiary_male=Sum(ExpressionWrapper(F('farmer_mela_beneficiary_male'), output_field=IntegerField())),
#         sum_farmer_mela_beneficiary_female=Sum(ExpressionWrapper(F('farmer_mela_beneficiary_female'), output_field=IntegerField())),
#         sum_exhibition_arranged_number=Sum(ExpressionWrapper(F('exhibition_arranged_number'), output_field=IntegerField())),
#         sum_exhibition_arranged_beneficiary_male=Sum(ExpressionWrapper(F('exhibition_arranged_beneficiary_male'), output_field=IntegerField())),
#         sum_exhibition_arranged_beneficiary_female=Sum(ExpressionWrapper(F('exhibition_arranged_beneficiary_female'), output_field=IntegerField())),
#         sum_farmer_training_number=Sum(ExpressionWrapper(F('farmer_training_number'), output_field=IntegerField())),
#         sum_farmer_training_beneficiary_male=Sum(ExpressionWrapper(F('farmer_training_beneficiary_male'), output_field=IntegerField())),
#         sum_farmer_training_beneficiary_female=Sum(ExpressionWrapper(F('farmer_training_beneficiary_female'), output_field=IntegerField())),
#         sum_training_number=Sum(ExpressionWrapper(F('training_number'), output_field=IntegerField())),
#         sum_training_beneficiary_male=Sum(ExpressionWrapper(F('training_beneficiary_male'), output_field=IntegerField())),
#         sum_training_beneficiary_female=Sum(ExpressionWrapper(F('training_beneficiary_female'), output_field=IntegerField())),
#         sum_tv_show_number=Sum(ExpressionWrapper(F('tv_show_number'), output_field=IntegerField())),
#         sum_tv_show_beneficiary_male=Sum(ExpressionWrapper(F('tv_show_beneficiary_male'), output_field=IntegerField())),
#         sum_tv_show_beneficiary_female=Sum(ExpressionWrapper(F('tv_show_beneficiary_female'), output_field=IntegerField())),
#         sum_radio_talks_numbers=Sum(ExpressionWrapper(F('radio_talks_numbers'), output_field=IntegerField())),
#         sum_radio_talks_beneficiary_male=Sum(ExpressionWrapper(F('radio_talks_beneficiary_male'), output_field=IntegerField())),
#         sum_radio_talks_beneficiary_female=Sum(ExpressionWrapper(F('radio_talks_beneficiary_female'), output_field=IntegerField())),
#         sum_sensitization_workshop_number=Sum(ExpressionWrapper(F('sensitization_workshop_number'), output_field=IntegerField())),
#         sum_sensitization_workshop_beneficiary_male=Sum(ExpressionWrapper(F('sensitization_workshop_beneficiary_male'), output_field=IntegerField())),
#         sum_sensitization_workshop_beneficiary_female=Sum(ExpressionWrapper(F('sensitization_workshop_beneficiary_female'), output_field=IntegerField())),
#         sum_farmers_queries_number=Sum(ExpressionWrapper(F('farmers_queries_number'), output_field=IntegerField())),
#         sum_farmers_queries_beneficiary_male=Sum(ExpressionWrapper(F('farmers_queries_beneficiary_male'), output_field=IntegerField())),
#         sum_farmers_queries_beneficiary_female=Sum(ExpressionWrapper(F('farmers_queries_beneficiary_female'), output_field=IntegerField())),
#         sum_lectures_delivered_number=Sum(ExpressionWrapper(F('lectures_delivered_number'), output_field=IntegerField())),
#         sum_lectures_delivered_beneficiary_male=Sum(ExpressionWrapper(F('lectures_delivered_beneficiary_male'), output_field=IntegerField())),
#         sum_lectures_delivered_beneficiary_female=Sum(ExpressionWrapper(F('lectures_delivered_beneficiary_female'), output_field=IntegerField())),
#         sum_news_clips_number=Sum(ExpressionWrapper(F('news_clips_number'), output_field=IntegerField())),
#         sum_news_clips_beneficiary_male=Sum(ExpressionWrapper(F('news_clips_beneficiary_male'), output_field=IntegerField())),
#         sum_news_clips_beneficiary_female=Sum(ExpressionWrapper(F('news_clips_beneficiary_female'), output_field=IntegerField())),
#         sum_visit_of_farmers_numbers=Sum(ExpressionWrapper(F('visit_of_farmers_numbers'), output_field=IntegerField())),
#         sum_visit_of_farmers_beneficiary_male=Sum(ExpressionWrapper(F('visit_of_farmers_beneficiary_male'), output_field=IntegerField())),
#         sum_visit_of_farmers_beneficiary_female=Sum(ExpressionWrapper(F('visit_of_farmers_beneficiary_female'), output_field=IntegerField())),
#     )


#     photograph_data = RepresentedPhotograph.objects.filter(
#         district=district_name,
#         date_field__month=target_month,
#     )

#     print('photograph_data',photograph_data)

#     assesment_data = AssessmentSeason.objects.filter(
#         district=district_name,
#         date_field__month=target_month,
#     )

#     print('assesment_data',assesment_data)

#     print('activities_sums',activities_sums)
    
#     context = {
#         'weekwise_averages': weekwise_averages,
#         'month': month,
#         'progress_count': progress_count,
#         'activities_sums':activities_sums,
#         'photograph_data':photograph_data,
#         'assesment_data':assesment_data,
#         'district_name':district_name,
       
#     }
#     return render(request, 'owner/monthly_progress_report.html', context)
    




# API FOR MONTHLY PROGRESS REPORT
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg
from .models import pest_incidence_data, monthly_physical_progress
from .serializers import PestIncidenceDataSerializer, MonthlyPhysicalProgressSerializer

@api_view(['GET'])
def monthly_progress_report_api(request, district_name, month):
    print('district_name', district_name)
    print('month', month)

    # Filter data for each week
    week1 = pest_incidence_data.objects.filter(district=district_name, month=month, week='Week 1')
    week2 = pest_incidence_data.objects.filter(district=district_name, month=month, week='Week 2')
    week3 = pest_incidence_data.objects.filter(district=district_name, month=month, week='Week 3')
    week4 = pest_incidence_data.objects.filter(district=district_name, month=month, week='Week 4')

    # Function to calculate averages
    def get_averages(queryset):
        return {
            'avg_jassid_irm': queryset.aggregate(Avg('jassid_irm_average'))['jassid_irm_average__avg'],
            'avg_jassid_nonirm': queryset.aggregate(Avg('jassid_nonirm_average'))['jassid_nonirm_average__avg'],
            'avg_whitefly_irm': queryset.aggregate(Avg('whitefly_irm_average'))['whitefly_irm_average__avg'],
            'avg_whitefly_nonirm': queryset.aggregate(Avg('whitefly_nonirm_average'))['whitefly_nonirm_average__avg'],
            'thrips_irm_average': queryset.aggregate(Avg('thrips_irm_average'))['thrips_irm_average__avg'],
            'thrips_nonirm_average': queryset.aggregate(Avg('thrips_nonirm_average'))['thrips_nonirm_average__avg'],
            'flowers_irm_average': queryset.aggregate(Avg('flowers_irm_average'))['flowers_irm_average__avg'],
            'flowers_nonirm_average': queryset.aggregate(Avg('flowers_nonirm_average'))['flowers_nonirm_average__avg'],
            'green_irm_average': queryset.aggregate(Avg('green_irm_average'))['green_irm_average__avg'],
            'green_nonirm_average': queryset.aggregate(Avg('green_nonirm_average'))['green_nonirm_average__avg'],
            'locule_irm_average': queryset.aggregate(Avg('locule_irm_average'))['locule_irm_average__avg'],
            'locule_nonirm_average': queryset.aggregate(Avg('locule_nonirm_average'))['locule_nonirm_average__avg'],
            'open_ball_irm_average': queryset.aggregate(Avg('open_ball_irm_average'))['open_ball_irm_average__avg'],
            'open_ball_nonirm_average': queryset.aggregate(Avg('open_ball_nonirm_average'))['open_ball_nonirm_average__avg'],
            'pheromone_irm_average': queryset.aggregate(Avg('pheromone_irm_average'))['pheromone_irm_average__avg'],
            'pheromone_nonirm_average': queryset.aggregate(Avg('pheromone_nonirm_average'))['pheromone_nonirm_average__avg'],
            'incidence_irm_average': queryset.aggregate(Avg('incidence_irm_average'))['incidence_irm_average__avg'],
            'incidence_nonirm_average': queryset.aggregate(Avg('incidence_nonirm_average'))['incidence_nonirm_average__avg'],
        }

    # Calculate averages for each week
    week1_averages = get_averages(week1)
    week2_averages = get_averages(week2)
    week3_averages = get_averages(week3)
    week4_averages = get_averages(week4)

    # for physical progress report
    progress_count = monthly_physical_progress.objects.filter(district=district_name, month=month).last()
    progress_count_data = MonthlyPhysicalProgressSerializer(progress_count).data if progress_count else None
    print('progress_count', progress_count, progress_count.pheromone_traps if progress_count else None)

    # Combine all averages into context
    context = {
        'month': month,
        'week1_averages': week1_averages,
        'week2_averages': week2_averages,
        'week3_averages': week3_averages,
        'week4_averages': week4_averages,
        'progress_count': progress_count_data,
    }

    return Response(context)

@login_required(login_url='/')
def basic_district(request):
    dis=district.objects.all().order_by('district_name')
    context={
        'dis':dis,
    }
    return render(request,'owner/basic_district.html',context)


# @login_required(login_url='/')
# def basic_servery_report(request,district_name):
#     data = basic_servey_info.objects.filter(district=district_name)
#     print('data',data)

#     context={
#     'data':data,
#     'district_name':district_name,
#     }

#     return render(request,'owner/basic_servery_report.html',context)


from datetime import date

@login_required(login_url='/')
def basic_servery_report(request, district_name):
    # --- FY from session (fallback latest or default) ---
    fy_obj = Financial_Year.objects.order_by('-id').first()
    selected_fin_year = request.session.get(
        'financial_year',
        fy_obj.financial_year if fy_obj else '2024-2025'
    )

    # Convert FY -> date range
    start_year, end_year = map(int, selected_fin_year.split('-'))
    start_date = date(start_year, 4, 1)   # 01-Apr
    end_date   = date(end_year, 3, 31)    # 31-Mar

    # --- Query: district + servey_date in FY ---
    data = (
        basic_servey_info.objects
        .filter(district=district_name)
        .exclude(servey_date__isnull=True)
        .filter(servey_date__range=(start_date, end_date))
        .order_by('-servey_date', '-id')
    )

    context = {
        'data': data,
        'district_name': district_name,
        'selected_fin_year': selected_fin_year,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'owner/basic_servery_report.html', context)



from django.contrib import messages
from django.core.exceptions import ValidationError
from datetime import datetime

def optional_int(value):
    if value in (None, ''):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

def edit_servey_report(request,district_name, id):
    data = basic_servey_info.objects.filter(id=id).first()
    if not data:
        messages.error(request, f'Survey report #{id} was not found.')
        return redirect(reverse('basic_servery_report', args=[district_name]))
    
    if request.method == 'POST':
        # Update the object manually from the POST data
        data.IRM = True if request.POST.get('IRM') == 'IRM' else False
        data.user_id = request.POST.get('user_id')
        data.name = request.POST.get('name')
        data.category = request.POST.get('category')
        data.gender = request.POST.get('gender')
        data.village = request.POST.get('village')
        data.taluka = request.POST.get('taluka')
        data.district = request.POST.get('district')
        data.mobile_number = request.POST.get('mobile_number')
        
        # Handle date_of_sowing to prevent errors with invalid or empty date inputs
        date_of_sowing_str = request.POST.get('date_of_sowing')
        if date_of_sowing_str:
            try:
                data.date_of_sowing = datetime.strptime(date_of_sowing_str, '%Y-%m-%d').date()
            except ValueError:
                # Handle invalid date format
                return render(request, 'owner/edit_servey_report.html', {'data': data, 'error': 'Invalid date format, please use YYYY-MM-DD'})

        data.row_distance = request.POST.get('row_distance')
        data.plant_distance = request.POST.get('plant_distance')
        data.cotton_variety = request.POST.get('cotton_variety')
        data.previous_year_crop_grown = request.POST.get('previous_year_crop_grown')
        data.causes = True if request.POST.get('causes') == 'irrigation' else False
        data.last_year_crop_extended = True if request.POST.get('last_year_crop_extended') == 'Yes' else False
        data.soil_type = request.POST.get('soil_type')
        data.crop_rotation_followed = True if request.POST.get('crop_rotation_followed') == 'Yes' else False
        data.advisory_received_from = request.POST.get('advisory_received_from')
        data.total_farmers_ecommunication = optional_int(request.POST.get('total_farmers_ecommunication'))
        servey_date_str = request.POST.get('servey_date')
        if servey_date_str:
            try:
                data.servey_date = datetime.strptime(servey_date_str, '%Y-%m-%d').date()
            except ValueError:
                return render(request, 'owner/edit_servey_report.html', {'data': data, 'error': 'Invalid survey date format, please use YYYY-MM-DD'})
        else:
            data.servey_date = None
        data.year = request.POST.get('year')
        data.landarea = request.POST.get('landarea')
        data.aadhar_number = request.POST.get('aadhar_number')

        # Save the updated object to the database
        data.save()
        
        url = reverse('basic_servery_report', args=[district_name])
        return redirect(url)  # Replace 'success_url' with the appropriate URL name after editing
    
    # Render the template with the survey report data
    return render(request, 'owner/edit_servey_report.html', {'data': data})


def delete_servey_report(request,district_name,id):
    data = basic_servey_info.objects.get(id=id)
    data.delete()
    
    url = reverse('basic_servery_report', args=[district_name])
    return redirect(url)



# basic survey for admin

@login_required(login_url='/login/')
def admin_basic_servery(request,district_name):
    # --- FY from session (fallback latest or default) ---
    fy_obj = Financial_Year.objects.order_by('-id').first()
    selected_fin_year = request.session.get(
        'financial_year',
        fy_obj.financial_year if fy_obj else '2024-2025'
    )

    # Convert FY -> date range
    start_year, end_year = map(int, selected_fin_year.split('-'))
    start_date = date(start_year, 4, 1)   # 01-Apr
    end_date   = date(end_year, 3, 31) 
    
    user = request.user
    print('admin_basic_servery',user,user.user_district)
    # data = basic_servey_info.objects.filter(district=user.user_district)
    
    data = (
        basic_servey_info.objects
        .filter(district=user.user_district)
        .exclude(servey_date__isnull=True)
        .filter(servey_date__range=(start_date, end_date))
        .order_by('-servey_date', '-id')
    )
    print('data',data)

    context={
        'data':data,
        'district_name':district_name,
        'selected_fin_year': selected_fin_year,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request,'owner/admin_basic_servery.html',context)




@login_required(login_url='/')
def weekly_district(request):
    dis=district.objects.all().order_by('district_name')
    context={
        'dis':dis,
    }
    return render(request,'owner/weekly_district.html',context)

@login_required(login_url='/')
def pest_weekly_report(request,district_name):
    data = pest_incidence_data.objects.filter(district=district_name)
    print('data',data)

    context={
    'data':data,
    'district_name':district_name,
    }

    return render(request,'owner/pest_weekly_report.html',context)


# pest weekly report for admin

@login_required(login_url='/login/')
def admin_weekly_report(request,district_name):
    user = request.user
    print('admin_basic_servery',user,user.user_district)
    data = pest_incidence_data.objects.filter(district=user.user_district)
    print('data',data)

    context={
    'data':data,
    'district_name':district_name,
    }

    return render(request,'owner/admin_weekly_report.html',context)



@login_required(login_url='/')
def investigator_district(request):
    dis=district.objects.all().order_by('district_name')
    context={
        'dis':dis,
    }
    return render(request,'owner/investigator_district.html',context)

@login_required(login_url='/')
def investigator_details(request,district_name):
    data = investigator_user.objects.filter(district=district_name)
    print('data',data)
    user_data = []

    for i in data:
        try:
            user = User.objects.get(id=i.user_id)
            user_data.append({
                'user_id': user.user_id,
                'generated_pass': user.generated_pass,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email_id,
                'mobile_number': i.mobile_number,  # Assuming this field is in investigator_user
                'address': i.address,  # Assuming this field is in investigator_user
                'id':i.id,
            })
        except User.DoesNotExist:
            pass

    context = {
        'data': user_data,
        'district_name':district_name,
    }
    return render(request,'owner/investigator_details.html',context)


@login_required(login_url='/')
def delete_investigator(request,user_id):
    data = User.objects.get(user_id=user_id)

    data.delete()

    name1=data.user_district
    
    url=reverse('investigator_details',args=[name1])
    return redirect(url)

# monthly report for super admin

@login_required(login_url='/')
def monthly_district(request):
    dis=district.objects.all().order_by('district_name')
    context={
        'dis':dis,
    }
    return render(request,'owner/monthly_district.html',context)


@login_required(login_url='/login/')
def super_monthly_report(request,district_name):
    data = pest_incidence_data.objects.filter(district=district_name)
    unique_months = data.values_list('month', flat=True).distinct().order_by('month')
    print('ffffffffffffffff',data)
    print('unique_months',unique_months)
    for i in unique_months:
        print('nnnnnnnnnnn',i)
    context={
    'unique_months':unique_months,
    'district_name':district_name,
    }
    return render(request,'owner/super_monthly_report.html',context)





# @login_required(login_url='/')
# def super_monthly_progress(request, district_name, month):
#     # Filter standard_weeks by the specified month and year
#     standard_weeks_data = standard_weeks.objects.filter(month_data=month)

#     print('standard_weeks_data',standard_weeks_data)

#     # Initialize a dictionary to hold week-wise averages
#     weekwise_averages = {}

#     for standard in standard_weeks_data:
#         # Filter pest incidence data where week matches the standard number
#         pest_data = pest_incidence_data.objects.filter(week=standard.standard_number,district=district_name)

#         print('pest_data',pest_data)

#         # Calculate the averages
#         averages = pest_data.aggregate(
#             avg_jassid_irm=Avg('jassid_irm_average'),
#             avg_jassid_nonirm=Avg('jassid_nonirm_average'),
#             avg_whitefly_irm=Avg('whitefly_irm_average'),
#             avg_whitefly_nonirm=Avg('whitefly_nonirm_average'),
#             avg_thrips_irm=Avg('thrips_irm_average'),
#             avg_thrips_nonirm=Avg('thrips_nonirm_average'),
#             avg_flowers_irm=Avg('flowers_irm_average'),
#             avg_flowers_nonirm=Avg('flowers_nonirm_average'),
#             avg_green_irm=Avg('green_irm_average'),
#             avg_green_nonirm=Avg('green_nonirm_average'),
#             avg_locule_irm=Avg('locule_irm_average'),
#             avg_locule_nonirm=Avg('locule_nonirm_average'),
#             avg_open_ball_irm=Avg('open_ball_irm_average'),
#             avg_open_ball_nonirm= Avg('open_ball_nonirm_average'),
#             avg_pheromone_irm=Avg('pheromone_irm_average'),
#             avg_pheromone_nonirm=Avg('pheromone_nonirm_average'),
#             avg_incidence_irm=Avg('incidence_irm_average'),
#             avg_incidence_nonirm=Avg('incidence_nonirm_average'),
#             avg_locular_damage_irm=Avg('locular_damage_irm_average'),
#             avg_locular_damage_nonirm=Avg('locular_damage_nonirm_average')

#         )

#         # Store in the dictionary
#         # weekwise_averages[standard.standard_week] = averages
#         weekwise_averages[(standard.standard_number, standard.standard_week)] = averages

#     # print('weekwise_averages',weekwise_averages)



#     # For B. Physical progress average

#     target_month = datetime.strptime(month, "%B").month
#     print('target_month',target_month)

#     progress_data = monthly_physical_progress.objects.filter(
#         district=district_name,
#         date_field__month=target_month
#     )

#     print('progress_data',progress_data)

#     # Calculate the averages
#     progress_count = progress_data.aggregate(
#         avg_pheromone_traps=Avg('pheromone_traps'),
#         avg_splat=Avg('splat'),
#         avg_pb_rope=Avg('pb_rope'),
#         avg_neem_insecticides=Avg('neem_insecticides'),
#         avg_flonicamid=Avg('flonicamid'),
#         avg_trichocards=Avg('trichocards'),
#         avg_quinalphos=Avg('quinalphos'),
#         avg_chlorpyriphos=Avg('chlorpyriphos'),
#         avg_profenophos=Avg('profenophos'),
#     )


#     # For Extension activities carried out average

#     activities_data = extension_activities_carried_out.objects.filter(
#         district=district_name,
#         date_field__month=target_month,
#     )


#     # Calculate the averages for the specified fields
#     activities_sums = activities_data.aggregate(
#         sum_popular_artical_number=Sum(ExpressionWrapper(F('popular_artical_number'), output_field=IntegerField())),
#         sum_popular_artical_beneficiary_male=Sum(ExpressionWrapper(F('popular_artical_beneficiary_male'), output_field=IntegerField())),
#         sum_popular_artical_beneficiary_female=Sum(ExpressionWrapper(F('popular_artical_beneficiary_female'), output_field=IntegerField())),
#         sum_press_release_number=Sum(ExpressionWrapper(F('press_release_number'), output_field=IntegerField())),
#         sum_press_release_beneficiary_male=Sum(ExpressionWrapper(F('press_release_beneficiary_male'), output_field=IntegerField())),
#         sum_press_release_beneficiary_female=Sum(ExpressionWrapper(F('press_release_beneficiary_female'), output_field=IntegerField())),
#         sum_extension_material_booklet_number=Sum(ExpressionWrapper(F('extension_material_booklet_number'), output_field=IntegerField())),
#         sum_extension_material_booklet_beneficiary_male=Sum(ExpressionWrapper(F('extension_material_booklet_beneficiary_male'), output_field=IntegerField())),
#         sum_extension_material_booklet_beneficiary_female=Sum(ExpressionWrapper(F('extension_material_booklet_beneficiary_female'), output_field=IntegerField())),
#         sum_extension_material_leaflet_number=Sum(ExpressionWrapper(F('extension_material_leaflet_number'), output_field=IntegerField())),
#         sum_extension_material_leaflet_beneficiary_male=Sum(ExpressionWrapper(F('extension_material_leaflet_beneficiary_male'), output_field=IntegerField())),
#         sum_extension_material_leaflet_beneficiary_female=Sum(ExpressionWrapper(F('extension_material_leaflet_beneficiary_female'), output_field=IntegerField())),
#         sum_extension_material_pamphlet_number=Sum(ExpressionWrapper(F('extension_material_pamphlet_number'), output_field=IntegerField())),
#         sum_extension_material_pamphlet_beneficiary_male=Sum(ExpressionWrapper(F('extension_material_pamphlet_beneficiary_male'), output_field=IntegerField())),
#         sum_extension_material_pamphlet_beneficiary_female=Sum(ExpressionWrapper(F('extension_material_pamphlet_beneficiary_female'), output_field=IntegerField())),
#         sum_extension_material_poster_number=Sum(ExpressionWrapper(F('extension_material_poster_number'), output_field=IntegerField())),
#         sum_extension_material_poster_beneficiary_male=Sum(ExpressionWrapper(F('extension_material_poster_beneficiary_male'), output_field=IntegerField())),
#         sum_extension_material_poster_beneficiary_female=Sum(ExpressionWrapper(F('extension_material_poster_beneficiary_female'), output_field=IntegerField())),
#         sum_literature_distributed_booklet_number=Sum(ExpressionWrapper(F('literature_distributed_booklet_number'), output_field=IntegerField())),
#         sum_literature_distributed_booklet_beneficiary_male=Sum(ExpressionWrapper(F('literature_distributed_booklet_beneficiary_male'), output_field=IntegerField())),
#         sum_literature_distributed_booklet_beneficiary_female=Sum(ExpressionWrapper(F('literature_distributed_booklet_beneficiary_female'), output_field=IntegerField())),
#         sum_literature_distributed_leaflet_number=Sum(ExpressionWrapper(F('literature_distributed_leaflet_number'), output_field=IntegerField())),
#         sum_literature_distributed_leaflet_beneficiary_male=Sum(ExpressionWrapper(F('literature_distributed_leaflet_beneficiary_male'), output_field=IntegerField())),
#         sum_literature_distributed_leaflet_beneficiary_female=Sum(ExpressionWrapper(F('literature_distributed_leaflet_beneficiary_female'), output_field=IntegerField())),
#         sum_literature_distributed_pamphlet_number=Sum(ExpressionWrapper(F('literature_distributed_pamphlet_number'), output_field=IntegerField())),
#         sum_literature_distributed_pamphlet_beneficiary_male=Sum(ExpressionWrapper(F('literature_distributed_pamphlet_beneficiary_male'), output_field=IntegerField())),
#         sum_literature_distributed_pamphlet_beneficiary_female=Sum(ExpressionWrapper(F('literature_distributed_pamphlet_beneficiary_female'), output_field=IntegerField())),
#         sum_voice_messages_number=Sum(ExpressionWrapper(F('voice_messages_number'), output_field=IntegerField())),
#         sum_voice_messages_beneficiary_male=Sum(ExpressionWrapper(F('voice_messages_beneficiary_male'), output_field=IntegerField())),
#         sum_voice_messages_beneficiary_female=Sum(ExpressionWrapper(F('voice_messages_beneficiary_female'), output_field=IntegerField())),
#         sum_field_visit_number=Sum(ExpressionWrapper(F('field_visit_number'), output_field=IntegerField())),
#         sum_field_visit_beneficiary_male=Sum(ExpressionWrapper(F('field_visit_beneficiary_male'), output_field=IntegerField())),
#         sum_field_visit_beneficiary_female=Sum(ExpressionWrapper(F('field_visit_beneficiary_female'), output_field=IntegerField())),
#         sum_farmer_mela_number=Sum(ExpressionWrapper(F('farmer_mela_number'), output_field=IntegerField())),
#         sum_farmer_mela_beneficiary_male=Sum(ExpressionWrapper(F('farmer_mela_beneficiary_male'), output_field=IntegerField())),
#         sum_farmer_mela_beneficiary_female=Sum(ExpressionWrapper(F('farmer_mela_beneficiary_female'), output_field=IntegerField())),
#         sum_exhibition_arranged_number=Sum(ExpressionWrapper(F('exhibition_arranged_number'), output_field=IntegerField())),
#         sum_exhibition_arranged_beneficiary_male=Sum(ExpressionWrapper(F('exhibition_arranged_beneficiary_male'), output_field=IntegerField())),
#         sum_exhibition_arranged_beneficiary_female=Sum(ExpressionWrapper(F('exhibition_arranged_beneficiary_female'), output_field=IntegerField())),
#         sum_farmer_training_number=Sum(ExpressionWrapper(F('farmer_training_number'), output_field=IntegerField())),
#         sum_farmer_training_beneficiary_male=Sum(ExpressionWrapper(F('farmer_training_beneficiary_male'), output_field=IntegerField())),
#         sum_farmer_training_beneficiary_female=Sum(ExpressionWrapper(F('farmer_training_beneficiary_female'), output_field=IntegerField())),
#         sum_training_number=Sum(ExpressionWrapper(F('training_number'), output_field=IntegerField())),
#         sum_training_beneficiary_male=Sum(ExpressionWrapper(F('training_beneficiary_male'), output_field=IntegerField())),
#         sum_training_beneficiary_female=Sum(ExpressionWrapper(F('training_beneficiary_female'), output_field=IntegerField())),
#         sum_tv_show_number=Sum(ExpressionWrapper(F('tv_show_number'), output_field=IntegerField())),
#         sum_tv_show_beneficiary_male=Sum(ExpressionWrapper(F('tv_show_beneficiary_male'), output_field=IntegerField())),
#         sum_tv_show_beneficiary_female=Sum(ExpressionWrapper(F('tv_show_beneficiary_female'), output_field=IntegerField())),
#         sum_radio_talks_numbers=Sum(ExpressionWrapper(F('radio_talks_numbers'), output_field=IntegerField())),
#         sum_radio_talks_beneficiary_male=Sum(ExpressionWrapper(F('radio_talks_beneficiary_male'), output_field=IntegerField())),
#         sum_radio_talks_beneficiary_female=Sum(ExpressionWrapper(F('radio_talks_beneficiary_female'), output_field=IntegerField())),
#         sum_sensitization_workshop_number=Sum(ExpressionWrapper(F('sensitization_workshop_number'), output_field=IntegerField())),
#         sum_sensitization_workshop_beneficiary_male=Sum(ExpressionWrapper(F('sensitization_workshop_beneficiary_male'), output_field=IntegerField())),
#         sum_sensitization_workshop_beneficiary_female=Sum(ExpressionWrapper(F('sensitization_workshop_beneficiary_female'), output_field=IntegerField())),
#         sum_farmers_queries_number=Sum(ExpressionWrapper(F('farmers_queries_number'), output_field=IntegerField())),
#         sum_farmers_queries_beneficiary_male=Sum(ExpressionWrapper(F('farmers_queries_beneficiary_male'), output_field=IntegerField())),
#         sum_farmers_queries_beneficiary_female=Sum(ExpressionWrapper(F('farmers_queries_beneficiary_female'), output_field=IntegerField())),
#         sum_lectures_delivered_number=Sum(ExpressionWrapper(F('lectures_delivered_number'), output_field=IntegerField())),
#         sum_lectures_delivered_beneficiary_male=Sum(ExpressionWrapper(F('lectures_delivered_beneficiary_male'), output_field=IntegerField())),
#         sum_lectures_delivered_beneficiary_female=Sum(ExpressionWrapper(F('lectures_delivered_beneficiary_female'), output_field=IntegerField())),
#         sum_news_clips_number=Sum(ExpressionWrapper(F('news_clips_number'), output_field=IntegerField())),
#         sum_news_clips_beneficiary_male=Sum(ExpressionWrapper(F('news_clips_beneficiary_male'), output_field=IntegerField())),
#         sum_news_clips_beneficiary_female=Sum(ExpressionWrapper(F('news_clips_beneficiary_female'), output_field=IntegerField())),
#         sum_visit_of_farmers_numbers=Sum(ExpressionWrapper(F('visit_of_farmers_numbers'), output_field=IntegerField())),
#         sum_visit_of_farmers_beneficiary_male=Sum(ExpressionWrapper(F('visit_of_farmers_beneficiary_male'), output_field=IntegerField())),
#         sum_visit_of_farmers_beneficiary_female=Sum(ExpressionWrapper(F('visit_of_farmers_beneficiary_female'), output_field=IntegerField())),
#     )



#     photograph_data = RepresentedPhotograph.objects.filter(
#         district=district_name,
#         date_field__month=target_month,
#     )

#     print('photograph_data',photograph_data)

#     assesment_data = AssessmentSeason.objects.filter(
#         district=district_name,
#         date_field__month=target_month,
#     )

#     print('assesment_data',assesment_data)
    
#     context = {
#         'weekwise_averages': weekwise_averages,
#         'month': month,
#         'progress_count': progress_count,
#         'activities_sums':activities_sums,
#         'photograph_data':photograph_data,
#         'assesment_data':assesment_data,
#         'district_name':district_name,
       
#     }
#     return render(request, 'owner/super_monthly_progress.html', context)




from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum, F, IntegerField, ExpressionWrapper
from django.shortcuts import render

@login_required(login_url='/')
def super_monthly_progress(request, district_name, month):
    district_name = district_name.strip()
    month = month.strip()
    # ---------- 1) Financial Year from session (fallbacks) ----------
    financial_years = Financial_Year.objects.order_by('-id').first()
    selected_fin_year = request.session.get(
        'financial_year',
        financial_years.financial_year if financial_years else '2024-2025'
    )

    # FY -> date range (01-Apr to 31-Mar)
    try:
        start_year, end_year = map(int, selected_fin_year.split('-'))
    except (AttributeError, TypeError, ValueError):
        selected_fin_year = '2024-2025'
        start_year, end_year = 2024, 2025
    start_date = date(start_year, 4, 1)     # 01-Apr
    end_date   = date(end_year, 3, 31)      # 31-Mar
    # print('FY:', selected_fin_year, 'Range:', start_date, '->', end_date)

    # ---------- 2) Month -> integer ----------
    try:
        target_month = datetime.strptime(month, "%B").month
    except ValueError:
        return redirect('super_dashboard')

    # ---------- 3) Standard weeks (month based) ----------
    standard_weeks_data = standard_weeks.objects.filter(month_data__iexact=month)
    # print('standard_weeks_data', standard_weeks_data)

    # ---------- 4) Week-wise pest averages (FY + month + district) ----------
    weekwise_averages = {}
    for standard in standard_weeks_data:
        # NOTE: Agar aapke pest_incidence_data me `week` numeric field hai,
        # to usko match kar rahe hain + district + FY range + month
        pest_data = (
            pest_incidence_data.objects
            .filter(
                district=district_name,
                week=standard.standard_number,
                date_field__range=(start_date, end_date),   # FY filter
                date_field__month=target_month              # Month filter
            )
        )

        averages = pest_data.aggregate(
            avg_jassid_irm=Avg('jassid_irm_average'),
            avg_jassid_nonirm=Avg('jassid_nonirm_average'),
            avg_whitefly_irm=Avg('whitefly_irm_average'),
            avg_whitefly_nonirm=Avg('whitefly_nonirm_average'),
            avg_thrips_irm=Avg('thrips_irm_average'),
            avg_thrips_nonirm=Avg('thrips_nonirm_average'),
            avg_flowers_irm=Avg('flowers_irm_average'),
            avg_flowers_nonirm=Avg('flowers_nonirm_average'),
            avg_green_irm=Avg('green_irm_average'),
            avg_green_nonirm=Avg('green_nonirm_average'),
            avg_locule_irm=Avg('locule_irm_average'),
            avg_locule_nonirm=Avg('locule_nonirm_average'),
            avg_open_ball_irm=Avg('open_ball_irm_average'),
            avg_open_ball_nonirm=Avg('open_ball_nonirm_average'),
            avg_pheromone_irm=Avg('pheromone_irm_average'),
            avg_pheromone_nonirm=Avg('pheromone_nonirm_average'),
            avg_incidence_irm=Avg('incidence_irm_average'),
            avg_incidence_nonirm=Avg('incidence_nonirm_average'),
            avg_locular_damage_irm=Avg('locular_damage_irm_average'),
            avg_locular_damage_nonirm=Avg('locular_damage_nonirm_average')
        )

        # Key: (standard_number, standard_week)
        weekwise_averages[(standard.standard_number, standard.standard_week)] = averages

    # ---------- 5) Monthly physical progress (FY + month + district) ----------
    progress_data = monthly_physical_progress.objects.filter(
        district=district_name,
        date_field__range=(start_date, end_date),  # FY
        date_field__month=target_month,            # Month
    )

    progress_count = safe_numeric_averages(progress_data, {
        'avg_pheromone_traps': 'pheromone_traps',
        'avg_splat': 'splat',
        'avg_pb_rope': 'pb_rope',
        'avg_neem_insecticides': 'neem_insecticides',
        'avg_flonicamid': 'flonicamid',
        'avg_trichocards': 'trichocards',
        'avg_quinalphos': 'quinalphos',
        'avg_chlorpyriphos': 'chlorpyriphos',
        'avg_profenophos': 'profenophos',
    })

    # ---------- 6) Extension activities carried out (FY + month + district) ----------
    activities_data = extension_activities_carried_out.objects.filter(
        district=district_name,
        date_field__range=(start_date, end_date),  # FY
        date_field__month=target_month,            # Month
    )

    extension_activity_sum_fields = [
        'popular_artical_number', 'popular_artical_beneficiary_male', 'popular_artical_beneficiary_female',
        'press_release_number', 'press_release_beneficiary_male', 'press_release_beneficiary_female',
        'extension_material_booklet_number', 'extension_material_booklet_beneficiary_male', 'extension_material_booklet_beneficiary_female',
        'extension_material_leaflet_number', 'extension_material_leaflet_beneficiary_male', 'extension_material_leaflet_beneficiary_female',
        'extension_material_pamphlet_number', 'extension_material_pamphlet_beneficiary_male', 'extension_material_pamphlet_beneficiary_female',
        'extension_material_poster_number', 'extension_material_poster_beneficiary_male', 'extension_material_poster_beneficiary_female',
        'literature_distributed_booklet_number', 'literature_distributed_booklet_beneficiary_male', 'literature_distributed_booklet_beneficiary_female',
        'literature_distributed_leaflet_number', 'literature_distributed_leaflet_beneficiary_male', 'literature_distributed_leaflet_beneficiary_female',
        'literature_distributed_pamphlet_number', 'literature_distributed_pamphlet_beneficiary_male', 'literature_distributed_pamphlet_beneficiary_female',
        'voice_messages_number', 'voice_messages_beneficiary_male', 'voice_messages_beneficiary_female',
        'field_visit_number', 'field_visit_beneficiary_male', 'field_visit_beneficiary_female',
        'farmer_mela_number', 'farmer_mela_beneficiary_male', 'farmer_mela_beneficiary_female',
        'exhibition_arranged_number', 'exhibition_arranged_beneficiary_male', 'exhibition_arranged_beneficiary_female',
        'farmer_training_number', 'farmer_training_beneficiary_male', 'farmer_training_beneficiary_female',
        'training_number', 'training_beneficiary_male', 'training_beneficiary_female',
        'tv_show_number', 'tv_show_beneficiary_male', 'tv_show_beneficiary_female',
        'radio_talks_numbers', 'radio_talks_beneficiary_male', 'radio_talks_beneficiary_female',
        'sensitization_workshop_number', 'sensitization_workshop_beneficiary_male', 'sensitization_workshop_beneficiary_female',
        'farmers_queries_number', 'farmers_queries_beneficiary_male', 'farmers_queries_beneficiary_female',
        'lectures_delivered_number', 'lectures_delivered_beneficiary_male', 'lectures_delivered_beneficiary_female',
        'news_clips_number', 'news_clips_beneficiary_male', 'news_clips_beneficiary_female',
        'visit_of_farmers_numbers', 'visit_of_farmers_beneficiary_male', 'visit_of_farmers_beneficiary_female',
    ]
    activities_sums = safe_numeric_sums(activities_data, extension_activity_sum_fields)
    activities_sums.update({
        'sum_exhibitions_number': activities_sums['sum_exhibition_arranged_number'],
        'sum_exhibitions_beneficiary_male': activities_sums['sum_exhibition_arranged_beneficiary_male'],
        'sum_exhibitions_beneficiary_female': activities_sums['sum_exhibition_arranged_beneficiary_female'],
        'sum_workshops_number': activities_sums['sum_training_number'],
        'sum_workshops_beneficiary_male': activities_sums['sum_training_beneficiary_male'],
        'sum_workshops_beneficiary_female': activities_sums['sum_training_beneficiary_female'],
        'sum_tv_shows_number': activities_sums['sum_tv_show_number'],
        'sum_tv_shows_beneficiary_male': activities_sums['sum_tv_show_beneficiary_male'],
        'sum_tv_shows_beneficiary_female': activities_sums['sum_tv_show_beneficiary_female'],
        'sum_radio_talks_number': activities_sums['sum_radio_talks_numbers'],
        'sum_sensitization_workshops_number': activities_sums['sum_sensitization_workshop_number'],
        'sum_sensitization_workshops_beneficiary_male': activities_sums['sum_sensitization_workshop_beneficiary_male'],
        'sum_sensitization_workshops_beneficiary_female': activities_sums['sum_sensitization_workshop_beneficiary_female'],
        'sum_farmer_queries_number': activities_sums['sum_farmers_queries_number'],
        'sum_farmer_queries_beneficiary_male': activities_sums['sum_farmers_queries_beneficiary_male'],
        'sum_farmer_queries_beneficiary_female': activities_sums['sum_farmers_queries_beneficiary_female'],
        'sum_lectures_number': activities_sums['sum_lectures_delivered_number'],
        'sum_lectures_beneficiary_male': activities_sums['sum_lectures_delivered_beneficiary_male'],
        'sum_lectures_beneficiary_female': activities_sums['sum_lectures_delivered_beneficiary_female'],
        'sum_farmer_visits_number': activities_sums['sum_visit_of_farmers_numbers'],
        'sum_farmer_visits_beneficiary_male': activities_sums['sum_visit_of_farmers_beneficiary_male'],
        'sum_farmer_visits_beneficiary_female': activities_sums['sum_visit_of_farmers_beneficiary_female'],
    })

    # ---------- 7) Photographs (FY + month + district) ----------
    photograph_data = RepresentedPhotograph.objects.filter(
        district=district_name,
        date_field__range=(start_date, end_date),  # FY
        date_field__month=target_month,            # Month
    )

    # ---------- 8) Assessment (FY + month + district) ----------
    assesment_data = AssessmentSeason.objects.filter(
        district=district_name,
        date_field__range=(start_date, end_date),  # FY
        date_field__month=target_month,            # Month
    )

    context = {
        'weekwise_averages': weekwise_averages,
        'month': month,
        'progress_count': progress_count,
        'activities_sums': activities_sums,
        'photograph_data': photograph_data,
        'assesment_data': assesment_data,
        'district_name': district_name,
        'selected_fin_year': selected_fin_year,
        'fy_start_date': start_date,
        'fy_end_date': end_date,
    }
    return render(request, 'owner/super_monthly_progress.html', context)



def detailed_report(request, district_name, month):
    # Filter standard_weeks by the specified month and year
    standard_weeks_data = standard_weeks.objects.filter(month_data=month)

    # Initialize a dictionary to hold week-wise data and averages
    weekwise_data = {}

    for standard in standard_weeks_data:
        # Filter pest incidence data where the week matches the standard number and district
        pest_data = pest_incidence_data.objects.filter(week=standard.standard_number, district=district_name)

        # For each pest type, retrieve 10 entries and their average
        for entry in pest_data:
            week_data = {
                'jassid_irm': [entry.jassid_irm_item1, entry.jassid_irm_item2, entry.jassid_irm_item3, 
                               entry.jassid_irm_item4, entry.jassid_irm_item5, entry.jassid_irm_item6,
                               entry.jassid_irm_item7, entry.jassid_irm_item8, entry.jassid_irm_item9,
                               entry.jassid_irm_item10],
                'jassid_nonirm': [entry.jassid_nonirm_item1, entry.jassid_nonirm_item2, entry.jassid_nonirm_item3,
                                  entry.jassid_nonirm_item4, entry.jassid_nonirm_item5, entry.jassid_nonirm_item6,
                                  entry.jassid_nonirm_item7, entry.jassid_nonirm_item8, entry.jassid_nonirm_item9,
                                  entry.jassid_nonirm_item10],
                'whitefly_irm': [entry.whitefly_irm_item1, entry.whitefly_irm_item2, entry.whitefly_irm_item3,
                                 entry.whitefly_irm_item4, entry.whitefly_irm_item5, entry.whitefly_irm_item6,
                                 entry.whitefly_irm_item7, entry.whitefly_irm_item8, entry.whitefly_irm_item9,
                                 entry.whitefly_irm_item10],
                'whitefly_nonirm': [entry.whitefly_nonirm_item1, entry.whitefly_nonirm_item2, entry.whitefly_nonirm_item3,
                                    entry.whitefly_nonirm_item4, entry.whitefly_nonirm_item5, entry.whitefly_nonirm_item6,
                                    entry.whitefly_nonirm_item7, entry.whitefly_nonirm_item8, entry.whitefly_nonirm_item9,
                                    entry.whitefly_nonirm_item10],
                'thrips_irm': [entry.thrips_irm_item1, entry.thrips_irm_item2, entry.thrips_irm_item3,
                               entry.thrips_irm_item4, entry.thrips_irm_item5, entry.thrips_irm_item6,
                               entry.thrips_irm_item7, entry.thrips_irm_item8, entry.thrips_irm_item9,
                               entry.thrips_irm_item10],
                'thrips_nonirm': [entry.thrips_nonirm_item1, entry.thrips_nonirm_item2, entry.thrips_nonirm_item3,
                                  entry.thrips_nonirm_item4, entry.thrips_nonirm_item5, entry.thrips_nonirm_item6,
                                  entry.thrips_nonirm_item7, entry.thrips_nonirm_item8, entry.thrips_nonirm_item9,
                                  entry.thrips_nonirm_item10],
                'flowers_irm': [entry.flowers_irm_item1, entry.flowers_irm_item2, entry.flowers_irm_item3,
                                entry.flowers_irm_item4, entry.flowers_irm_item5, entry.flowers_irm_item6,
                                entry.flowers_irm_item7, entry.flowers_irm_item8, entry.flowers_irm_item9,
                                entry.flowers_irm_item10],
                'flowers_nonirm': [entry.flowers_nonirm_item1, entry.flowers_nonirm_item2, entry.flowers_nonirm_item3,
                                   entry.flowers_nonirm_item4, entry.flowers_nonirm_item5, entry.flowers_nonirm_item6,
                                   entry.flowers_nonirm_item7, entry.flowers_nonirm_item8, entry.flowers_nonirm_item9,
                                   entry.flowers_nonirm_item10],
                'green_boll_irm': [entry.green_irm_item1, entry.green_irm_item2, entry.green_irm_item3,
                                   entry.green_irm_item4, entry.green_irm_item5, entry.green_irm_item6,
                                   entry.green_irm_item7, entry.green_irm_item8, entry.green_irm_item9,
                                   entry.green_irm_item10],
                'green_boll_nonirm': [entry.green_nonirm_item1, entry.green_nonirm_item2, entry.green_nonirm_item3,
                                      entry.green_nonirm_item4, entry.green_nonirm_item5, entry.green_nonirm_item6,
                                      entry.green_nonirm_item7, entry.green_nonirm_item8, entry.green_nonirm_item9,
                                      entry.green_nonirm_item10],
                'locule_irm': [entry.locule_irm_item1, entry.locule_irm_item2, entry.locule_irm_item3,
                               entry.locule_irm_item4, entry.locule_irm_item5, entry.locule_irm_item6,
                               entry.locule_irm_item7, entry.locule_irm_item8, entry.locule_irm_item9,
                               entry.locule_irm_item10],
                'locule_nonirm': [entry.locule_nonirm_item1, entry.locule_nonirm_item2, entry.locule_nonirm_item3,
                                  entry.locule_nonirm_item4, entry.locule_nonirm_item5, entry.locule_nonirm_item6,
                                  entry.locule_nonirm_item7, entry.locule_nonirm_item8, entry.locule_nonirm_item9,
                                  entry.locule_nonirm_item10],
                'open_ball_irm': [entry.open_ball_irm_item1, entry.open_ball_irm_item2, entry.open_ball_irm_item3,
                                  entry.open_ball_irm_item4, entry.open_ball_irm_item5, entry.open_ball_irm_item6,
                                  entry.open_ball_irm_item7, entry.open_ball_irm_item8, entry.open_ball_irm_item9,
                                  entry.open_ball_irm_item10],
                'open_ball_nonirm': [entry.open_ball_nonirm_item1, entry.open_ball_nonirm_item2, entry.open_ball_nonirm_item3,
                                     entry.open_ball_nonirm_item4, entry.open_ball_nonirm_item5, entry.open_ball_nonirm_item6,
                                     entry.open_ball_nonirm_item7, entry.open_ball_nonirm_item8, entry.open_ball_nonirm_item9,
                                     entry.open_ball_nonirm_item10],
                'pheromone_irm': [entry.pheromone_irm_item1, entry.pheromone_irm_item2, entry.pheromone_irm_item3,
                                  entry.pheromone_irm_item4, entry.pheromone_irm_item5, entry.pheromone_irm_item6,
                                  entry.pheromone_irm_item7, entry.pheromone_irm_item8, entry.pheromone_irm_item9,
                                  entry.pheromone_irm_item10],
                'pheromone_nonirm': [entry.pheromone_nonirm_item1, entry.pheromone_nonirm_item2, entry.pheromone_nonirm_item3,
                                     entry.pheromone_nonirm_item4, entry.pheromone_nonirm_item5, entry.pheromone_nonirm_item6,
                                     entry.pheromone_nonirm_item7, entry.pheromone_nonirm_item8, entry.pheromone_nonirm_item9,
                                     entry.pheromone_nonirm_item10],
                'locular_damage_irm': [entry.locular_damage_irm1, entry.locular_damage_irm2, entry.locular_damage_irm3,
                                  entry.locular_damage_irm4, entry.locular_damage_irm5, entry.locular_damage_irm6,
                                  entry.locular_damage_irm7, entry.locular_damage_irm8, entry.locular_damage_irm9,
                                  entry.locular_damage_irm10],
                'locular_damage_nonirm': [entry.locular_damage_nonirm1, entry.locular_damage_nonirm2, entry.locular_damage_nonirm3,
                                     entry.locular_damage_nonirm4, entry.locular_damage_nonirm5, entry.locular_damage_nonirm6,
                                     entry.locular_damage_nonirm7, entry.locular_damage_nonirm8, entry.locular_damage_nonirm9,
                                     entry.locular_damage_nonirm10],
                'incidence_irm': [entry.incidence_irm_item1, entry.incidence_irm_item2, entry.incidence_irm_item3,
                                  entry.incidence_irm_item4, entry.incidence_irm_item5, entry.incidence_irm_item6,
                                  entry.incidence_irm_item7, entry.incidence_irm_item8, entry.incidence_irm_item9,
                                  entry.incidence_irm_item10],
                'incidence_nonirm': [entry.incidence_nonirm_item1, entry.incidence_nonirm_item2, entry.incidence_nonirm_item3,
                                     entry.incidence_nonirm_item4, entry.incidence_nonirm_item5, entry.incidence_nonirm_item6,
                                     entry.incidence_nonirm_item7, entry.incidence_nonirm_item8, entry.incidence_nonirm_item9,
                                     entry.incidence_nonirm_item10],
            }
            
            # Add average values for each pest
            averages = {
                'avg_jassid_irm': entry.jassid_irm_average,
                'avg_jassid_nonirm': entry.jassid_nonirm_average,
                'avg_whitefly_irm': entry.whitefly_irm_average,
                'avg_whitefly_nonirm': entry.whitefly_nonirm_average,
                'avg_thrips_irm': entry.thrips_irm_average,
                'avg_thrips_nonirm': entry.thrips_nonirm_average,
                'avg_flowers_irm': entry.flowers_irm_average,
                'avg_flowers_nonirm': entry.flowers_nonirm_average,
                'avg_green_boll_irm': entry.green_irm_average,
                'avg_green_boll_nonirm': entry.green_nonirm_average,
                'avg_locule_irm': entry.locule_irm_average,
                'avg_locule_nonirm': entry.locule_nonirm_average,
                'avg_open_ball_irm': entry.open_ball_irm_average,
                'avg_open_ball_nonirm': entry.open_ball_nonirm_average,
                'avg_pheromone_irm':entry.pheromone_irm_average,
                'avg_pheromone_nonirm':entry.pheromone_nonirm_average,
                'avg_incidence_irm':entry.incidence_irm_average,
                'avg_incidence_nonirm':entry.incidence_nonirm_average,
                'avg_locular_damage_irm':entry.locular_damage_irm_average,
                'avg_locular_damage_nonirm':entry.locular_damage_nonirm_average,        
                
                }

            # Add week data and averages to the dictionary
            weekwise_data[(standard.standard_number, standard.standard_week)] = {
                'data': week_data,
                'averages': averages
            }

    # Pass the weekwise data to the template for display
    context = {
        'weekwise_data': weekwise_data,
        'district_name': district_name,
        'month': month
    }
    return render(request, 'owner/detailed_report.html', context)


# views.py
from django.shortcuts import render, redirect, get_object_or_404

def update_pest_incidence(request, district_name, month, week_number):
    # Fetch standard week data for the given month and week number
    standard_week = get_object_or_404(standard_weeks, month_data=month, standard_number=week_number)
    
    # Fetch the pest incidence data for the given district and week
    pest_data = get_object_or_404(pest_incidence_data, week=week_number, district=district_name)
    
    if request.method == 'POST':
        # Jassid IRM and Non-IRM fields
        pest_data.jassid_irm_item1 = request.POST.get('jassid_irm_item1')
        pest_data.jassid_irm_item2 = request.POST.get('jassid_irm_item2')
        pest_data.jassid_irm_item3 = request.POST.get('jassid_irm_item3')
        pest_data.jassid_irm_item4 = request.POST.get('jassid_irm_item4')
        pest_data.jassid_irm_item5 = request.POST.get('jassid_irm_item5')
        pest_data.jassid_irm_item6 = request.POST.get('jassid_irm_item6')
        pest_data.jassid_irm_item7 = request.POST.get('jassid_irm_item7')
        pest_data.jassid_irm_item8 = request.POST.get('jassid_irm_item8')
        pest_data.jassid_irm_item9 = request.POST.get('jassid_irm_item9')
        pest_data.jassid_irm_item10 = request.POST.get('jassid_irm_item10')
        
        pest_data.jassid_nonirm_item1 = request.POST.get('jassid_nonirm_item1')
        pest_data.jassid_nonirm_item2 = request.POST.get('jassid_nonirm_item2')
        pest_data.jassid_nonirm_item3 = request.POST.get('jassid_nonirm_item3')
        pest_data.jassid_nonirm_item4 = request.POST.get('jassid_nonirm_item4')
        pest_data.jassid_nonirm_item5 = request.POST.get('jassid_nonirm_item5')
        pest_data.jassid_nonirm_item6 = request.POST.get('jassid_nonirm_item6')
        pest_data.jassid_nonirm_item7 = request.POST.get('jassid_nonirm_item7')
        pest_data.jassid_nonirm_item8 = request.POST.get('jassid_nonirm_item8')
        pest_data.jassid_nonirm_item9 = request.POST.get('jassid_nonirm_item9')
        pest_data.jassid_nonirm_item10 = request.POST.get('jassid_nonirm_item10')

        # Whitefly IRM and Non-IRM fields
        pest_data.whitefly_irm_item1 = request.POST.get('whitefly_irm_item1')
        pest_data.whitefly_irm_item2 = request.POST.get('whitefly_irm_item2')
        pest_data.whitefly_irm_item3 = request.POST.get('whitefly_irm_item3')
        pest_data.whitefly_irm_item4 = request.POST.get('whitefly_irm_item4')
        pest_data.whitefly_irm_item5 = request.POST.get('whitefly_irm_item5')
        pest_data.whitefly_irm_item6 = request.POST.get('whitefly_irm_item6')
        pest_data.whitefly_irm_item7 = request.POST.get('whitefly_irm_item7')
        pest_data.whitefly_irm_item8 = request.POST.get('whitefly_irm_item8')
        pest_data.whitefly_irm_item9 = request.POST.get('whitefly_irm_item9')
        pest_data.whitefly_irm_item10 = request.POST.get('whitefly_irm_item10')

        pest_data.whitefly_nonirm_item1 = request.POST.get('whitefly_nonirm_item1')
        pest_data.whitefly_nonirm_item2 = request.POST.get('whitefly_nonirm_item2')
        pest_data.whitefly_nonirm_item3 = request.POST.get('whitefly_nonirm_item3')
        pest_data.whitefly_nonirm_item4 = request.POST.get('whitefly_nonirm_item4')
        pest_data.whitefly_nonirm_item5 = request.POST.get('whitefly_nonirm_item5')
        pest_data.whitefly_nonirm_item6 = request.POST.get('whitefly_nonirm_item6')
        pest_data.whitefly_nonirm_item7 = request.POST.get('whitefly_nonirm_item7')
        pest_data.whitefly_nonirm_item8 = request.POST.get('whitefly_nonirm_item8')
        pest_data.whitefly_nonirm_item9 = request.POST.get('whitefly_nonirm_item9')
        pest_data.whitefly_nonirm_item10 = request.POST.get('whitefly_nonirm_item10')

        # Thrips IRM and Non-IRM fields
        pest_data.thrips_irm_item1 = request.POST.get('thrips_irm_item1')
        pest_data.thrips_irm_item2 = request.POST.get('thrips_irm_item2')
        pest_data.thrips_irm_item3 = request.POST.get('thrips_irm_item3')
        pest_data.thrips_irm_item4 = request.POST.get('thrips_irm_item4')
        pest_data.thrips_irm_item5 = request.POST.get('thrips_irm_item5')
        pest_data.thrips_irm_item6 = request.POST.get('thrips_irm_item6')
        pest_data.thrips_irm_item7 = request.POST.get('thrips_irm_item7')
        pest_data.thrips_irm_item8 = request.POST.get('thrips_irm_item8')
        pest_data.thrips_irm_item9 = request.POST.get('thrips_irm_item9')
        pest_data.thrips_irm_item10 = request.POST.get('thrips_irm_item10')
        
        pest_data.thrips_nonirm_item1 = request.POST.get('thrips_nonirm_item1')
        pest_data.thrips_nonirm_item2 = request.POST.get('thrips_nonirm_item2')
        pest_data.thrips_nonirm_item3 = request.POST.get('thrips_nonirm_item3')
        pest_data.thrips_nonirm_item4 = request.POST.get('thrips_nonirm_item4')
        pest_data.thrips_nonirm_item5 = request.POST.get('thrips_nonirm_item5')
        pest_data.thrips_nonirm_item6 = request.POST.get('thrips_nonirm_item6')
        pest_data.thrips_nonirm_item7 = request.POST.get('thrips_nonirm_item7')
        pest_data.thrips_nonirm_item8 = request.POST.get('thrips_nonirm_item8')
        pest_data.thrips_nonirm_item9 = request.POST.get('thrips_nonirm_item9')
        pest_data.thrips_nonirm_item10 = request.POST.get('thrips_nonirm_item10')

        # Flowers IRM and Non-IRM fields
        pest_data.flowers_irm_item1 = request.POST.get('flowers_irm_item1')
        pest_data.flowers_irm_item2 = request.POST.get('flowers_irm_item2')
        pest_data.flowers_irm_item3 = request.POST.get('flowers_irm_item3')
        pest_data.flowers_irm_item4 = request.POST.get('flowers_irm_item4')
        pest_data.flowers_irm_item5 = request.POST.get('flowers_irm_item5')
        pest_data.flowers_irm_item6 = request.POST.get('flowers_irm_item6')
        pest_data.flowers_irm_item7 = request.POST.get('flowers_irm_item7')
        pest_data.flowers_irm_item8 = request.POST.get('flowers_irm_item8')
        pest_data.flowers_irm_item9 = request.POST.get('flowers_irm_item9')
        pest_data.flowers_irm_item10 = request.POST.get('flowers_irm_item10')
        
        pest_data.flowers_nonirm_item1 = request.POST.get('flowers_nonirm_item1')
        pest_data.flowers_nonirm_item2 = request.POST.get('flowers_nonirm_item2')
        pest_data.flowers_nonirm_item3 = request.POST.get('flowers_nonirm_item3')
        pest_data.flowers_nonirm_item4 = request.POST.get('flowers_nonirm_item4')
        pest_data.flowers_nonirm_item5 = request.POST.get('flowers_nonirm_item5')
        pest_data.flowers_nonirm_item6 = request.POST.get('flowers_nonirm_item6')
        pest_data.flowers_nonirm_item7 = request.POST.get('flowers_nonirm_item7')
        pest_data.flowers_nonirm_item8 = request.POST.get('flowers_nonirm_item8')
        pest_data.flowers_nonirm_item9 = request.POST.get('flowers_nonirm_item9')
        pest_data.flowers_nonirm_item10 = request.POST.get('flowers_nonirm_item10')
        

        # Locule IRM and Non-IRM fields
        pest_data.locule_irm_item1 = request.POST.get('locule_irm_item1')
        pest_data.locule_irm_item2 = request.POST.get('locule_irm_item2')
        pest_data.locule_irm_item3 = request.POST.get('locule_irm_item3')
        pest_data.locule_irm_item4 = request.POST.get('locule_irm_item4')
        pest_data.locule_irm_item5 = request.POST.get('locule_irm_item5')
        pest_data.locule_irm_item6 = request.POST.get('locule_irm_item6')
        pest_data.locule_irm_item7 = request.POST.get('locule_irm_item7')
        pest_data.locule_irm_item8 = request.POST.get('locule_irm_item8')
        pest_data.locule_irm_item9 = request.POST.get('locule_irm_item9')
        pest_data.locule_irm_item10 = request.POST.get('locule_irm_item10')
        
        pest_data.locule_nonirm_item1 = request.POST.get('locule_nonirm_item1')
        pest_data.locule_nonirm_item2 = request.POST.get('locule_nonirm_item2')
        pest_data.locule_nonirm_item3 = request.POST.get('locule_nonirm_item3')
        pest_data.locule_nonirm_item4 = request.POST.get('locule_nonirm_item4')
        pest_data.locule_nonirm_item5 = request.POST.get('locule_nonirm_item5')
        pest_data.locule_nonirm_item6 = request.POST.get('locule_nonirm_item6')
        pest_data.locule_nonirm_item7 = request.POST.get('locule_nonirm_item7')
        pest_data.locule_nonirm_item8 = request.POST.get('locule_nonirm_item8')
        pest_data.locule_nonirm_item9 = request.POST.get('locule_nonirm_item9')
        pest_data.locule_nonirm_item10 = request.POST.get('locule_nonirm_item10')

        # Pheromone IRM and Non-IRM fields
        pest_data.pheromone_irm_item1 = request.POST.get('pheromone_irm_item1')
        pest_data.pheromone_irm_item2 = request.POST.get('pheromone_irm_item2')
        pest_data.pheromone_irm_item3 = request.POST.get('pheromone_irm_item3')
        pest_data.pheromone_irm_item4 = request.POST.get('pheromone_irm_item4')
        pest_data.pheromone_irm_item5 = request.POST.get('pheromone_irm_item5')
        pest_data.pheromone_irm_item6 = request.POST.get('pheromone_irm_item6')
        pest_data.pheromone_irm_item7 = request.POST.get('pheromone_irm_item7')
        pest_data.pheromone_irm_item8 = request.POST.get('pheromone_irm_item8')
        pest_data.pheromone_irm_item9 = request.POST.get('pheromone_irm_item9')
        pest_data.pheromone_irm_item10 = request.POST.get('pheromone_irm_item10')

        pest_data.pheromone_nonirm_item1 = request.POST.get('pheromone_nonirm_item1')
        pest_data.pheromone_nonirm_item2 = request.POST.get('pheromone_nonirm_item2')
        pest_data.pheromone_nonirm_item3 = request.POST.get('pheromone_nonirm_item3')
        pest_data.pheromone_nonirm_item4 = request.POST.get('pheromone_nonirm_item4')
        pest_data.pheromone_nonirm_item5 = request.POST.get('pheromone_nonirm_item5')
        pest_data.pheromone_nonirm_item6 = request.POST.get('pheromone_nonirm_item6')
        pest_data.pheromone_nonirm_item7 = request.POST.get('pheromone_nonirm_item7')
        pest_data.pheromone_nonirm_item8 = request.POST.get('pheromone_nonirm_item8')
        pest_data.pheromone_nonirm_item9 = request.POST.get('pheromone_nonirm_item9')
        pest_data.pheromone_nonirm_item10 = request.POST.get('pheromone_nonirm_item10')

        # Green IRM and Non-IRM fields
        pest_data.green_irm_item1 = request.POST.get('green_irm_item1')
        pest_data.green_irm_item2 = request.POST.get('green_irm_item2')
        pest_data.green_irm_item3 = request.POST.get('green_irm_item3')
        pest_data.green_irm_item4 = request.POST.get('green_irm_item4')
        pest_data.green_irm_item5 = request.POST.get('green_irm_item5')
        pest_data.green_irm_item6 = request.POST.get('green_irm_item6')
        pest_data.green_irm_item7 = request.POST.get('green_irm_item7')
        pest_data.green_irm_item8 = request.POST.get('green_irm_item8')
        pest_data.green_irm_item9 = request.POST.get('green_irm_item9')
        pest_data.green_irm_item10 = request.POST.get('green_irm_item10')

        pest_data.green_nonirm_item1 = request.POST.get('green_nonirm_item1')
        pest_data.green_nonirm_item2 = request.POST.get('green_nonirm_item2')
        pest_data.green_nonirm_item3 = request.POST.get('green_nonirm_item3')
        pest_data.green_nonirm_item4 = request.POST.get('green_nonirm_item4')
        pest_data.green_nonirm_item5 = request.POST.get('green_nonirm_item5')
        pest_data.green_nonirm_item6 = request.POST.get('green_nonirm_item6')
        pest_data.green_nonirm_item7 = request.POST.get('green_nonirm_item7')
        pest_data.green_nonirm_item8 = request.POST.get('green_nonirm_item8')
        pest_data.green_nonirm_item9 = request.POST.get('green_nonirm_item9')
        pest_data.green_nonirm_item10 = request.POST.get('green_nonirm_item10')
        
        
        # Open IRM and Non-IRM fields
        pest_data.open_ball_irm_item1 = request.POST.get('open_ball_irm_item1')
        pest_data.open_ball_irm_item2 = request.POST.get('open_ball_irm_item2')
        pest_data.open_ball_irm_item3 = request.POST.get('open_ball_irm_item3')
        pest_data.open_ball_irm_item4 = request.POST.get('open_ball_irm_item4')
        pest_data.open_ball_irm_item5 = request.POST.get('open_ball_irm_item5')
        pest_data.open_ball_irm_item6 = request.POST.get('open_ball_irm_item6')
        pest_data.open_ball_irm_item7 = request.POST.get('open_ball_irm_item7')
        pest_data.open_ball_irm_item8 = request.POST.get('open_ball_irm_item8')
        pest_data.open_ball_irm_item9 = request.POST.get('open_ball_irm_item9')
        pest_data.open_ball_irm_item10 = request.POST.get('open_ball_irm_item10')

        pest_data.open_ball_nonirm_item1 = request.POST.get('open_ball_nonirm_item1')
        pest_data.open_ball_nonirm_item2 = request.POST.get('open_ball_nonirm_item2')
        pest_data.open_ball_nonirm_item3 = request.POST.get('open_ball_nonirm_item3')
        pest_data.open_ball_nonirm_item4 = request.POST.get('open_ball_nonirm_item4')
        pest_data.open_ball_nonirm_item5 = request.POST.get('open_ball_nonirm_item5')
        pest_data.open_ball_nonirm_item6 = request.POST.get('open_ball_nonirm_item6')
        pest_data.open_ball_nonirm_item7 = request.POST.get('open_ball_nonirm_item7')
        pest_data.open_ball_nonirm_item8 = request.POST.get('open_ball_nonirm_item8')
        pest_data.open_ball_nonirm_item9 = request.POST.get('open_ball_nonirm_item9')
        pest_data.open_ball_nonirm_item10 = request.POST.get('open_ball_nonirm_item10')
        
        
        # Incidence IRM fields
        pest_data.incidence_irm_item1 = request.POST.get('incidence_irm_item1')
        pest_data.incidence_irm_item2 = request.POST.get('incidence_irm_item2')
        pest_data.incidence_irm_item3 = request.POST.get('incidence_irm_item3')
        pest_data.incidence_irm_item4 = request.POST.get('incidence_irm_item4')
        pest_data.incidence_irm_item5 = request.POST.get('incidence_irm_item5')
        pest_data.incidence_irm_item6 = request.POST.get('incidence_irm_item6')
        pest_data.incidence_irm_item7 = request.POST.get('incidence_irm_item7')
        pest_data.incidence_irm_item8 = request.POST.get('incidence_irm_item8')
        pest_data.incidence_irm_item9 = request.POST.get('incidence_irm_item9')
        pest_data.incidence_irm_item10 = request.POST.get('incidence_irm_item10')

        # Non-IRM fields
        pest_data.incidence_nonirm_item1 = request.POST.get('incidence_nonirm_item1')
        pest_data.incidence_nonirm_item2 = request.POST.get('incidence_nonirm_item2')
        pest_data.incidence_nonirm_item3 = request.POST.get('incidence_nonirm_item3')
        pest_data.incidence_nonirm_item4 = request.POST.get('incidence_nonirm_item4')
        pest_data.incidence_nonirm_item5 = request.POST.get('incidence_nonirm_item5')
        pest_data.incidence_nonirm_item6 = request.POST.get('incidence_nonirm_item6')
        pest_data.incidence_nonirm_item7 = request.POST.get('incidence_nonirm_item7')
        pest_data.incidence_nonirm_item8 = request.POST.get('incidence_nonirm_item8')
        pest_data.incidence_nonirm_item9 = request.POST.get('incidence_nonirm_item9')
        pest_data.incidence_nonirm_item10 = request.POST.get('incidence_nonirm_item10')

        # Locular Damage IRM fields
        pest_data.locular_damage_irm1 = request.POST.get('locular_damage_irm1')
        pest_data.locular_damage_irm2 = request.POST.get('locular_damage_irm2')
        pest_data.locular_damage_irm3 = request.POST.get('locular_damage_irm3')
        pest_data.locular_damage_irm4 = request.POST.get('locular_damage_irm4')
        pest_data.locular_damage_irm5 = request.POST.get('locular_damage_irm5')
        pest_data.locular_damage_irm6 = request.POST.get('locular_damage_irm6')
        pest_data.locular_damage_irm7 = request.POST.get('locular_damage_irm7')
        pest_data.locular_damage_irm8 = request.POST.get('locular_damage_irm8')
        pest_data.locular_damage_irm9 = request.POST.get('locular_damage_irm9')
        pest_data.locular_damage_irm10 = request.POST.get('locular_damage_irm10')

        # Non-IRM fields
        pest_data.locular_damage_nonirm1 = request.POST.get('locular_damage_nonirm1')
        pest_data.locular_damage_nonirm2 = request.POST.get('locular_damage_nonirm2')
        pest_data.locular_damage_nonirm3 = request.POST.get('locular_damage_nonirm3')
        pest_data.locular_damage_nonirm4 = request.POST.get('locular_damage_nonirm4')
        pest_data.locular_damage_nonirm5 = request.POST.get('locular_damage_nonirm5')
        pest_data.locular_damage_nonirm6 = request.POST.get('locular_damage_nonirm6')
        pest_data.locular_damage_nonirm7 = request.POST.get('locular_damage_nonirm7')
        pest_data.locular_damage_nonirm8 = request.POST.get('locular_damage_nonirm8')
        pest_data.locular_damage_nonirm9 = request.POST.get('locular_damage_nonirm9')
        pest_data.locular_damage_nonirm10 = request.POST.get('locular_damage_nonirm10')



        # Calculate and assign averages
        pest_data.jassid_irm_average = calculate_average([
            pest_data.jassid_irm_item1, pest_data.jassid_irm_item2,
            pest_data.jassid_irm_item3, pest_data.jassid_irm_item4,
            pest_data.jassid_irm_item5, pest_data.jassid_irm_item6,
            pest_data.jassid_irm_item7, pest_data.jassid_irm_item8,
            pest_data.jassid_irm_item9, pest_data.jassid_irm_item10
        ])
        
        # Calculate and assign averages
        pest_data.jassid_nonirm_average = calculate_average([
            pest_data.jassid_nonirm_item1, pest_data.jassid_nonirm_item2,
            pest_data.jassid_nonirm_item3, pest_data.jassid_nonirm_item4,
            pest_data.jassid_nonirm_item5, pest_data.jassid_nonirm_item6,
            pest_data.jassid_nonirm_item7, pest_data.jassid_nonirm_item8,
            pest_data.jassid_nonirm_item9, pest_data.jassid_nonirm_item10
        ])
        
        pest_data.whitefly_irm_average = calculate_average([
            pest_data.whitefly_irm_item1, pest_data.whitefly_irm_item2,
            pest_data.whitefly_irm_item3, pest_data.whitefly_irm_item4,
            pest_data.whitefly_irm_item5, pest_data.whitefly_irm_item6,
            pest_data.whitefly_irm_item7, pest_data.whitefly_irm_item8,
            pest_data.whitefly_irm_item9, pest_data.whitefly_irm_item10
        ])
        
        pest_data.whitefly_nonirm_average = calculate_average([
            pest_data.whitefly_nonirm_item1, pest_data.whitefly_nonirm_item2,
            pest_data.whitefly_nonirm_item3, pest_data.whitefly_nonirm_item4,
            pest_data.whitefly_nonirm_item5, pest_data.whitefly_nonirm_item6,
            pest_data.whitefly_nonirm_item7, pest_data.whitefly_nonirm_item8,
            pest_data.whitefly_nonirm_item9, pest_data.whitefly_nonirm_item10
        ])
        
        pest_data.thrips_irm_average = calculate_average([
            pest_data.thrips_irm_item1, pest_data.thrips_irm_item2,
            pest_data.thrips_irm_item3, pest_data.thrips_irm_item4,
            pest_data.thrips_irm_item5, pest_data.thrips_irm_item6,
            pest_data.thrips_irm_item7, pest_data.thrips_irm_item8,
            pest_data.thrips_irm_item9, pest_data.thrips_irm_item10
        ])
        
        
        pest_data.thrips_nonirm_average = calculate_average([
            pest_data.thrips_nonirm_item1, pest_data.thrips_nonirm_item2,
            pest_data.thrips_nonirm_item3, pest_data.thrips_nonirm_item4,
            pest_data.thrips_nonirm_item5, pest_data.thrips_nonirm_item6,
            pest_data.thrips_nonirm_item7, pest_data.thrips_nonirm_item8,
            pest_data.thrips_nonirm_item9, pest_data.thrips_nonirm_item10
        ])
        
        pest_data.flowers_irm_average = calculate_average([
            pest_data.flowers_irm_item1, pest_data.flowers_irm_item2,
            pest_data.flowers_irm_item3, pest_data.flowers_irm_item4,
            pest_data.flowers_irm_item5, pest_data.flowers_irm_item6,
            pest_data.flowers_irm_item7, pest_data.flowers_irm_item8,
            pest_data.flowers_irm_item9, pest_data.flowers_irm_item10
        ])
        
        pest_data.flowers_nonirm_average = calculate_average([
            pest_data.flowers_nonirm_item1, pest_data.flowers_nonirm_item2,
            pest_data.flowers_nonirm_item3, pest_data.flowers_nonirm_item4,
            pest_data.flowers_nonirm_item5, pest_data.flowers_nonirm_item6,
            pest_data.flowers_nonirm_item7, pest_data.flowers_nonirm_item8,
            pest_data.flowers_nonirm_item9, pest_data.flowers_nonirm_item10
        ])
        
        pest_data.green_irm_average = calculate_average([
            pest_data.green_irm_item1, pest_data.green_irm_item2,
            pest_data.green_irm_item3, pest_data.green_irm_item4,
            pest_data.green_irm_item5, pest_data.green_irm_item6,
            pest_data.green_irm_item7, pest_data.green_irm_item8,
            pest_data.green_irm_item9, pest_data.green_irm_item10
        ])
        
        pest_data.green_nonirm_average = calculate_average([
            pest_data.green_nonirm_item1, pest_data.green_nonirm_item2,
            pest_data.green_nonirm_item3, pest_data.green_nonirm_item4,
            pest_data.green_nonirm_item5, pest_data.green_nonirm_item6,
            pest_data.green_nonirm_item7, pest_data.green_nonirm_item8,
            pest_data.green_nonirm_item9, pest_data.green_nonirm_item10
        ])
        
        pest_data.locule_irm_average = calculate_average([
            pest_data.locule_irm_item1, pest_data.locule_irm_item2,
            pest_data.locule_irm_item3, pest_data.locule_irm_item4,
            pest_data.locule_irm_item5, pest_data.locule_irm_item6,
            pest_data.locule_irm_item7, pest_data.locule_irm_item8,
            pest_data.locule_irm_item9, pest_data.locule_irm_item10
        ])
        
        pest_data.locule_nonirm_average = calculate_average([
            pest_data.locule_nonirm_item1, pest_data.locule_nonirm_item2,
            pest_data.locule_nonirm_item3, pest_data.locule_nonirm_item4,
            pest_data.locule_nonirm_item5, pest_data.locule_nonirm_item6,
            pest_data.locule_nonirm_item7, pest_data.locule_nonirm_item8,
            pest_data.locule_nonirm_item9, pest_data.locule_nonirm_item10
        ])
        
        pest_data.open_ball_irm_average = calculate_average([
            pest_data.open_ball_irm_item1, pest_data.open_ball_irm_item2,
            pest_data.open_ball_irm_item3, pest_data.open_ball_irm_item4,
            pest_data.open_ball_irm_item5, pest_data.open_ball_irm_item6,
            pest_data.open_ball_irm_item7, pest_data.open_ball_irm_item8,
            pest_data.open_ball_irm_item9, pest_data.open_ball_irm_item10
        ])
        
        pest_data.open_ball_nonirm_average = calculate_average([
            pest_data.open_ball_nonirm_item1, pest_data.open_ball_nonirm_item2,
            pest_data.open_ball_nonirm_item3, pest_data.open_ball_nonirm_item4,
            pest_data.open_ball_nonirm_item5, pest_data.open_ball_nonirm_item6,
            pest_data.open_ball_nonirm_item7, pest_data.open_ball_nonirm_item8,
            pest_data.open_ball_nonirm_item9, pest_data.open_ball_nonirm_item10
        ])
        
        pest_data.pheromone_irm_average = calculate_average([
            pest_data.pheromone_irm_item1, pest_data.pheromone_irm_item2,
            pest_data.pheromone_irm_item3, pest_data.pheromone_irm_item4,
            pest_data.pheromone_irm_item5, pest_data.pheromone_irm_item6,
            pest_data.pheromone_irm_item7, pest_data.pheromone_irm_item8,
            pest_data.pheromone_irm_item9, pest_data.pheromone_irm_item10
        ])
        
        pest_data.pheromone_nonirm_average = calculate_average([
            pest_data.pheromone_nonirm_item1, pest_data.pheromone_nonirm_item2,
            pest_data.pheromone_nonirm_item3, pest_data.pheromone_nonirm_item4,
            pest_data.pheromone_nonirm_item5, pest_data.pheromone_nonirm_item6,
            pest_data.pheromone_nonirm_item7, pest_data.pheromone_nonirm_item8,
            pest_data.pheromone_nonirm_item9, pest_data.pheromone_nonirm_item10
        ])
        
        pest_data.incidence_irm_average = calculate_average([
            pest_data.incidence_irm_item1, pest_data.incidence_irm_item2,
            pest_data.incidence_irm_item3, pest_data.incidence_irm_item4,
            pest_data.incidence_irm_item5, pest_data.incidence_irm_item6,
            pest_data.incidence_irm_item7, pest_data.incidence_irm_item8,
            pest_data.incidence_irm_item9, pest_data.incidence_irm_item10
        ])
        
        pest_data.incidence_nonirm_average = calculate_average([
            pest_data.incidence_nonirm_item1, pest_data.incidence_nonirm_item2,
            pest_data.incidence_nonirm_item3, pest_data.incidence_nonirm_item4,
            pest_data.incidence_nonirm_item5, pest_data.incidence_nonirm_item6,
            pest_data.incidence_nonirm_item7, pest_data.incidence_nonirm_item8,
            pest_data.incidence_nonirm_item9, pest_data.incidence_nonirm_item10
        ])
        
        pest_data.locular_damage_irm_average = calculate_average([
            pest_data.locular_damage_irm1, pest_data.locular_damage_irm2,
            pest_data.locular_damage_irm3, pest_data.locular_damage_irm4,
            pest_data.locular_damage_irm5, pest_data.locular_damage_irm6,
            pest_data.locular_damage_irm7, pest_data.locular_damage_irm8,
            pest_data.locular_damage_irm9, pest_data.locular_damage_irm10
        ])
        
        pest_data.locular_damage_nonirm_average = calculate_average([
            pest_data.locular_damage_nonirm1, pest_data.locular_damage_nonirm2,
            pest_data.locular_damage_nonirm3, pest_data.locular_damage_nonirm4,
            pest_data.locular_damage_nonirm5, pest_data.locular_damage_nonirm6,
            pest_data.locular_damage_nonirm7, pest_data.locular_damage_nonirm8,
            pest_data.locular_damage_nonirm9, pest_data.locular_damage_nonirm10
        ])

        # Save the updated data
        pest_data.save()

        return redirect('detailed_report', district_name=district_name, month=month)

    else:
        # Pre-fill the data to display in the template
        initial_data = {
            'jassid_irm': [
                pest_data.jassid_irm_item1,
                pest_data.jassid_irm_item2,
                pest_data.jassid_irm_item3,
                pest_data.jassid_irm_item4,
                pest_data.jassid_irm_item5,
                pest_data.jassid_irm_item6,
                pest_data.jassid_irm_item7,
                pest_data.jassid_irm_item8,
                pest_data.jassid_irm_item9,
                pest_data.jassid_irm_item10,
            ],
            'jassid_nonirm': [
                pest_data.jassid_nonirm_item1,
                pest_data.jassid_nonirm_item2,
                pest_data.jassid_nonirm_item3,
                pest_data.jassid_nonirm_item4,
                pest_data.jassid_nonirm_item5,
                pest_data.jassid_nonirm_item6,
                pest_data.jassid_nonirm_item7,
                pest_data.jassid_nonirm_item8,
                pest_data.jassid_nonirm_item9,
                pest_data.jassid_nonirm_item10,
            ],
            'whitefly_irm': [
                pest_data.whitefly_irm_item1,
                pest_data.whitefly_irm_item2,
                pest_data.whitefly_irm_item3,
                pest_data.whitefly_irm_item4,
                pest_data.whitefly_irm_item5,
                pest_data.whitefly_irm_item6,
                pest_data.whitefly_irm_item7,
                pest_data.whitefly_irm_item8,
                pest_data.whitefly_irm_item9,
                pest_data.whitefly_irm_item10,
            ],
            'whitefly_nonirm': [
                pest_data.whitefly_nonirm_item1,
                pest_data.whitefly_nonirm_item2,
                pest_data.whitefly_nonirm_item3,
                pest_data.whitefly_nonirm_item4,
                pest_data.whitefly_nonirm_item5,
                pest_data.whitefly_nonirm_item6,
                pest_data.whitefly_nonirm_item7,
                pest_data.whitefly_nonirm_item8,
                pest_data.whitefly_nonirm_item9,
                pest_data.whitefly_nonirm_item10,
            ],
            'thrips_irm': [
                pest_data.thrips_irm_item1,
                pest_data.thrips_irm_item2,
                pest_data.thrips_irm_item3,
                pest_data.thrips_irm_item4,
                pest_data.thrips_irm_item5,
                pest_data.thrips_irm_item6,
                pest_data.thrips_irm_item7,
                pest_data.thrips_irm_item8,
                pest_data.thrips_irm_item9,
                pest_data.thrips_irm_item10,
            ],
            'thrips_nonirm': [
                pest_data.thrips_nonirm_item1,
                pest_data.thrips_nonirm_item2,
                pest_data.thrips_nonirm_item3,
                pest_data.thrips_nonirm_item4,
                pest_data.thrips_nonirm_item5,
                pest_data.thrips_nonirm_item6,
                pest_data.thrips_nonirm_item7,
                pest_data.thrips_nonirm_item8,
                pest_data.thrips_nonirm_item9,
                pest_data.thrips_nonirm_item10,
            ],
            'flowers_irm': [
                pest_data.flowers_irm_item1,
                pest_data.flowers_irm_item2,
                pest_data.flowers_irm_item3,
                pest_data.flowers_irm_item4,
                pest_data.flowers_irm_item5,
                pest_data.flowers_irm_item6,
                pest_data.flowers_irm_item7,
                pest_data.flowers_irm_item8,
                pest_data.flowers_irm_item9,
                pest_data.flowers_irm_item10,
            ],
            'flowers_nonirm': [
                pest_data.flowers_nonirm_item1,
                pest_data.flowers_nonirm_item2,
                pest_data.flowers_nonirm_item3,
                pest_data.flowers_nonirm_item4,
                pest_data.flowers_nonirm_item5,
                pest_data.flowers_nonirm_item6,
                pest_data.flowers_nonirm_item7,
                pest_data.flowers_nonirm_item8,
                pest_data.flowers_nonirm_item9,
                pest_data.flowers_nonirm_item10,
            ],
            'locule_irm': [
                pest_data.locule_irm_item1,
                pest_data.locule_irm_item2,
                pest_data.locule_irm_item3,
                pest_data.locule_irm_item4,
                pest_data.locule_irm_item5,
                pest_data.locule_irm_item6,
                pest_data.locule_irm_item7,
                pest_data.locule_irm_item8,
                pest_data.locule_irm_item9,
                pest_data.locule_irm_item10,
            ],
            'locule_nonirm': [
                pest_data.locule_nonirm_item1,
                pest_data.locule_nonirm_item2,
                pest_data.locule_nonirm_item3,
                pest_data.locule_nonirm_item4,
                pest_data.locule_nonirm_item5,
                pest_data.locule_nonirm_item6,
                pest_data.locule_nonirm_item7,
                pest_data.locule_nonirm_item8,
                pest_data.locule_nonirm_item9,
                pest_data.locule_nonirm_item10,
            ],
            'pheromone_irm': [
                pest_data.pheromone_irm_item1,
                pest_data.pheromone_irm_item2,
                pest_data.pheromone_irm_item3,
                pest_data.pheromone_irm_item4,
                pest_data.pheromone_irm_item5,
                pest_data.pheromone_irm_item6,
                pest_data.pheromone_irm_item7,
                pest_data.pheromone_irm_item8,
                pest_data.pheromone_irm_item9,
                pest_data.pheromone_irm_item10,
            ],
            'pheromone_nonirm': [
                pest_data.pheromone_nonirm_item1,
                pest_data.pheromone_nonirm_item2,
                pest_data.pheromone_nonirm_item3,
                pest_data.pheromone_nonirm_item4,
                pest_data.pheromone_nonirm_item5,
                pest_data.pheromone_nonirm_item6,
                pest_data.pheromone_nonirm_item7,
                pest_data.pheromone_nonirm_item8,
                pest_data.pheromone_nonirm_item9,
                pest_data.pheromone_nonirm_item10,
            ],
            'green_irm': [
                pest_data.green_irm_item1,
                pest_data.green_irm_item2,
                pest_data.green_irm_item3,
                pest_data.green_irm_item4,
                pest_data.green_irm_item5,
                pest_data.green_irm_item6,
                pest_data.green_irm_item7,
                pest_data.green_irm_item8,
                pest_data.green_irm_item9,
                pest_data.green_irm_item10,
            ],
            'green_nonirm': [
                pest_data.green_nonirm_item1,
                pest_data.green_nonirm_item2,
                pest_data.green_nonirm_item3,
                pest_data.green_nonirm_item4,
                pest_data.green_nonirm_item5,
                pest_data.green_nonirm_item6,
                pest_data.green_nonirm_item7,
                pest_data.green_nonirm_item8,
                pest_data.green_nonirm_item9,
                pest_data.green_nonirm_item10,
            ],
            'incidence_irm': [
                pest_data.incidence_irm_item1,
                pest_data.incidence_irm_item2,
                pest_data.incidence_irm_item3,
                pest_data.incidence_irm_item4,
                pest_data.incidence_irm_item5,
                pest_data.incidence_irm_item6,
                pest_data.incidence_irm_item7,
                pest_data.incidence_irm_item8,
                pest_data.incidence_irm_item9,
                pest_data.incidence_irm_item10,
            ],
            'incidence_nonirm': [
                pest_data.incidence_nonirm_item1,
                pest_data.incidence_nonirm_item2,
                pest_data.incidence_nonirm_item3,
                pest_data.incidence_nonirm_item4,
                pest_data.incidence_nonirm_item5,
                pest_data.incidence_nonirm_item6,
                pest_data.incidence_nonirm_item7,
                pest_data.incidence_nonirm_item8,
                pest_data.incidence_nonirm_item9,
                pest_data.incidence_nonirm_item10,
            ],
            'locular_damage_irm': [
                pest_data.locular_damage_irm1,
                pest_data.locular_damage_irm2,
                pest_data.locular_damage_irm3,
                pest_data.locular_damage_irm4,
                pest_data.locular_damage_irm5,
                pest_data.locular_damage_irm6,
                pest_data.locular_damage_irm7,
                pest_data.locular_damage_irm8,
                pest_data.locular_damage_irm9,
                pest_data.locular_damage_irm10,
            ],
            'locular_damage_nonirm': [
                pest_data.locular_damage_nonirm1,
                pest_data.locular_damage_nonirm2,
                pest_data.locular_damage_nonirm3,
                pest_data.locular_damage_nonirm4,
                pest_data.locular_damage_nonirm5,
                pest_data.locular_damage_nonirm6,
                pest_data.locular_damage_nonirm7,
                pest_data.locular_damage_nonirm8,
                pest_data.locular_damage_nonirm9,
                pest_data.locular_damage_nonirm10,
            ],
            'open_ball_irm': [
                pest_data.open_ball_irm_item1,
                pest_data.open_ball_irm_item2,
                pest_data.open_ball_irm_item3,
                pest_data.open_ball_irm_item4,
                pest_data.open_ball_irm_item5,
                pest_data.open_ball_irm_item6,
                pest_data.open_ball_irm_item7,
                pest_data.open_ball_irm_item8,
                pest_data.open_ball_irm_item9,
                pest_data.open_ball_irm_item10,
            ],
            'open_ball_nonirm': [
                pest_data.open_ball_nonirm_item1,
                pest_data.open_ball_nonirm_item2,
                pest_data.open_ball_nonirm_item3,
                pest_data.open_ball_nonirm_item4,
                pest_data.open_ball_nonirm_item5,
                pest_data.open_ball_nonirm_item6,
                pest_data.open_ball_nonirm_item7,
                pest_data.open_ball_nonirm_item8,
                pest_data.open_ball_nonirm_item9,
                pest_data.open_ball_nonirm_item10,
            ],
            
        }

    context = {
        'district_name': district_name,
        'month': month,
        'week_number': week_number,
        'standard_week': standard_week,
        'pest_data': pest_data,
        'initial_data': initial_data  # to pass to template if needed
    }
    return render(request, 'owner/update_pest_incidence.html', context)


def calculate_average(items):
    print('calculate_averagecalculate_averagecalculate_averagecalculate_average')
    # Convert items to float and filter out zeros
    valid_items = [float(item) for item in items if item and float(item) != 0]
    # Calculate average
    average = sum(valid_items) / len(valid_items) if valid_items else None
    return average



# Weekly report for admin  (In disscusstion because monthly and weekly same)
@login_required(login_url='/login/')
def admin_weeks(request,district_name):
    week = standard_weeks.objects.all().annotate(
            standard_number_int=Cast('standard_number', IntegerField())
        ).order_by('standard_number_int')

    # week = standard_weeks.objects.all().order_by('standard_number')

    context={
    'week':week,
    'district_name':district_name,
    }
    return render(request, 'owner/admin_weeks.html', context)


def weekly_pestincident_admin(request,district_name,standard_number):
    standard_weeks_data = standard_weeks.objects.filter(standard_number=standard_number)

    print('standard_weeks_data',standard_weeks_data)

    # Initialize a dictionary to hold week-wise averages
    weekwise_averages = {}

    for standard in standard_weeks_data:
        # Filter pest incidence data where week matches the standard number
        pest_data = pest_incidence_data.objects.filter(week=standard_number,district=district_name)

        print('pest_data',pest_data)

        # Calculate the averages
        averages = pest_data.aggregate(
            avg_jassid_irm=Avg('jassid_irm_average'),
            avg_jassid_nonirm=Avg('jassid_nonirm_average'),
            avg_whitefly_irm=Avg('whitefly_irm_average'),
            avg_whitefly_nonirm=Avg('whitefly_nonirm_average'),
            avg_thrips_irm=Avg('thrips_irm_average'),
            avg_thrips_nonirm=Avg('thrips_nonirm_average'),
            avg_flowers_irm=Avg('flowers_irm_average'),
            avg_flowers_nonirm=Avg('flowers_nonirm_average'),
            avg_green_irm=Avg('green_irm_average'),
            avg_green_nonirm=Avg('green_nonirm_average'),
            avg_locule_irm=Avg('locule_irm_average'),
            avg_locule_nonirm=Avg('locule_nonirm_average'),
            avg_open_ball_irm=Avg('open_ball_irm_average'),
            avg_open_ball_nonirm= Avg('open_ball_nonirm_average'),
            avg_pheromone_irm=Avg('pheromone_irm_average'),
            avg_pheromone_nonirm=Avg('pheromone_nonirm_average'),
            avg_incidence_irm=Avg('incidence_irm_average'),
            avg_incidence_nonirm=Avg('incidence_nonirm_average'),
            avg_locular_damage_irm=Avg('locular_damage_irm_average'),
            avg_locular_damage_nonirm=Avg('locular_damage_nonirm_average')

        )

        # Store in the dictionary
        # weekwise_averages[standard.standard_week] = averages
        weekwise_averages[(standard.standard_number, standard.standard_week)] = averages

    print('weekwise_averages',weekwise_averages)

    context={
    'weekwise_averages':weekwise_averages,
    }

    return render(request,'owner/weekly_pestincident_admin.html',context)

# End Weekly report for admin  (In disscusstion because monthly and weekly same)



# Yearly report for Admin

@login_required(login_url='/login/')
def admin_year(request,district_name):
    year_data = standard_weeks.objects.values('year').distinct().order_by('year')

    print('yearyearyearyearyearyearyearyearyearyear',year_data)

    # Prepare a list to store year and availability of data
    year_data_availability = []
    
    for year_obj in year_data:
        year = year_obj['year']
        
        # Check if there is any data in YearlyProgressReport for the given year and district
        data = YearlyProgressReport.objects.filter(
            district=district_name,
            date_field__year=year
        )
        
        # Store the year and whether data exists
        year_data_availability.append({
            'year': year,
            'has_data': data.exists()  # Check if the queryset is not empty
        })

    # Debugging output
    print('year_data_availability', year_data_availability)



    context={
    'year':year_data,
    'district_name':district_name,
    'year_data_availability':year_data_availability
    }
    return render(request, 'admin/admin_year.html', context)


@login_required(login_url='/login/')
def yearly_admin_report(request,district_name,year):
    # Latest FY fallback
    fy_obj = Financial_Year.objects.order_by('-id').first()
    selected_fin_year = request.session.get(
        'financial_year',
        fy_obj.financial_year if fy_obj else '2024-2025'
    )

    # 'YYYY-YYYY' -> start/end dates (01-Apr to 31-Mar)
    try:
        start_year, end_year = map(int, selected_fin_year.split('-'))
    except Exception:
        # Safety fallback
        start_year, end_year = 2024, 2025
        selected_fin_year = '2024-2025'

    fy_start = date(start_year, 4, 1)   # 01-Apr
    fy_end   = date(end_year, 3, 31)    # 31-Mar

    # Filter by district + FY range
    yearly_data = (
        YearlyProgressReport.objects
        .filter(district=district_name, date_field__range=(fy_start, fy_end))
        .order_by('-date_field', '-id')
    )

    # yearly_data = YearlyProgressReport.objects.filter(
    #     district=district_name,
    #     date_field__year=year,
    # )

    print('yearly_data',yearly_data)

    context={
    'yearly_data':yearly_data
    }
    return render(request,'admin/yearly_admin_report.html',context)



# Yearly report for Super Admin


@login_required(login_url='/')
def yearly_district(request):
    dis=district.objects.all().order_by('district_name')
    context={
        'dis':dis,
    }
    return render(request,'owner/yearly_district.html',context)

@login_required(login_url='/')
def superadmin_year(request,district_name):
    year_data = standard_weeks.objects.values('year').distinct().order_by('year')

    print('yearyearyearyearyearyearyearyearyearyear',year_data)

    # Prepare a list to store year and availability of data
    year_data_availability = []
    
    for year_obj in year_data:
        year = year_obj['year']
        
        # Check if there is any data in YearlyProgressReport for the given year and district
        data = YearlyProgressReport.objects.filter(
            district=district_name,
            date_field__year=year
        )
        
        # Store the year and whether data exists
        year_data_availability.append({
            'year': year,
            'has_data': data.exists()  # Check if the queryset is not empty
        })

    # Debugging output
    print('year_data_availability', year_data_availability)


    context={
    'year':year_data,
    'district_name':district_name,
    'year_data_availability': year_data_availability,
    }
    return render(request,'owner/superadmin_year.html',context)


# @login_required(login_url='/')
# def yearly_super_report(request,district_name,year):
#     yearly = YearlyProgressReport.objects.all()

#     yearly_data = YearlyProgressReport.objects.filter(
#         district=district_name,
#         date_field__year=year,
#     )

#     print('yearly_data',yearly_data)

#     context={
#     'yearly_data':yearly_data
#     }
#     return render(request,'owner/yearly_super_report.html',context)



@login_required(login_url='/')
def yearly_super_report(request, district_name, year):
    # Latest FY fallback
    fy_obj = Financial_Year.objects.order_by('-id').first()
    selected_fin_year = request.session.get(
        'financial_year',
        fy_obj.financial_year if fy_obj else '2024-2025'
    )

    # 'YYYY-YYYY' -> start/end dates (01-Apr to 31-Mar)
    try:
        start_year, end_year = map(int, selected_fin_year.split('-'))
    except Exception:
        # Safety fallback
        start_year, end_year = 2024, 2025
        selected_fin_year = '2024-2025'

    fy_start = date(start_year, 4, 1)   # 01-Apr
    fy_end   = date(end_year, 3, 31)    # 31-Mar

    # Filter by district + FY range
    yearly_data = (
        YearlyProgressReport.objects
        .filter(district=district_name, date_field__range=(fy_start, fy_end))
        .order_by('-date_field', '-id')
    )

    context = {
        'yearly_data': yearly_data,
        'district_name': district_name,
        'selected_fin_year': selected_fin_year,
        'fy_start': fy_start,
        'fy_end': fy_end,
    }
    return render(request, 'owner/yearly_super_report.html', context)




#API's for Pest Incidence data :Aparna TO DO LIST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import pest_incidence_data
from .serializers import PestIncidenceDataSerializer

class PestIncidenceDataListCreateAPIView(APIView):
    def get(self, request):
        pest_data = pest_incidence_data.objects.all()
        serializer = PestIncidenceDataSerializer(pest_data, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PestIncidenceDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PestIncidenceDataDetailAPIView(APIView):
    def get(self, request, pk):
        pest_data = get_object_or_404(pest_incidence_data, pk=pk)
        serializer = PestIncidenceDataSerializer(pest_data)
        return Response(serializer.data, status=status.HTTP_200_OK)




class MonthlyPhysicalProgressListCreateAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        progresses = monthly_physical_progress.objects.all()
        serializer = MonthlyPhysicalProgressSerializer(progresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MonthlyPhysicalProgressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# aparna: TO DO LIST : for edit/delete api monthly_physical_progress : 
class MonthlyPhysicalProgressDetailAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return monthly_physical_progress.objects.get(pk=pk)
        except monthly_physical_progress.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        progress = self.get_object(pk)
        serializer = MonthlyPhysicalProgressSerializer(progress)
        return Response(serializer.data)

    def put(self, request, pk):
        progress = self.get_object(pk)
        serializer = MonthlyPhysicalProgressSerializer(progress, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        progress = self.get_object(pk)
        progress.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ExtensionActivitiesListCreateAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        activities = extension_activities_carried_out.objects.all()
        serializer = ExtensionActivitiesSerializer(activities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExtensionActivitiesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# aparna: TO DO LIST : for edit/delete api extension_activities_carried_out :
class ExtensionActivitiesDetailAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return extension_activities_carried_out.objects.get(pk=pk)
        except extension_activities_carried_out.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        activity = self.get_object(pk)
        serializer = ExtensionActivitiesSerializer(activity)
        return Response(serializer.data)

    def put(self, request, pk):
        activity = self.get_object(pk)
        serializer = ExtensionActivitiesSerializer(activity, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        activity = self.get_object(pk)
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
