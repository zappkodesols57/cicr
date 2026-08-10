from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import district,basic_servey_info,RepresentedPhotograph,AssessmentSeason,YearlyProgressReport,standard_weeks
from .models import *

admin.site.register(district)
admin.site.register(basic_servey_info)
admin.site.register(RepresentedPhotograph)
admin.site.register(AssessmentSeason)
admin.site.register(YearlyProgressReport)
admin.site.register(standard_weeks)
admin.site.register(NewsArticle)
