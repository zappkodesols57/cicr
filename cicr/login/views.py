from django.shortcuts import render
from django.urls import reverse
# Create your views here.
from django.db.models import Q
from django.shortcuts import render
from django.db.models import Q, Count


# login/views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout

import random
import string
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import User, investigator_user
from login.models import User as CustomUser

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from investigator_app.models import district  # Import your district model
from investigator_app.models import *

from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.conf import settings
from django.http import FileResponse, Http404
from pathlib import Path
import mimetypes
from django.db.models import Avg
from owner_settings.models import *

from datetime import datetime
from django.db.models import Count, Case, When, IntegerField

from login.models import User as CustomUser


def change_financial_year(request):
    financial_year = request.GET.get('financial_year')  # This is the year_id from dropdown
    print('financial_year', financial_year)
    
    try:
        year = Financial_Year.objects.get(financial_year=financial_year)
        print('financial_year:', year.financial_year)

        # ✅ Store both ID and readable year name in session
        request.session['financial_year'] = year.financial_year

    except Financial_Year.DoesNotExist:
        print("Invalid financial year selected.")

    return redirect(request.META.get('HTTP_REFERER', '/'))


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'csrfToken': request.META.get('CSRF_COOKIE')})



MONTH_ORDER = [
    'January', 'February', 'March', 'April', 'May', 'June', 
    'July', 'August', 'September', 'October', 'November', 'December'
]


