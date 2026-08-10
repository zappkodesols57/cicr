from django.shortcuts import render,redirect
import sweetify
from .models import *
from login.models import User
from investigator_app.models import *
from login.models import *
from owner_settings.models import pest_incidence_data
from .serializers import *

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import district
from .models import *
from django.utils.timezone import now
from django.urls import reverse

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
from login.models import *
from login.models import User as CustomUser

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.generics import ListAPIView, RetrieveAPIView

# Create your views here.

@login_required(login_url='/')
def district_info(request):
    if request.method == 'POST':
        district_name =request.POST.get('district_name')
        if district.objects.filter(district_name=district_name).exists():
            error_message = f"A district with the name '{district_name}' already exists."
            return render(request,'admin/district.html',{'error_messages': error_message})
        else:
            data = district(district_name=district_name)
            data.save()
            sweetify.success(request, "District created successfully.", timer=3000)
            return redirect('/display_district/')

    data1 = district.objects.all()
    context={
        "data1":data1,
    }
    return render(request,"admin/district.html", context)


@login_required(login_url='/')
def display_district(request):
    data = district.objects.all().order_by('district_name')

    context={
    "data":data
    }
    return render(request,"admin/display_district.html",context)


@login_required(login_url='/')
def edit_district(request, id):
    data =district.objects.get(id=id)
    if request.method == 'POST':
        data.district_name = request.POST.get('district_name')
        data.save()
        return redirect('/display_district/')
        
    context={"data":data,}
    return render(request,"admin/edit_district.html", context)


@login_required(login_url='/')
def delete_district(request, id):
    cus = district.objects.get(id=id)
    cus.delete()
    return redirect('/display_district/')


def display_all_district(request):
    data = district.objects.all()
    context={
    'data':data,
    }
    return render(request,"admin/display_all_district.html", context)


@login_required(login_url='/')
def sandard_week(request):
    if request.method == 'POST':
        standard_number = request.POST.get("standard_number", "")
        standard_week = request.POST.get("standard_week", "")
        weeks_value = request.POST.get("weeks_value", "")
        month_data = request.POST.get("month_data", "")
        print('gsd',month_data)
        date_field = now().date()
        year = date_field.year

        if standard_weeks.objects.filter(standard_number=standard_number,year=year).exists():
            number_message = f"A Standard Number with the number '{standard_number}' of same {year} is already exists."
            return render(request,'admin/standardweeks.html',{'number_message': number_message})

        if standard_weeks.objects.filter(standard_week=standard_week,year=year).exists():
            error_message = f"A Standard Weeks with the name '{standard_week}' of same {year} is already exists."
            return render(request,'admin/standardweeks.html',{'error_messages': error_message})

        else:
            standard_week_entry = standard_weeks(
                standard_number=standard_number,
                standard_week=standard_week,
                date_field=date_field,
                year=year,
                weeks_value=weeks_value,
                month_data=month_data,
            )
            standard_week_entry.save()

    data1 = standard_weeks.objects.all()
    context={
        "data1":data1,
    }
    return render(request,"admin/standardweeks.html", context)


def investigator_list(request):
    user = request.user
    print('user',user,user.user_district)
    
    data = investigator_user.objects.filter(district=user.user_district)
    print('datsssssss',data)
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
                'address': i.address  # Assuming this field is in investigator_user
            })
        except User.DoesNotExist:
            pass

    context = {
        'data': user_data,
    }
    return render(request,'investigator/investigator_list.html',context)
    

from .serializers import DistrictSerializer
from django.db.models.functions import Cast
from django.db.models import IntegerField

