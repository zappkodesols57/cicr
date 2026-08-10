# # serializers.py
# from rest_framework import serializers
# from .models import pest_incidence_data

# class PestIncidenceDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = pest_incidence_data
#         fields = '__all__'


from rest_framework import serializers
from .models import pest_incidence_data
from .models import *

class PestIncidenceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = pest_incidence_data
        fields = '__all__'
    
    # def validate(self, data):
    #     week = data.get('week')
    #     month = data.get('month')
    #     year = data.get('year')
        
    #     if pest_incidence_data.objects.filter(week=week, month=month, year=year).exists():
    #         raise serializers.ValidationError("Entry for the same week, month, and year already exists.")
        
    #     return data


class MonthlyPhysicalProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = monthly_physical_progress
        fields = '__all__'


class ExtensionActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = extension_activities_carried_out
        fields = '__all__'