def super_login(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        password = request.POST['password']
        user = authenticate(request, username=user_id, password=password)

        if user is None:
            return render(request, 'login/admin_login.html', {'error_message': 'Invalid login credentials.'})

        is_super_admin = (
            user.is_active
            and user.is_superuser
            and not getattr(user, 'is_admin', False)
            and not getattr(user, 'is_investigator', False)
            and not getattr(user, 'is_farmer', False)
        )
        if not is_super_admin:
            return render(request, 'login/admin_login.html', {'error_message': 'Only super admin users can login here.'})

        login(request, user)
        return redirect('/super_dashboard/')
    return render(request, 'login/admin_login.html')


def web_app(request):
    return render(request, 'home.html')


def cotton_web_app(request):
    cotton_root = Path(settings.BASE_DIR).parent / "CICR-Cotton-webapp"
    index_path = cotton_root / "index.html"
    if not index_path.exists():
        raise Http404("CICR Cotton web app not found")
    return FileResponse(index_path.open("rb"), content_type="text/html")


def cotton_web_asset(request, asset_path):
    cotton_root = (Path(settings.BASE_DIR).parent / "CICR-Cotton-webapp").resolve()
    target_path = (cotton_root / asset_path).resolve()
    if cotton_root not in target_path.parents:
        raise Http404("CICR Cotton web app asset not found")
    if not target_path.is_file():
        index_path = cotton_root / "index.html"
        if index_path.exists():
            return FileResponse(index_path.open("rb"), content_type="text/html")
        raise Http404("CICR Cotton web app route not found")
    content_type = mimetypes.guess_type(str(target_path))[0] or "application/octet-stream"
    return FileResponse(target_path.open("rb"), content_type=content_type)


def web_panel_logout(request):
    logout(request)
    return redirect("/web_app/")


# comment on 30july 2025 after implement financial year functionality

# @login_required(login_url='/')
# def super_dashboard(request):
#     user= request.user
#     basic_survey_data = (basic_servey_info.objects
#                          .values('district')
#                          .annotate(count=Count('id'))
#                          .order_by('district'))
    
#     # Get data for all districts from pest_incidence_data
#     pest_data = (pest_incidence_data.objects
#                  .values('district')
#                  .annotate(count=Count('id'))
#                  .order_by('district'))
    
#     # Create a dictionary for district counts
#     district_counts = {}
#     for item in basic_survey_data:
#         district_counts[item['district']] = {'surveys': item['count'], 'reports': 0}
    
#     for item in pest_data:
#         if item['district'] in district_counts:
#             district_counts[item['district']]['reports'] = item['count']
#         else:
#             district_counts[item['district']] = {'surveys': 0, 'reports': item['count']}
    
#     # Prepare data for Google Chart
#     chart_data = [["District", "Surveys", "Weekly Reports"]]
#     for district, counts in district_counts.items():
#         chart_data.append([district, counts['surveys'], counts['reports']])
    

#     # print('chart_data',chart_data)
#     # Pass data to template


#     basic_survey_data1 = (
#         basic_servey_info.objects
#         .values('district')
#         .annotate(
#             irm_count=Count(Case(When(IRM=True, then=1), output_field=IntegerField())),
#             non_irm_count=Count(Case(When(IRM=False, then=1), output_field=IntegerField()))
#         )
#         .order_by('district')
#     )


#     # print('basic_survey_data1',basic_survey_data1)

#     # data = pest_incidence_data.objects.values('district').annotate(
#     #     irm_avg=models.Avg('jassid_irm_average') + models.Avg('whitefly_irm_average') + models.Avg('thrips_irm_average') + models.Avg('flowers_irm_average'),
#     #     non_irm_avg=models.Avg('jassid_nonirm_average') + models.Avg('whitefly_nonirm_average') + models.Avg('thrips_nonirm_average') + models.Avg('flowers_nonirm_average')
#     # )
    
#     # # Converting the data into a format that can be used by Google Charts
#     # chart_data1 = {
#     #     'data': list(data)
#     # }
#     # print('chart_data1',chart_data1)

#     district_counts = pest_incidence_data.objects.values('district').annotate(count=Count('id')).order_by('district')
#     # print('district_counts',district_counts)


#     # Get distinct districts
#     district_details = CustomUser.objects.filter(~Q(user_district='')).values('user_district').distinct()

#     # Get investigator count for each district with ordering
#     investigator_details = CustomUser.objects.filter(~Q(user_district=''), is_investigator=True).values('user_district').annotate(investigator_count=Count('user_district')).order_by('user_district')

#     # Get admin count for each district with ordering
#     admin_details = CustomUser.objects.filter(~Q(user_district=''), is_admin=True).values('user_district').annotate(admin_count=Count('user_district')).order_by('user_district')

#     # Combine the data into a list of dictionaries
#     combined_data = []
#     for district in district_details:
#         district_name = district['user_district']
        
#         # Use order_by and first() to get the counts
#         investigator_count = investigator_details.filter(user_district=district_name).order_by('user_district').first()['investigator_count'] if investigator_details.filter(user_district=district_name).exists() else 0
#         admin_count = admin_details.filter(user_district=district_name).order_by('user_district').first()['admin_count'] if admin_details.filter(user_district=district_name).exists() else 0
        
#         combined_data.append({
#             'district': district_name,
#             'investigators': investigator_count,
#             'admins': admin_count,
#         })


#     print('combined_data',combined_data)

#     context = {
#         'chart_data': chart_data,
#         'survey_data': basic_survey_data1,
#         'district_counts':district_counts,
#         'combined_data':combined_data,
#     }
#     return render(request, 'login/super_dashboard.html',context)



@login_required(login_url='/')
def super_dashboard(request):
    financial_years = Financial_Year.objects.order_by('-id').first()
    # financial_years = Financial_Year.objects.last()
    print('financial_years',financial_years,financial_years.financial_year)
    selected_fin_year = request.session.get('financial_year',financial_years.financial_year)
    
    print('financial_yearfinancial_year====',selected_fin_year)
    
    # Step 1: Get selected financial year from GET or default to 2024-2025
    # selected_fin_year = request.GET.get('fin_year', '2024-2025')
    start_year, end_year = map(int, selected_fin_year.split('-'))
    start_date = date(start_year, 4, 1)
    end_date = date(end_year, 3, 31)

    print('start_date========',start_date,end_date)
    
    # Step 2: Filter survey and pest data based on financial year
    basic_survey_data = (
        basic_servey_info.objects
        .filter(servey_date__range=(start_date, end_date))
        .values('district')
        .annotate(count=Count('id'))
        .order_by('district')
    )
    print('basic_survey_data new',len(basic_survey_data))

    pest_data = (
        pest_incidence_data.objects
        .filter(date_field__range=(start_date, end_date))
        .values('district')
        .annotate(count=Count('id'))
        .order_by('district')
    )

    # Step 3: Merge counts by district
    district_counts = {}
    for item in basic_survey_data:
        district_counts[item['district']] = {'surveys': item['count'], 'reports': 0}

    for item in pest_data:
        if item['district'] in district_counts:
            district_counts[item['district']]['reports'] = item['count']
        else:
            district_counts[item['district']] = {'surveys': 0, 'reports': item['count']}

    # Step 4: Prepare data for Google Chart
    chart_data = [["District", "Surveys", "Weekly Reports"]]
    for district, counts in district_counts.items():
        chart_data.append([district, counts['surveys'], counts['reports']])

    # Step 5: IRM / NON-IRM survey counts (filtered by financial year)
    basic_survey_data1 = (
        basic_servey_info.objects
        .filter(servey_date__range=(start_date, end_date))
        .values('district')
        .annotate(
            irm_count=Count(Case(When(IRM=True, then=1), output_field=IntegerField())),
            non_irm_count=Count(Case(When(IRM=False, then=1), output_field=IntegerField()))
        )
        .order_by('district')
    )

    # Step 6: District-wise weekly pest report counts
    district_counts = (
        pest_incidence_data.objects
        .filter(date_field__range=(start_date, end_date))
        .values('district')
        .annotate(count=Count('id'))
        .order_by('district')
    )

    # Step 7: Investigator and Admin user counts per district
    district_details = CustomUser.objects.filter(~Q(user_district='')).values('user_district').distinct()

    investigator_details = (
        CustomUser.objects
        .filter(~Q(user_district=''), is_investigator=True)
        .values('user_district')
        .annotate(investigator_count=Count('user_district'))
        .order_by('user_district')
    )

    admin_details = (
        CustomUser.objects
        .filter(~Q(user_district=''), is_admin=True)
        .values('user_district')
        .annotate(admin_count=Count('user_district'))
        .order_by('user_district')
    )

    # Step 8: Combine admin + investigator count for each district
    combined_data = []
    for district in district_details:
        district_name = district['user_district']
        investigator_count = (
            investigator_details.filter(user_district=district_name).first()['investigator_count']
            if investigator_details.filter(user_district=district_name).exists() else 0
        )
        admin_count = (
            admin_details.filter(user_district=district_name).first()['admin_count']
            if admin_details.filter(user_district=district_name).exists() else 0
        )
        combined_data.append({
            'district': district_name,
            'investigators': investigator_count,
            'admins': admin_count,
        })

    context = {
        'chart_data': chart_data,
        'survey_data': basic_survey_data1,
        'district_counts': district_counts,
        'combined_data': combined_data,
        'selected_fin_year': selected_fin_year,
    }
    return render(request, 'login/super_dashboard.html', context)


@login_required(login_url='/login_investigator/')
def investigator_dashboard(request):
    return render(request, 'login/investigator_dashboard.html', {
        'investigator_id': request.user.user_id,
        'investigator_district': request.user.user_district or '',
    })


@login_required(login_url='/login_investigator/')
def investigator_basic_survey(request):
    return render(request, 'login/investigator_basic_survey.html', {
        'investigator_id': request.user.user_id,
        'investigator_district': request.user.user_district or '',
    })


@login_required(login_url='/login_investigator/')
def investigator_weekly_report(request):
    return render(request, 'login/investigator_weekly_report.html', {
        'investigator_id': request.user.user_id,
        'investigator_district': request.user.user_district or '',
    })


@login_required(login_url='/login_investigator/')
def investigator_monthly_progress(request):
    return redirect('/investigator/monthly-progress/physical/')


@login_required(login_url='/login_investigator/')
def investigator_physical_progress(request):
    return render(request, 'login/investigator_physical_progress.html', {
        'investigator_id': request.user.user_id,
        'investigator_district': request.user.user_district or '',
    })


@login_required(login_url='/login_investigator/')
def investigator_extension_activities(request):
    return render(request, 'login/investigator_extension_activities.html', {
        'investigator_id': request.user.user_id,
        'investigator_district': request.user.user_district or '',
    })


@login_required(login_url='/login_investigator/')
def investigator_representative_photographs(request):
    return render(request, 'login/investigator_representative_photographs.html', {
        'investigator_id': request.user.user_id,
        'investigator_district': request.user.user_district or '',
    })


@login_required(login_url='/login_investigator/')
def investigator_assessment_season(request):
    return render(request, 'login/investigator_assessment_season.html', {
        'investigator_id': request.user.user_id,
        'investigator_district': request.user.user_district or '',
    })


@login_required(login_url='/login_investigator/')
def investigator_yearly_progress(request):
    return render(request, 'login/investigator_yearly_progress.html', {
        'investigator_id': request.user.user_id,
        'investigator_district': request.user.user_district or '',
    })


@login_required(login_url='/login_investigator/')
def investigator_manage_surveys(request):
    return render(request, 'login/investigator_manage_surveys.html', {
        'investigator_id': request.user.user_id,
        'investigator_district': request.user.user_district or '',
    })


@login_required(login_url='/login_investigator/')
def investigator_manage_reports(request):
    return render(request, 'login/investigator_manage_reports.html', {
        'investigator_id': request.user.user_id,
        'investigator_district': request.user.user_district or '',
    })

@login_required(login_url='/super_login/')
def logout_view(request):
    logout(request)
    return redirect("/")

@login_required(login_url='/login/')
def logout_admin(request):
    logout(request)
    return redirect("/login/")

from django.contrib.auth.models import User
import string
import random

# def generate_username(first_name, last_name):
#     # Generate username starting with "CICR" in capital letters
#     prefix = "CICR"
    
#     # First letter of first name and last name in lowercase
#     initials = f"{first_name[:1].upper()}{last_name[:1].upper()}"
    
#     # Random suffix of 4 digits
#     random_suffix = ''.join(random.choices(string.digits, k=4))
    
#     # Combine prefix, initials, and random suffix
#     username = f"{prefix}{initials}{random_suffix}"
    
#     # Ensure username is unique; add more randomness if necessary
#     while CustomUser.objects.filter(user_id=username).exists():
#         random_suffix = ''.join(random.choices(string.digits, k=4))
#         username = f"{prefix}{initials}{random_suffix}"
    
#     return username

def generate_username(first_name):
    base_username = f"{first_name.lower()}"
    username = f"{base_username}@01"

    counter = 1
    while CustomUser.objects.filter(user_id=username).exists():
        counter += 1
        username = f"{base_username}@{counter:02}"
    print('username',username)
    return username


# def generate_password():
#     characters = string.ascii_letters + string.digits
#     password = ''.join(random.choice(characters) for i in range(6))
#     return password

# def generate_password(first_name, last_name, counter):
#     first_name_lower = first_name.lower()
#     last_initial_lower = last_name[0].lower()
#     password = f"{first_name_lower}.{last_initial_lower}@{counter:02}"
#     print('passwordpassword',password)
#     return password


def generate_password(first_name, counter):
    first_name_lower = first_name.lower()
    password = f"{first_name_lower}@{counter:02}"
    print('passwordpassword',password)
    return password


@login_required(login_url='/login/')
def create_investigator(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        email_id = request.POST.get('email_id')
        mobile_number = request.POST.get('mobile_number')
        address = request.POST.get('address')
        district = request.POST.get('district')
        gender = request.POST.get('gender')

        if CustomUser.objects.filter(mobile_number=mobile_number).exists():
            # If user already exists, you can handle this case accordingly
            return render(request, 'admin/create_investigator.html', {'error_message': 'User with this Mobile Number already exists.'})
        
        existing_users_count = CustomUser.objects.filter(last_name=last_name).count()
        counter = existing_users_count + 1

        user_id = generate_username(first_name)
        password = generate_password(first_name, counter)

        user = CustomUser.objects.create(
            user_id=user_id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email_id=email_id,
            mobile_number=mobile_number,
            generated_pass=password,
            user_district=district,
            is_investigator=True,
            is_active=True,
            is_superuser=False,
        )
        user.set_password(password)
        user.save()
        print('usersssssss',user)

        investigator = investigator_user.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email_id,
            mobile_number=mobile_number,
            address=address,
            district=district,
            gender=gender,
            is_investigator=True,
            is_active=True,
        )
        investigator.save()



        # Notify the user (e.g., by email) with their credentials here
        return redirect('/investigator_list/')
        # return HttpResponse(f"Investigator created successfully! Username: {user_id}, Password: {password}")

    user = request.user
    print('hhhhhhhhh',user,user.user_district)
    # district = user.objects.get(user_district)

    data = investigator_user.objects.all()

    context={
    'user':user,
    'data':data,
    }
    return render(request, 'admin/create_investigator.html',context)


from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse

def login_investigator(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            # Redirect to a success page or dashboard
            return HttpResponseRedirect(reverse('investigator_dashboard'))  # Replace 'dashboard' with your desired URL name
        else:
            # Handle authentication failure, e.g., show an error message
            error_message = "Invalid username or password. Please try again."
            # return HttpResponseRedirect(reverse('create_investigator'))  # Redirect to create investigator page if not a POST request
    
    return render(request, 'login/login_investigator.html', {'error_message': error_message})
    
# views.py
from django.contrib.auth.decorators import login_required

@login_required
def success_page(request):
    return render(request, 'login/success_page.html')



# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import investigator_user
from .serializers import InvestigatorSerializer
import string
import random

@api_view(['POST'])
def create_investigator_api(request):
    if request.method == 'POST':
        first_name = request.data.get('first_name')
        middle_name = request.data.get('middle_name', '')  # Optional, provide default value if not provided
        last_name = request.data.get('last_name')
        email_id = request.data.get('email_id')
        mobile_number = request.data.get('mobile_number')
        address = request.data.get('address')
        district = request.data.get('district')
        gender = request.data.get('gender')

        if CustomUser.objects.filter(mobile_number=mobile_number).exists():
            return Response({'error_message': 'User with this Mobile Number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_id = generate_username(first_name, last_name)
        password = generate_password()

        user = CustomUser.objects.create(
            user_id=user_id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email_id=email_id,
            mobile_number=mobile_number,
            user_district=district,
            generated_pass=password,
            is_investigator=True,
            is_active=True,
            is_superuser=False,
        )
        user.set_password(password)
        user.save()

        investigator = investigator_user.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email_id,
            mobile_number=mobile_number,
            address=address,
            district=district,
            gender=gender,
            is_investigator=True,
            is_active=True,
        )
        investigator.save()

        # Notify the user (e.g., by email) with their credentials here

        serializer = InvestigatorSerializer(user)  # Serialize user data
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({'error_message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import InvestigatorLoginSerializer

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
def login_investigator_api(request):
    if request.method == 'POST':
        serializer = InvestigatorLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            if user:
                is_investigator = CustomUser.objects.filter(user_id=username)
                if user is not None and is_investigator:
                    login(request, user)
                    csrf_token = get_token(request)
                    response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
                    response.set_cookie('csrftoken', csrf_token)
                    return response
                else:
                    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return JsonResponse({'status': 'error', 'message': "Invalid credentials !!!"}, status=400)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# admin login for respective district
def login_view(request):
    error_message=""
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        user = authenticate(user_id = user_id, password=password)

        if user is None:
            return render(request, 'login/district_login.html', {'error_message': 'Invalid login credentials.'})

            
        if user is not None:
            login(request, user)
            if request.user.is_authenticated and request.user.is_admin:
                return redirect('/dashboard_admin/')
            else:
                error_message = 'Invalid user ID or password'
                return render(request, 'login/district_login.html', {'error_message': error_message})
        else:
            error_message = 'Invalid user ID or password'
    return render(request, 'login/district_login.html', {'error_message': error_message})


# @login_required(login_url='/login/')
# def dashboard_admin(request):
#     user = request.user
#     print('ggggggggggg',user,user.user_district)

#     months = pest_incidence_data.objects.values_list('month', flat=True).distinct()
#     months = sorted(months, key=lambda x: MONTH_ORDER.index(x) if x in MONTH_ORDER else 0)

#     print('months', months)

#     selected_month = request.GET.get('month', None)
#     print('selected_month',selected_month)

#     if selected_month is None:
#         # Get the current month name
#         current_month_index = datetime.now().month - 1  # -1 because list index starts at 0
#         selected_month = MONTH_ORDER[current_month_index]

#     print('selected_month', selected_month)


#     # if selected_month:
#     #     # Filter records based on month and district
#     #     filtered_pests_w1 = pest_incidence_data.objects.filter(month=selected_month, district=user.user_district)
#     #     filtered_pests_w2 = pest_incidence_data.objects.filter(month=selected_month, district=user.user_district)
#     #     filtered_pests_w3 = pest_incidence_data.objects.filter(month=selected_month, district=user.user_district)
#     #     filtered_pests_w4 = pest_incidence_data.objects.filter(month=selected_month, district=user.user_district)

#     #     # Calculate averages for jassid_irm_average and jassid_nonirm_average
#     #     jassid_irm_avg = filtered_pests_w1.aggregate(avg_jassid_irm=Avg('jassid_irm_average'))['avg_jassid_irm']
#     #     jassid_nonirm_avg = filtered_pests_w1.aggregate(avg_jassid_nonirm=Avg('jassid_nonirm_average'))['avg_jassid_nonirm']

#     # print('selected_month',selected_month)
#     # # print('filtered_pests',filtered_pests)
#     # print('jassid_irm_avg',jassid_irm_avg)
#     # print('jassid_nonirm_avg',jassid_nonirm_avg)


#     chart_data1 = ["0.0", "0.0", "0.0"]
#     chart_data2 = ["0.0", "0.0", "0.0"]
#     chart_data3 = ["0.0", "0.0", "0.0"]
#     chart_data4 = ["0.0", "0.0", "0.0"]
#     chart_data5 = ["0.0", "0.0", "0.0"]
#     chart_data6 = ["0.0", "0.0", "0.0"]
#     chart_data7 = ["0.0", "0.0", "0.0"]
#     chart_data8 = ["0.0", "0.0", "0.0"]

#     if selected_month:
#         filtered_pests = pest_incidence_data.objects.filter(month=selected_month, district=user.user_district)

#         print('filtered_pests',filtered_pests)

#         # Calculate averages for each standard week of JASSID
#         week_data = filtered_pests.values('week','standard_week').annotate(
#             avg_jassid_irm=Avg('jassid_irm_average'),
#             avg_jassid_nonirm=Avg('jassid_nonirm_average')
#         ).order_by('week','standard_week')

#         # Prepare data for Google Charts
#         chart_data1 = [
#             ["Week", "IRM", "NON-IRM"]
#         ]
#         for week in week_data:
#             print('Jassid Data:', week)
#             chart_data1.append([
#                 f"{week['standard_week']}",
#                 week['avg_jassid_irm'] if week['avg_jassid_irm'] else 0,
#                 week['avg_jassid_nonirm'] if week['avg_jassid_nonirm'] else 0
#             ])



#         # # Calculate averages for each week OF JASSID
#         # week_data = filtered_pests.values('week').annotate(
#         #     avg_jassid_irm=Avg('jassid_irm_average'),
#         #     avg_jassid_nonirm=Avg('jassid_nonirm_average')
#         # ).order_by('week')

#         # # Prepare data for Google Charts
#         # chart_data1 = [
#         #     ["Week", "IRM", "NON-IRM"]
            
#         # ]
#         # for week in week_data:
#         #     print('fffff jassid',week)
#         #     chart_data1.append([
#         #         f" {week['week']}",
#         #         week['avg_jassid_irm'] if week['avg_jassid_irm'] else 0,
#         #         week['avg_jassid_nonirm'] if week['avg_jassid_nonirm'] else 0
#         #     ])


#         # Calculate averages for each week OF WHITEFLY
#         week_data1 = filtered_pests.values('week','standard_week').annotate(
#             avg_whitefly_irm=Avg('whitefly_irm_average'),
#             avg_whitefly_nonirm=Avg('whitefly_nonirm_average')
#         ).order_by('week','standard_week')

#         # Prepare data for Google Charts
#         chart_data2 = [
#             ["Week", "IRM", "NON-IRM"]
#         ]
#         for week in week_data1:
#             chart_data2.append([
#                 f" {week['standard_week']}",
#                 week['avg_whitefly_irm'] if week['avg_whitefly_irm'] else 0,
#                 week['avg_whitefly_nonirm'] if week['avg_whitefly_nonirm'] else 0
#             ])



#         # Calculate averages for each week OF THRIPS
#         week_data2 = filtered_pests.values('week','standard_week').annotate(
#             avg_thrips_irm=Avg('thrips_irm_average'),
#             avg_thrips_nonirm=Avg('thrips_nonirm_average')
#         ).order_by('week','standard_week')

#         # Prepare data for Google Charts
#         chart_data3 = [
#             ["Week", "IRM", "NON-IRM"]
#         ]
#         for week in week_data2:
#             chart_data3.append([
#                 f" {week['standard_week']}",
#                 week['avg_thrips_irm'] if week['avg_thrips_irm'] else 0,
#                 week['avg_thrips_nonirm'] if week['avg_thrips_nonirm'] else 0
#             ])



#         # Calculate averages for each week OF PINK BOLLWORM
#         week_data3 = filtered_pests.values('week','standard_week').annotate(
#             avg_flowers_irm=Avg('flowers_irm_average'),
#             avg_flowers_nonirm=Avg('flowers_nonirm_average')
#         ).order_by('week','standard_week')

#         # Prepare data for Google Charts
#         chart_data4 = [
#             ["Week", "IRM", "NON-IRM"]
#         ]
#         for week in week_data3:
#             chart_data4.append([
#                 f" {week['standard_week']}",
#                 week['avg_flowers_irm'] if week['avg_flowers_irm'] else 0,
#                 week['avg_flowers_nonirm'] if week['avg_flowers_nonirm'] else 0
#             ])


#         # Calculate averages for each week OF PINK BOLLWORM Infestation (Green Boll)
#         week_data4 = filtered_pests.values('week','standard_week').annotate(
#             avg_green_irm=Avg('green_irm_average'),
#             avg_green_nonirm=Avg('green_nonirm_average')
#         ).order_by('week','standard_week')

#         # Prepare data for Google Charts
#         chart_data5 = [
#             ["Week", "IRM", "NON-IRM"]
#         ]
#         for week in week_data4:
#             chart_data5.append([
#                 f" {week['standard_week']}",
#                 week['avg_green_irm'] if week['avg_green_irm'] else 0,
#                 week['avg_green_nonirm'] if week['avg_green_nonirm'] else 0
#             ])


#         # Calculate averages for each week OF PINK BOLLWORM Infestation (Locule Damage)
#         week_data5 = filtered_pests.values('week','standard_week').annotate(
#             avg_locule_irm=Avg('locule_irm_average'),
#             avg_locule_nonirm=Avg('locule_nonirm_average')
#         ).order_by('week','standard_week')

#         # Prepare data for Google Charts
#         chart_data6 = [
#             ["Week", "IRM", "NON-IRM"]
#         ]
#         for week in week_data5:
#             chart_data6.append([
#                 f" {week['standard_week']}",
#                 week['avg_locule_irm'] if week['avg_locule_irm'] else 0,
#                 week['avg_locule_nonirm'] if week['avg_locule_nonirm'] else 0
#             ])


#         # Calculate averages for each week OF PINK BOLLWORM Infestation (Open Boll)
#         week_data6 = filtered_pests.values('week','standard_week').annotate(
#             avg_open_ball_irm=Avg('open_ball_irm_average'),
#             avg_open_ball_nonirm=Avg('open_ball_nonirm_average')
#         ).order_by('week','standard_week')

#         # Prepare data for Google Charts
#         chart_data7 = [
#             ["Week", "IRM", "NON-IRM"]
#         ]
#         for week in week_data6:
#             chart_data7.append([
#                 f" {week['standard_week']}",
#                 week['avg_open_ball_irm'] if week['avg_open_ball_irm'] else 0,
#                 week['avg_open_ball_nonirm'] if week['avg_open_ball_nonirm'] else 0
#             ])


#         # Calculate averages for each week OF Pheromone trap Catches
#         week_data7 = filtered_pests.values('week','standard_week').annotate(
#             avg_pheromone_irm=Avg('pheromone_irm_average'),
#             avg_pheromone_nonirm=Avg('pheromone_nonirm_average')
#         ).order_by('week','standard_week')

#         # Prepare data for Google Charts
#         chart_data8 = [
#             ["Week", "IRM", "NON-IRM"]
#         ]
#         for week in week_data7:
#             chart_data8.append([
#                 f" {week['standard_week']}",
#                 week['avg_pheromone_irm'] if week['avg_pheromone_irm'] else 0,
#                 week['avg_pheromone_nonirm'] if week['avg_pheromone_nonirm'] else 0
#             ])


#     print('JASSID',chart_data1)
#     # print('WHITEFLY',chart_data2)
#     # print('THRIPS',chart_data3)
#     # print('PINK BOLLWORM',chart_data4)
#     # print('(Green Boll)',chart_data5)
#     # print(' (Locule Damage)',chart_data6)
#     # print('(Open Boll)',chart_data7)
#     print('Pheromone trap Catches',chart_data8)

#     basic_servey = basic_servey_info.objects.filter(district=user.user_district)
#     # print('basic_servey',basic_servey)

#     surveys_per_month = (basic_servey_info.objects
#                          .filter(district=user.user_district)
#                          .annotate(month=ExtractMonth('servey_date'))
#                          .values('month')
#                          .annotate(count=Count('id'))
#                          .order_by('month'))

#     # Convert the queryset to a list of dictionaries
#     survey_data = list(surveys_per_month)

#     # Map month numbers to month names
#     month_names = [
#         "January", "February", "March", "April", "May", "June",
#         "July", "August", "September", "October", "November", "December"
#     ]

#     for item in survey_data:
#         month_index = item['month'] - 1  # Convert month number to zero-based index
#         item['month_name'] = month_names[month_index] if 0 <= month_index < 12 else 'Unknown'


#     print('servey_date',survey_data)

#     # Aggregate pest incidences by month
#     pests_per_month = (pest_incidence_data.objects
#                        .filter(district=user.user_district)
#                        .values('month')
#                        .annotate(count=Count('id'))
#                        .order_by('month'))

#     pest_data = list(pests_per_month)

#     pest_data_sorted = sorted(pest_data, key=lambda x: MONTH_ORDER.index(x['month']) if x['month'] in MONTH_ORDER else -1)

#     print('pest_data', pest_data_sorted)

#     context = {
#         'months': months,
#         'survey_data': survey_data,
#         'pest_data':pest_data_sorted,
#         'chart_data':chart_data1,
#         'chart_data2':chart_data2,
#         'chart_data3':chart_data3,
#         'chart_data4':chart_data4,
#         'chart_data5':chart_data5,
#         'chart_data6':chart_data6,
#         'chart_data7':chart_data7,
#         'chart_data8':chart_data8,
#         'selected_month':selected_month,
#     }
#     return render(request, 'login/admin_dashboard.html',context)



from datetime import datetime, date
from django.db.models import Avg, Count
from django.db.models.functions import ExtractMonth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='/login/')
def dashboard_admin(request):
    user = request.user

    # --- Step 1: Get financial year ---
    financial_years = Financial_Year.objects.order_by('-id').first()
    selected_fin_year = request.session.get('financial_year', financial_years.financial_year)
    start_year, end_year = map(int, selected_fin_year.split('-'))
    start_date = date(start_year, 4, 1)
    end_date = date(end_year, 3, 31)

    print('Selected Financial Year:', selected_fin_year)
    print('Date Range:', start_date, end_date)

    # --- Step 2: Get unique months (within financial year) ---
    months = (pest_incidence_data.objects
              .filter(date_field__range=(start_date, end_date), district=user.user_district)
              .values_list('month', flat=True)
              .distinct())
    months = sorted(months, key=lambda x: MONTH_ORDER.index(x) if x in MONTH_ORDER else 0)

    selected_month = request.GET.get('month')
    if selected_month is None:
        selected_month = MONTH_ORDER[datetime.now().month - 1]

    # --- Step 3: Filter pest data for selected month & date range ---
    chart_data1 = chart_data2 = chart_data3 = chart_data4 = chart_data5 = chart_data6 = chart_data7 = chart_data8 = [["Week", "IRM", "NON-IRM"]]

    if selected_month:
        filtered_pests = pest_incidence_data.objects.filter(
            month=selected_month,
            district=user.user_district,
            date_field__range=(start_date, end_date)
        )

        # Chart logic repeated for 8 pests
        def get_weekly_avg_chart(field1, field2):
            week_data = filtered_pests.values('week', 'standard_week').annotate(
                avg1=Avg(field1),
                avg2=Avg(field2)
            ).order_by('week', 'standard_week')

            chart = [["Week", "IRM", "NON-IRM"]]
            for week in week_data:
                chart.append([
                    f"{week['standard_week']}",
                    week['avg1'] if week['avg1'] else 0,
                    week['avg2'] if week['avg2'] else 0
                ])
            return chart

        chart_data1 = get_weekly_avg_chart('jassid_irm_average', 'jassid_nonirm_average')
        chart_data2 = get_weekly_avg_chart('whitefly_irm_average', 'whitefly_nonirm_average')
        chart_data3 = get_weekly_avg_chart('thrips_irm_average', 'thrips_nonirm_average')
        chart_data4 = get_weekly_avg_chart('flowers_irm_average', 'flowers_nonirm_average')
        chart_data5 = get_weekly_avg_chart('green_irm_average', 'green_nonirm_average')
        chart_data6 = get_weekly_avg_chart('locule_irm_average', 'locule_nonirm_average')
        chart_data7 = get_weekly_avg_chart('open_ball_irm_average', 'open_ball_nonirm_average')
        chart_data8 = get_weekly_avg_chart('pheromone_irm_average', 'pheromone_nonirm_average')

    # --- Step 4: Survey chart (financial year wise) ---
    basic_servey = basic_servey_info.objects.filter(district=user.user_district, servey_date__range=(start_date, end_date))

    surveys_per_month = (basic_servey_info.objects
                         .filter(district=user.user_district, servey_date__range=(start_date, end_date))
                         .annotate(month=ExtractMonth('servey_date'))
                         .values('month')
                         .annotate(count=Count('id'))
                         .order_by('month'))

    survey_data = list(surveys_per_month)
    month_names = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    for item in survey_data:
        item['month_name'] = month_names[item['month'] - 1] if 1 <= item['month'] <= 12 else 'Unknown'

    # --- Step 5: Pest data chart (financial year wise) ---
    pests_per_month = (pest_incidence_data.objects
                       .filter(district=user.user_district, date_field__range=(start_date, end_date))
                       .values('month')
                       .annotate(count=Count('id'))
                       .order_by('month'))

    pest_data = list(pests_per_month)
    pest_data_sorted = sorted(pest_data, key=lambda x: MONTH_ORDER.index(x['month']) if x['month'] in MONTH_ORDER else -1)

    # --- Step 6: Render ---
    context = {
        'months': months,
        'selected_month': selected_month,
        'survey_data': survey_data,
        'pest_data': pest_data_sorted,
        'chart_data': chart_data1,
        'chart_data2': chart_data2,
        'chart_data3': chart_data3,
        'chart_data4': chart_data4,
        'chart_data5': chart_data5,
        'chart_data6': chart_data6,
        'chart_data7': chart_data7,
        'chart_data8': chart_data8,
        'selected_financial_year': selected_fin_year,
        'financial_years': Financial_Year.objects.all()
    }
    return render(request, 'login/admin_dashboard.html', context)



@login_required(login_url='/login/')
def admin_profile(request):
    print('admin',request.user)
    data = CustomUser.objects.get(user_id= request.user)
  
    print('data',data)
    if request.method == 'POST':
        data.first_name =request.POST.get('first_name')
        data.last_name =request.POST.get('last_name')
        data.email_id =request.POST.get('email_id')
        data.mobile_number = request.POST.get('mobile_number')
        data.address = request.POST.get('address')
       
        data.save()

        return redirect('/admin_profile/')

        
    user = CustomUser.objects.get(user_id= request.user)
    
    context = {
    'data':data,
    'user':user,
    'first_name': data.first_name,
    'last_name': data.last_name,
    }
        
    return render(request, 'admin/admin_profile.html',context)


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Advisory
from .serializers import AdvisorySerializer

# class AdvisoryCreateAPIView(APIView):
#     def get(self, request, format=None):
#         photographs = Advisory.objects.all()
#         serializer = AdvisorySerializer(photographs, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, *args, **kwargs):
#         # Pass the request data to the serializer, request.FILES will be handled automatically
#         serializer = AdvisorySerializer(data=request.data)
#         print('serializer',serializer)
        
#         # Validate the data
#         if serializer.is_valid():
#             serializer.save()  # Save the instance including files
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
#         # If invalid data, return the errors
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AdvisoryCreateAPIView(APIView):
#     def get(self, request, format=None):
#         # advisories = Advisory.objects.all().order_by('-id')
#         advisories = Advisory.objects.all().order_by('-id')
#         serializer = AdvisorySerializer(advisories, many=True)
#         advisory_data = serializer.data

#         # Create 'all_pdf' object from the latest advisory if exists
#         if advisory_data:
#             latest = advisory_data[0]  # most recent one

#             all_pdf = {
#                 "week_en": latest.get("week_en"),
#                 "path_pdf_en": latest.get("path_pdf_en"),
#                 "week_hi": latest.get("week_hi"),
#                 "path_pdf_hi": latest.get("path_pdf_hi"),
#                 "week_gu": latest.get("week_gu"),
#                 "path_pdf_gu": latest.get("path_pdf_gu"),
#                 "lang_1": latest.get("lang_1"),
#                 "lang_1_pdf": latest.get("lang_1_pdf"),
#                 "lang_2": latest.get("lang_2"),
#                 "lang_2_pdf": latest.get("lang_2_pdf"),
#                 "lang_3": latest.get("lang_3"),
#                 "lang_3_pdf": latest.get("lang_3_pdf"),
#                 "lang_4": latest.get("lang_4"),
#                 "lang_4_pdf": latest.get("lang_4_pdf"),
#                 "lang_5": latest.get("lang_5"),
#                 "lang_5_pdf": latest.get("lang_5_pdf"),
#                 "lang_6": latest.get("lang_6"),
#                 "lang_6_pdf": latest.get("lang_6_pdf"),
#                 "lang_7": latest.get("lang_7"),
#                 "lang_7_pdf": latest.get("lang_7_pdf"),
#             }

#             final_data = advisory_data + [{"all_pdf": all_pdf}]
#         else:
#             final_data = []

#         return Response(final_data, status=status.HTTP_200_OK)

#     def post(self, request, *args, **kwargs):
#         serializer = AdvisorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AdvisoryCreateAPIView(APIView):
    def get(self, request, format=None):
        limit_param = request.query_params.get('limit')
        advisories = Advisory.objects.order_by('-id')
        if limit_param:
            try:
                advisories = advisories[:int(limit_param)]
            except ValueError:
                pass
        serializer = AdvisorySerializer(advisories, many=True, context={'request': request})
        advisory_data = list(serializer.data)

        # Build all_pdf from the absolute latest advisory (id desc)
        # If you want it to be based only on the limited list, use advisory_data[0] instead.
        latest_obj = Advisory.objects.order_by('-id').first()
        if latest_obj:
            latest_ser = AdvisorySerializer(latest_obj, context={'request': request}).data
            all_pdf = {
                "week_en": latest_ser.get("week_en"),
                "path_pdf_en": latest_ser.get("path_pdf_en"),
                "week_hi": latest_ser.get("week_hi"),
                "path_pdf_hi": latest_ser.get("path_pdf_hi"),
                "week_gu": latest_ser.get("week_gu"),
                "path_pdf_gu": latest_ser.get("path_pdf_gu"),
                "lang_1": latest_ser.get("lang_1"),
                "lang_1_pdf": latest_ser.get("lang_1_pdf"),
                "lang_2": latest_ser.get("lang_2"),
                "lang_2_pdf": latest_ser.get("lang_2_pdf"),
                "lang_3": latest_ser.get("lang_3"),
                "lang_3_pdf": latest_ser.get("lang_3_pdf"),
                "lang_4": latest_ser.get("lang_4"),
                "lang_4_pdf": latest_ser.get("lang_4_pdf"),
                "lang_5": latest_ser.get("lang_5"),
                "lang_5_pdf": latest_ser.get("lang_5_pdf"),
                "lang_6": latest_ser.get("lang_6"),
                "lang_6_pdf": latest_ser.get("lang_6_pdf"),
                "lang_7": latest_ser.get("lang_7"),
                "lang_7_pdf": latest_ser.get("lang_7_pdf"),
            }
            # final_data = advisory_data + [{"all_pdf": all_pdf}]
            final_data = advisory_data
        else:
            final_data = advisory_data  # will be []

        return Response(final_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = AdvisorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdvisoryDetailAPIView(APIView):
    def get(self, request, pk, format=None):
        advisory = get_object_or_404(Advisory, pk=pk)
        serializer = AdvisorySerializer(advisory, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)




from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Advisory


# List all advisories
from django.contrib.auth.decorators import login_required
from django.db.models import F, Value, DateField
from django.db.models.functions import Substr, Concat, Cast

@login_required(login_url='/')
def advisory_list(request):
    # 1) Financial year read
    financial_years = Financial_Year.objects.order_by('-id').first()
    selected_fin_year = request.session.get(
        'financial_year',
        financial_years.financial_year if financial_years else '2024-2025'
    )
    print('====financial_years====', financial_years, selected_fin_year)
    
    # 2) FY -> start/end dates
    start_year, end_year = map(int, selected_fin_year.split('-'))
    start_date = date(start_year, 4, 1)   # 01-Apr
    end_date   = date(end_year, 3, 31)    # 31-Mar
    print('FY:', selected_fin_year, 'Range:', start_date, '->', end_date)

    # 3) start_date_en ("DD-MM-YYYY") ko "YYYY-MM-DD" me convert karna (DB side)
    # YYYY  = Substr(start_date_en, 7, 4)
    # MM    = Substr(start_date_en, 4, 2)
    # DD    = Substr(start_date_en, 1, 2)
    advisories = (
        Advisory.objects
        # Optional: blank/None hata do
        .exclude(start_date_en__isnull=True)
        .exclude(start_date_en__exact='')
        # "YYYY-MM-DD" string banayen
        .annotate(
            start_date_iso=Concat(
                Substr('start_date_en', 7, 4), Value('-'),
                Substr('start_date_en', 4, 2), Value('-'),
                Substr('start_date_en', 1, 2),
            )
        )
        # String -> Date cast (SQLite tab kaam karta hai jab format YYYY-MM-DD ho)
        .annotate(start_date_db=Cast(F('start_date_iso'), output_field=DateField()))
        # Range filter
        .filter(start_date_db__range=(start_date, end_date))
        # Sorting by parsed date desc, then id desc
        .order_by('-start_date_db', '-id')
    )

    print('advisories',advisories)
    
    return render(
        request,
        'advisory_list.html',
        {'advisories': advisories, 'selected_fin_year': selected_fin_year}
    )


# @login_required(login_url='/')
# def advisory_list(request):
#     advisories = Advisory.objects.all()
#     return render(request, 'advisory_list.html', {'advisories': advisories})


# Create a new advisory
# @login_required(login_url='/')
# def advisory_create(request):
#     if request.method == 'POST':
#         week_en = request.POST.get('week_en')
#         week_hi = request.POST.get('week_hi')
#         week_gu = request.POST.get('week_gu')
#         date_range_en = request.POST.get('date_range_en')
#         date_range_hi = request.POST.get('date_range_hi')
#         date_range_gu = request.POST.get('date_range_gu')
#         month_en = request.POST.get('month_en')
#         month_hi = request.POST.get('month_hi')
#         month_gu = request.POST.get('month_gu')
#         start_date_en = request.POST.get('start_date_en')
#         start_date_hi = request.POST.get('start_date_hi')
#         start_date_gu = request.POST.get('start_date_gu')
#         path_pdf_en = request.FILES.get('path_pdf_en')
#         path_pdf_hi = request.FILES.get('path_pdf_hi')
#         path_pdf_gu = request.FILES.get('path_pdf_gu')

#         advisory = Advisory(
#             week_en=week_en, week_hi=week_hi, week_gu=week_gu,
#             date_range_en=date_range_en, date_range_hi=date_range_hi, date_range_gu=date_range_gu,
#             month_en=month_en, month_hi=month_hi, month_gu=month_gu,
#             start_date_en=start_date_en, start_date_hi=start_date_hi, start_date_gu=start_date_gu,
#             path_pdf_en=path_pdf_en, path_pdf_hi=path_pdf_hi, path_pdf_gu=path_pdf_gu
#         )
#         advisory.save()
#         return redirect('advisory_list')
#     return render(request, 'advisory_create.html')


@login_required(login_url='/')
def advisory_create(request):
    if request.method == 'POST':
        advisory = Advisory(
            week_en=request.POST.get('week_en'),
            week_hi=request.POST.get('week_hi'),
            week_gu=request.POST.get('week_gu'),
            date_range_en=request.POST.get('date_range_en'),
            date_range_hi=request.POST.get('date_range_hi'),
            date_range_gu=request.POST.get('date_range_gu'),
            month_en=request.POST.get('month_en'),
            month_hi=request.POST.get('month_hi'),
            month_gu=request.POST.get('month_gu'),
            start_date_en=request.POST.get('start_date_en'),
            start_date_hi=request.POST.get('start_date_hi'),
            start_date_gu=request.POST.get('start_date_gu'),
            path_pdf_en=request.FILES.get('path_pdf_en'),
            path_pdf_hi=request.FILES.get('path_pdf_hi'),
            path_pdf_gu=request.FILES.get('path_pdf_gu'),

            lang_1=request.POST.get('lang_1'),
            lang_1_pdf=request.FILES.get('lang_1_pdf'),
            lang_2=request.POST.get('lang_2'),
            lang_2_pdf=request.FILES.get('lang_2_pdf'),
            lang_3=request.POST.get('lang_3'),
            lang_3_pdf=request.FILES.get('lang_3_pdf'),
            lang_4=request.POST.get('lang_4'),
            lang_4_pdf=request.FILES.get('lang_4_pdf'),
            lang_5=request.POST.get('lang_5'),
            lang_5_pdf=request.FILES.get('lang_5_pdf'),
            lang_6=request.POST.get('lang_6'),
            lang_6_pdf=request.FILES.get('lang_6_pdf'),
            lang_7=request.POST.get('lang_7'),
            lang_7_pdf=request.FILES.get('lang_7_pdf'),
        )
        advisory.save()
        return redirect('advisory_list')

    return render(request, 'advisory_create.html')


# Update an existing advisory
@login_required(login_url='/')
def advisory_update(request, id):
    advisory = get_object_or_404(Advisory, id=id)
    if request.method == 'POST':
        advisory.week_en = request.POST.get('week_en')
        advisory.week_hi = request.POST.get('week_hi')
        advisory.week_gu = request.POST.get('week_gu')
        advisory.date_range_en = request.POST.get('date_range_en')
        advisory.date_range_hi = request.POST.get('date_range_hi')
        advisory.date_range_gu = request.POST.get('date_range_gu')
        advisory.month_en = request.POST.get('month_en')
        advisory.month_hi = request.POST.get('month_hi')
        advisory.month_gu = request.POST.get('month_gu')
        advisory.start_date_en = request.POST.get('start_date_en')
        advisory.start_date_hi = request.POST.get('start_date_hi')
        advisory.start_date_gu = request.POST.get('start_date_gu')
        
        advisory.lang_1 = request.POST.get('lang_1')
        advisory.lang_2 = request.POST.get('lang_2')
        advisory.lang_3 = request.POST.get('lang_3')
        advisory.lang_4 = request.POST.get('lang_4')
        advisory.lang_5 = request.POST.get('lang_5')
        advisory.lang_6 = request.POST.get('lang_6')
        advisory.lang_7 = request.POST.get('lang_7')
        
        if request.FILES.get('path_pdf_en'):
            advisory.path_pdf_en = request.FILES.get('path_pdf_en')
        if request.FILES.get('path_pdf_hi'):
            advisory.path_pdf_hi = request.FILES.get('path_pdf_hi')
        if request.FILES.get('path_pdf_gu'):
            advisory.path_pdf_gu = request.FILES.get('path_pdf_gu')
            
        if request.FILES.get('lang_1_pdf'):
            advisory.lang_1_pdf = request.FILES.get('lang_1_pdf')
        if request.FILES.get('lang_2_pdf'):
            advisory.lang_2_pdf = request.FILES.get('lang_2_pdf')
        if request.FILES.get('lang_3_pdf'):
            advisory.lang_3_pdf = request.FILES.get('lang_3_pdf')
        if request.FILES.get('lang_4_pdf'):
            advisory.lang_4_pdf = request.FILES.get('lang_4_pdf')
        if request.FILES.get('lang_5_pdf'):
            advisory.lang_5_pdf = request.FILES.get('lang_5_pdf')
        if request.FILES.get('lang_6_pdf'):
            advisory.lang_6_pdf = request.FILES.get('lang_6_pdf')
        if request.FILES.get('lang_7_pdf'):
            advisory.lang_7_pdf = request.FILES.get('lang_7_pdf')

        advisory.save()
        return redirect('advisory_list')
    return render(request, 'advisory_update.html', {'advisory': advisory})




# Delete an advisory
@login_required(login_url='/')
def advisory_delete(request, id):
    advisory = get_object_or_404(Advisory, id=id)
    if request.method == 'POST':
        advisory.delete()
        return redirect('advisory_list')
    return render(request, 'advisory_delete.html', {'advisory': advisory})



from django.shortcuts import render, redirect, get_object_or_404
from .models import Banner
from django.conf import settings
import os

def banner_list(request):
    banners = Banner.objects.all().order_by('-id')

    if request.method == 'POST':
        banner_id = request.POST.get('banner_id')
        name = request.POST.get('name', '').strip()
        image = request.FILES.get('image')

        if banner_id:  # EDIT
            banner = get_object_or_404(Banner, id=banner_id)
            banner.name = name
            if image:
                if banner.image and os.path.isfile(banner.image.path):
                    os.remove(banner.image.path)
                banner.image = image
            banner.save()
        else:  # ADD
            if image:
                Banner.objects.create(name=name, image=image)

        return redirect('banner_list')

    is_farmer_panel = request.path.startswith('/farmer/')
    return render(request, 'banners/list.html', {
        'banners': banners,
        'active_tab': 'banners' if is_farmer_panel else None,
        'base_template': 'farmer_app/farmer_panel_base.html' if is_farmer_panel else 'base.html',
        'page_heading': 'Manage Banners',
    })



def banner_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        image = request.FILES.get('image')
        if image:
            Banner.objects.create(name=name, image=image)
            return redirect('banner_list')
    return render(request, 'banners/add.html')


def banner_edit(request, banner_id):
    banner = get_object_or_404(Banner, id=banner_id)
    if request.method == 'POST':
        banner.name = request.POST.get('name', '').strip()
        if 'image' in request.FILES:
            # Delete old image
            if banner.image:
                if os.path.isfile(banner.image.path):
                    os.remove(banner.image.path)
            banner.image = request.FILES['image']
            banner.save()
        return redirect('banner_list')
    return render(request, 'banners/edit.html', {'banner': banner})


def banner_delete(request, banner_id):
    banner = get_object_or_404(Banner, id=banner_id)
    if banner.image:
        if os.path.isfile(banner.image.path):
            os.remove(banner.image.path)
    banner.delete()
    return redirect('banner_list')



def banner_list_api(request):
    banners = Banner.objects.all().order_by('-id')[:7]
    data = []
    for banner in banners:
        image_url = request.build_absolute_uri(banner.image.url) if banner.image else None
        data.append({
            "id": banner.id,
            "name": banner.name,
            "image_url": image_url,
        })
    return JsonResponse({"banners": data}, safe=False)



# financial year master

def financial_year_list(request):
    years = Financial_Year.objects.all()

    if request.method == 'POST':
        financial_year_id = request.POST.get('financial_year_id')
        financial_year = request.POST.get('financial_year')

        if financial_year_id:  # EDIT
            year = get_object_or_404(Financial_Year, id=financial_year_id)
            year.financial_year = financial_year
            year.save()
        else:  # ADD
            if financial_year:
                Financial_Year.objects.create(financial_year=financial_year)

        return redirect('financial_year_list')

    return render(request, 'financial_list.html', {'years': years})


def year_delete(request, year_id):
    year = get_object_or_404(Financial_Year, id=year_id)
    year.delete()
    return redirect('financial_year_list')