class DistrictList(APIView):
    def get(self, request, format=None):
        districts = district.objects.all().order_by('district_name')
        serializer = DistrictSerializer(districts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class StandardWeekList(APIView):
    def get(self, request, format=None):
        weeks = standard_weeks.objects.all().annotate(
            standard_number_int=Cast('standard_number', IntegerField())
        ).order_by('standard_number_int')
        
        serializer = StandardWeekSerializer(weeks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



from .models import basic_servey_info
from .serializers import FarmerSerializer

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

class FarmerListCreateAPIView(APIView):
    def get(self, request):
        farmers = basic_servey_info.objects.all()
        serializer = FarmerSerializer(farmers, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = FarmerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FarmerDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return basic_servey_info.objects.get(pk=pk)
        except Farmer.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        farmer = self.get_object(pk)
        serializer = FarmerSerializer(farmer)
        return Response(serializer.data)
    
    def put(self, request, pk):
        farmer = self.get_object(pk)
        serializer = FarmerSerializer(farmer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        farmer = self.get_object(pk)
        farmer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




from .serializers import BasicServeyInfoSerializer
from rest_framework.permissions import IsAuthenticated

class InvestigatorEntriesAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        investigator = request.user
        entries = basic_servey_info.objects.filter(user_id=investigator)
        serializer = BasicServeyInfoSerializer(entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# class InvestigatorEntryEditAPIView(APIView):

#     @method_decorator(csrf_exempt)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
#         # return super(InvestigatorEntryEditAPIView, self).dispatch(*args, **kwargs)

#     def put(self, request, pk):
#         try:
#             entry = basic_servey_info.objects.get(pk=pk)
#             print('entry', entry)
#         except basic_servey_info.DoesNotExist:
#             return Response({'error': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = BasicServeyInfoSerializer(entry, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

@method_decorator(csrf_exempt, name='dispatch')
class InvestigatorEntryEditAPIView(APIView):
    def put(self, request, pk):
        try:
            entry = basic_servey_info.objects.get(pk=pk)
            print('entry', entry)
        except basic_servey_info.DoesNotExist:
            return Response({'error': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BasicServeyInfoSerializer(entry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class InvestigatorEntryEditAPIView(APIView):
#     # permission_classes = [IsAuthenticated]

#     def put(self, request, pk):
#         try:
#             entry = basic_servey_info.objects.get(pk=pk)
#             print('entry',entry)
#         except basic_servey_info.DoesNotExist:
#             return Response({'error': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = BasicServeyInfoSerializer(entry, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .serializers import WeeklyReportInfoSerializer
class ReportsEntriesAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        investigator = request.user
        entries = pest_incidence_data.objects.filter(user_id=investigator)
        serializer = WeeklyReportInfoSerializer(entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManageReportsEditAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            entry = pest_incidence_data.objects.get(pk=pk)
        except pest_incidence_data.DoesNotExist:
            return Response({'error': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WeeklyReportInfoSerializer(entry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RepresentedPhotographListCreateAPIView(APIView):
    def get(self, request, format=None):
        photographs = RepresentedPhotograph.objects.all()
        serializer = RepresentedPhotographSerializer(photographs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = RepresentedPhotographSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssessmentSeasonListCreateAPIView(APIView):
    def get(self, request, format=None):
        assessment = AssessmentSeason.objects.all()
        serializer = AssessmentSeasonSerializer(assessment, many= True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = AssessmentSeasonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class YearlyProgressReportCreateAPIView(APIView):
    def get(self, request, format=None):
        yearlyprogress = YearlyProgressReport.objects.all()
        serializer = YearlyProgressReportSerializer(yearlyprogress, many= True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = YearlyProgressReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import basic_servey_info
from .serializers import BasicServeyInfoSerializer

# views.py

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class BasicServeyInfoView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(BasicServeyInfoView, self).dispatch(*args, **kwargs)

    def get(self, request):
        user_id = request.user.user_id
        print('user_id',user_id)
        try:
            servey_info = basic_servey_info.objects.filter(user_id=user_id)
            serializer = BasicServeyInfoSerializer(servey_info, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except basic_servey_info.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import basic_servey_info

@csrf_exempt
@login_required
def basic_servey_data_view(request):
    if request.method == 'GET':
        user_id = request.user.user_id
        print('user_id',user_id)
        servey_info = basic_servey_info.objects.filter(user_id=user_id)
        print('servey_info',servey_info)
        
        # Create a list of dictionaries from the queryset
        data = list(servey_info.values())

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'GET method required'}, status=400)




class NewsArticleCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = NewsArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List all articles
class NewsArticleListAPIView(ListAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer

# Retrieve a single article by ID
class NewsArticleDetailAPIView(RetrieveAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    lookup_field = 'id'  # Default is 'pk', use 'id' if preferred

    
