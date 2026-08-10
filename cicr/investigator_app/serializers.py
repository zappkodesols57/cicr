from rest_framework import serializers
from .models import basic_servey_info
from datetime import date
from owner_settings.models import pest_incidence_data
from .models import *

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_servey_info
        fields = '__all__'  # or specify fields explicitly if needed

    def create(self, validated_data):
        if 'servey_date' not in validated_data or not validated_data['servey_date']:
            validated_data['servey_date'] = date.today()
        if 'year' not in validated_data or not validated_data['year']:
            validated_data['year'] = str(date.today().year)
        return super().create(validated_data)


# serializers.py
from rest_framework import serializers
from .models import district

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = district
        fields = '__all__'


from rest_framework import serializers

class BasicServeyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_servey_info
        fields = '__all__'  # Or list all fields explicitly


class WeeklyReportInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = pest_incidence_data
        fields = '__all__'  # Or list all fields explicitly


class RepresentedPhotographSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepresentedPhotograph
        fields = '__all__'

class AssessmentSeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentSeason
        fields = '__all__'

class YearlyProgressReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearlyProgressReport
        fields = '__all__'



class StandardWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = standard_weeks
        fields = '__all__'


class NewsArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = ['id', 'issue_no', 'date', 'month', 'pdf']

