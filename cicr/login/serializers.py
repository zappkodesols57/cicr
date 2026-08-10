from rest_framework import serializers
from .models import User, investigator_user

class InvestigatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Assuming CustomUser is your User model
        fields = ['user_id', 'first_name', 'last_name', 'email_id', 'mobile_number', 'address', 'user_district']
        
        
# serializers.py
from rest_framework import serializers

class InvestigatorLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()




from rest_framework import serializers
from login.models import Advisory

# class AdvisorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Advisory
#         fields = [
#             'week_en', 'week_hi', 'week_gu',
#             'date_range_en', 'date_range_hi', 'date_range_gu',
#             'month_en', 'month_hi', 'month_gu',
#             'start_date_en', 'start_date_hi', 'start_date_gu',
#             'path_pdf_en', 'path_pdf_hi', 'path_pdf_gu'
#         ]

class AdvisorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisory
        fields = [
            'week_en', 'week_hi', 'week_gu',
            'date_range_en', 'date_range_hi', 'date_range_gu',
            'month_en', 'month_hi', 'month_gu',
            'start_date_en', 'start_date_hi', 'start_date_gu',
            'path_pdf_en', 'path_pdf_hi', 'path_pdf_gu',

            'lang_1', 'lang_1_pdf',
            'lang_2', 'lang_2_pdf',
            'lang_3', 'lang_3_pdf',
            'lang_4', 'lang_4_pdf',
            'lang_5', 'lang_5_pdf',
            'lang_6', 'lang_6_pdf',
            'lang_7', 'lang_7_pdf',
        ]



# class AdvisorySerializer(serializers.ModelSerializer):
#     pdf_path_en = serializers.SerializerMethodField()
#     pdf_path_hi = serializers.SerializerMethodField()
#     pdf_path_gu = serializers.SerializerMethodField()

#     class Meta:
#         model = Advisory
#         fields = '__all__'

#     def get_pdf_path_en(self, obj):
#         request = self.context.get('request')
#         return request.build_absolute_uri(obj.pdf_path_en.url)

#     def get_pdf_path_hi(self, obj):
#         request = self.context.get('request')
#         return request.build_absolute_uri(obj.pdf_path_hi.url)

#     def get_pdf_path_gu(self, obj):
#         request = self.context.get('request')
#         return request.build_absolute_uri(obj.pdf_path_gu.url)

