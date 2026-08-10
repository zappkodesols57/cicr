from django.db import models

# Create your models here.


class district(models.Model):
	district_name = models.CharField(max_length=100,null=True,blank=True,default='')

	def __str__(self):
		return self.district_name



from django.db import models
from datetime import date

class basic_servey_info(models.Model):
    # IRM and NON-IRM radio buttons
    IRM_CHOICES = [
        (True, 'IRM'),
        (False, 'NON-IRM')
    ]
    IRM = models.BooleanField(choices=IRM_CHOICES, default=False)

    user_id = models.CharField(max_length=100,default='')

    # Name of farmer
    name = models.CharField(max_length=100, null=True, blank=True, default='')
    category = models.CharField(max_length=100, null=True, blank=True, default='')
    
    # Gender
    gender= models.CharField(max_length=100, null=True, blank=True, default='')
    village = models.CharField(max_length=100, null=True, blank=True, default='')
    taluka = models.CharField(max_length=100, null=True, blank=True, default='')
 
    # District
    district = models.CharField(max_length=100)

    # Mobile number
    mobile_number = models.CharField(max_length=15)

    # Date of sowing
    date_of_sowing = models.DateField()

    # Spacing
    row_distance= models.CharField(max_length=100, null=True, blank=True, default='')
    plant_distance= models.CharField(max_length=100, null=True, blank=True, default='')
    # spacing = models.CharField(max_length=100)
    cotton_variety = models.CharField(max_length=100, null=True, blank=True, default='')
    previous_year_crop_grown = models.CharField(max_length=100, null=True, blank=True, default='')

    # Irrigation and rainfed checkboxes
    CAUSES_CHOICES = [
        (True, 'irrigation'),
        (False, 'rainfed')
    ]
    causes = models.BooleanField(choices=CAUSES_CHOICES, default=False)
    

    # Last year crop extended radio buttons
    LAST_YEAR_CROP_CHOICES = [
        (True, 'Yes'),
        (False, 'No')
    ]
    last_year_crop_extended = models.BooleanField(choices=LAST_YEAR_CROP_CHOICES, default=False)
    
    soil_type = models.CharField(max_length=100, blank=True, null=True)
    
    CROP_ROTATION_FOLLOWED = [
        (True, 'Yes'),
        (False, 'No')
    ]
    crop_rotation_followed = models.BooleanField(choices=CROP_ROTATION_FOLLOWED, default=False)
    advisory_received_from = models.CharField(max_length=500, null=True, blank=True, default='')
    
    recorded_file = models.FileField(upload_to='recorded_files/',blank=True, null=True, default='')
    
    # Geolocation (latitude and longitude)
    geolocations = models.CharField(max_length=900, null=True, blank=True, default='')

    total_farmers_ecommunication = models.IntegerField(null=True, blank=True)
    
    servey_date = models.DateField(null=True,blank=True)

    year =  models.CharField(max_length=100, null=True, blank=True)

    landarea = models.CharField(max_length=500,null=True, blank=True)

    aadhar_number = models.CharField(max_length=100,null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}-{self.user_id}-{self.servey_date}-{self.district}" if self.name else "Unnamed Farmer"



class RepresentedPhotograph(models.Model):
    user_id = models.CharField(max_length=100,default='')
    date_field = models.DateField(null=True, blank=True)
    physical_date = models.CharField(max_length=100, null=True, blank=True)
    week = models.CharField(max_length=100, null=True, blank=True)
    name_of_investigator = models.CharField(max_length=100, null=True, blank=True)
    month = models.CharField(max_length=100, null=True, blank=True)
    year = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)

    brief_activity_description_1 = models.TextField(null=True, blank=True)
    brief_activity_description_2 = models.TextField(null=True, blank=True)
    brief_activity_description_3 = models.TextField(null=True, blank=True)

    image_1 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_3 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_4 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_5 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_6 = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f"Represented Photograph {self.id}-{self.district}"


class AssessmentSeason(models.Model):
    user_id = models.CharField(max_length=100,default='')
    date_field = models.DateField(null=True, blank=True)
    physical_date = models.CharField(max_length=100, null=True, blank=True)
    week = models.CharField(max_length=100, null=True, blank=True)
    name_of_investigator = models.CharField(max_length=100, null=True, blank=True)
    month = models.CharField(max_length=100, null=True, blank=True)
    year = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)

    number_sucking = models.CharField(max_length=100, null=True, blank=True)
    number_bollworms = models.CharField(max_length=100, null=True, blank=True)

    cost_spray_sucking = models.CharField(max_length=100, null=True, blank=True)
    cost_spray_bollworms = models.CharField(max_length=100, null=True, blank=True)

    pesticide_reduction_cost = models.CharField(max_length=100, null=True, blank=True)
    pesticide_reduction_volume = models.CharField(max_length=100, null=True, blank=True)

    picking_1 = models.CharField(max_length=100, null=True, blank=True)
    picking_2 = models.CharField(max_length=100, null=True, blank=True)
    picking_3 = models.CharField(max_length=100, null=True, blank=True)
    picking_4 = models.CharField(max_length=100, null=True, blank=True)
    picking_5 = models.CharField(max_length=100, null=True, blank=True)
    picking_6 = models.CharField(max_length=100, null=True, blank=True)

    cost_ratio = models.CharField(max_length=100, null=True, blank=True)
    farmer_feedback = models.TextField(null=True, blank=True)

    success_stories = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Assessment Season {self.id}-{self.district}-{self.date_field}"


class YearlyProgressReport(models.Model):
    user_id = models.CharField(max_length=100,default='')
    date_field = models.DateField(null=True, blank=True)
    physical_date = models.CharField(max_length=100, null=True, blank=True)
    week = models.CharField(max_length=100, null=True, blank=True)
    name_of_investigator = models.CharField(max_length=100, null=True, blank=True)
    month = models.CharField(max_length=100, null=True, blank=True)
    year = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    village = models.CharField(max_length=100, null=True, blank=True)
    taluka = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    name_of_farmer = models.CharField(max_length=100, null=True, blank=True)

    CULTIVATION_CHOICES = [
        (True, 'irrigated'),
        (False, 'rainfed')
    ]
    cultivation = models.BooleanField(choices=CULTIVATION_CHOICES, default=False)

    cultivation_feedback = models.TextField(null=True, blank=True)

    spray_1_pesticide = models.CharField(max_length=500, null=True, blank=True)
    spray_1_dose = models.FloatField(null=True, blank=True)
    spray_1_target_pest = models.CharField(max_length=500, null=True, blank=True)

    spray_2_pesticide = models.CharField(max_length=500, null=True, blank=True)
    spray_2_dose = models.FloatField(null=True, blank=True)
    spray_2_target_pest = models.CharField(max_length=500, null=True, blank=True)

    spray_3_pesticide = models.CharField(max_length=500, null=True, blank=True)
    spray_3_dose = models.FloatField(null=True, blank=True)
    spray_3_target_pest = models.CharField(max_length=500, null=True, blank=True)

    spray_4_pesticide = models.CharField(max_length=500, null=True, blank=True)
    spray_4_dose = models.FloatField(null=True, blank=True)
    spray_4_target_pest = models.CharField(max_length=500, null=True, blank=True)

    spray_5_pesticide = models.CharField(max_length=500, null=True, blank=True)
    spray_5_dose = models.FloatField(null=True, blank=True)
    spray_5_target_pest = models.CharField(max_length=500, null=True, blank=True)

    spray_6_pesticide = models.CharField(max_length=500, null=True, blank=True)
    spray_6_dose = models.FloatField(null=True, blank=True)
    spray_6_target_pest = models.CharField(max_length=500, null=True, blank=True)

    spray_7_pesticide = models.CharField(max_length=500, null=True, blank=True)
    spray_7_dose = models.FloatField(null=True, blank=True)
    spray_7_target_pest = models.CharField(max_length=500, null=True, blank=True)

    spray_8_pesticide = models.CharField(max_length=500, null=True, blank=True)
    spray_8_dose = models.FloatField(null=True, blank=True)
    spray_8_target_pest = models.CharField(max_length=500, null=True, blank=True)

    spray_9_pesticide = models.CharField(max_length=500, null=True, blank=True)
    spray_9_dose = models.FloatField(null=True, blank=True)
    spray_9_target_pest = models.CharField(max_length=500, null=True, blank=True)

    spray_10_pesticide = models.CharField(max_length=500, null=True, blank=True)
    spray_10_dose = models.FloatField(null=True, blank=True)
    spray_10_target_pest = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"Yearly Progress Report {self.id}-{self.district}-{self.date_field}"


class standard_weeks(models.Model):
    standard_number = models.CharField(max_length=100,null=True,blank=True,default='')
    standard_week = models.CharField(max_length=100,null=True,blank=True,default='')

    date_field = models.DateField(null=True, blank=True)
    year = models.CharField(max_length=100, null=True, blank=True)

    weeks_value = models.CharField(max_length=100, null=True, blank=True)

    month_data = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Standard Weeks {self.standard_number}-{self.standard_week}-{self.date_field}"


class NewsArticle(models.Model):
    issue_no = models.CharField(max_length=800, null=True, blank=True, default='')  
    date = models.CharField(max_length=500, null=True, blank=True, default='')
    month = models.CharField(max_length=100, null=True, blank=True, default='')  
    pdf = models.FileField(upload_to='news_articles/', null=True, blank=True)  

    def __str__(self):  
        return f"Issue No: {self.issue_no} - Date: {self.date or 'N/A'}"

    # class Meta:  
    #     verbose_name = "News Article"  
    #     verbose_name_plural = "News Articles"

 