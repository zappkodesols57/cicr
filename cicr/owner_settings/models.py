from django.db import models
# Create your models here.

class pest_incidence_data(models.Model):
    user_id = models.CharField(max_length=100,default='')
    date_field = models.DateField(null=True, blank=True)
    pest_date = models.CharField(max_length=100, null=True, blank=True)
    week = models.CharField(max_length=100, null=True, blank=True)
    standard_week = models.CharField(max_length=100, null=True, blank=True)
    name_of_investigator = models.CharField(max_length=100, null=True, blank=True)
    month =  models.CharField(max_length=100, null=True, blank=True)
    year =  models.CharField(max_length=100, null=True, blank=True)
    district =  models.CharField(max_length=100, null=True, blank=True)
    
    # Jassid /3 leaves/plant
    jassid_irm_item1 = models.IntegerField(null=True, blank=True)
    jassid_irm_item2 = models.IntegerField(null=True, blank=True)
    jassid_irm_item3 = models.IntegerField(null=True, blank=True)
    jassid_irm_item4 = models.IntegerField(null=True, blank=True)
    jassid_irm_item5 = models.IntegerField(null=True, blank=True)
    jassid_irm_item6 = models.IntegerField(null=True, blank=True)
    jassid_irm_item7 = models.IntegerField(null=True, blank=True)
    jassid_irm_item8 = models.IntegerField(null=True, blank=True)
    jassid_irm_item9 = models.IntegerField(null=True, blank=True)
    jassid_irm_item10 = models.IntegerField(null=True, blank=True)
    jassid_irm_average = models.FloatField(null=True, blank=True)
    
    jassid_nonirm_item1 = models.IntegerField(null=True, blank=True)
    jassid_nonirm_item2 = models.IntegerField(null=True, blank=True)
    jassid_nonirm_item3 = models.IntegerField(null=True, blank=True)
    jassid_nonirm_item4 = models.IntegerField(null=True, blank=True)
    jassid_nonirm_item5 = models.IntegerField(null=True, blank=True)
    jassid_nonirm_item6 = models.IntegerField(null=True, blank=True)
    jassid_nonirm_item7 = models.IntegerField(null=True, blank=True)
    jassid_nonirm_item8 = models.IntegerField(null=True, blank=True)
    jassid_nonirm_item9 = models.IntegerField(null=True, blank=True)
    jassid_nonirm_item10 = models.IntegerField(null=True, blank=True)
    jassid_nonirm_average = models.FloatField(null=True, blank=True)
    
    # Whitefly /3 leaves/plant
    whitefly_irm_item1 = models.IntegerField(null=True, blank=True)
    whitefly_irm_item2 = models.IntegerField(null=True, blank=True)
    whitefly_irm_item3 = models.IntegerField(null=True, blank=True)
    whitefly_irm_item4 = models.IntegerField(null=True, blank=True)
    whitefly_irm_item5 = models.IntegerField(null=True, blank=True)
    whitefly_irm_item6 = models.IntegerField(null=True, blank=True)
    whitefly_irm_item7 = models.IntegerField(null=True, blank=True)
    whitefly_irm_item8 = models.IntegerField(null=True, blank=True)
    whitefly_irm_item9 = models.IntegerField(null=True, blank=True)
    whitefly_irm_item10 = models.IntegerField(null=True, blank=True)
    whitefly_irm_average = models.FloatField(null=True, blank=True)
    
    whitefly_nonirm_item1 = models.IntegerField(null=True, blank=True)
    whitefly_nonirm_item2 = models.IntegerField(null=True, blank=True)
    whitefly_nonirm_item3 = models.IntegerField(null=True, blank=True)
    whitefly_nonirm_item4 = models.IntegerField(null=True, blank=True)
    whitefly_nonirm_item5 = models.IntegerField(null=True, blank=True)
    whitefly_nonirm_item6 = models.IntegerField(null=True, blank=True)
    whitefly_nonirm_item7 = models.IntegerField(null=True, blank=True)
    whitefly_nonirm_item8 = models.IntegerField(null=True, blank=True)
    whitefly_nonirm_item9 = models.IntegerField(null=True, blank=True)
    whitefly_nonirm_item10 = models.IntegerField(null=True, blank=True)
    whitefly_nonirm_average = models.FloatField(null=True, blank=True)
    
    # Thrips /3 leaves/plant
    thrips_irm_item1 = models.IntegerField(null=True, blank=True)
    thrips_irm_item2 = models.IntegerField(null=True, blank=True)
    thrips_irm_item3 = models.IntegerField(null=True, blank=True)
    thrips_irm_item4 = models.IntegerField(null=True, blank=True)
    thrips_irm_item5 = models.IntegerField(null=True, blank=True)
    thrips_irm_item6 = models.IntegerField(null=True, blank=True)
    thrips_irm_item7 = models.IntegerField(null=True, blank=True)
    thrips_irm_item8 = models.IntegerField(null=True, blank=True)
    thrips_irm_item9 = models.IntegerField(null=True, blank=True)
    thrips_irm_item10 = models.IntegerField(null=True, blank=True)
    thrips_irm_average = models.FloatField(null=True, blank=True)
    
    thrips_nonirm_item1 = models.IntegerField(null=True, blank=True)
    thrips_nonirm_item2 = models.IntegerField(null=True, blank=True)
    thrips_nonirm_item3 = models.IntegerField(null=True, blank=True)
    thrips_nonirm_item4 = models.IntegerField(null=True, blank=True)
    thrips_nonirm_item5 = models.IntegerField(null=True, blank=True)
    thrips_nonirm_item6 = models.IntegerField(null=True, blank=True)
    thrips_nonirm_item7 = models.IntegerField(null=True, blank=True)
    thrips_nonirm_item8 = models.IntegerField(null=True, blank=True)
    thrips_nonirm_item9 = models.IntegerField(null=True, blank=True)
    thrips_nonirm_item10 = models.IntegerField(null=True, blank=True)
    thrips_nonirm_average = models.FloatField(null=True, blank=True)
    
    # % Flowers Infestation
    flowers_irm_item1 = models.IntegerField(null=True, blank=True)
    flowers_irm_item2 = models.IntegerField(null=True, blank=True)
    flowers_irm_item3 = models.IntegerField(null=True, blank=True)
    flowers_irm_item4 = models.IntegerField(null=True, blank=True)
    flowers_irm_item5 = models.IntegerField(null=True, blank=True)
    flowers_irm_item6 = models.IntegerField(null=True, blank=True)
    flowers_irm_item7 = models.IntegerField(null=True, blank=True)
    flowers_irm_item8 = models.IntegerField(null=True, blank=True)
    flowers_irm_item9 = models.IntegerField(null=True, blank=True)
    flowers_irm_item10 = models.IntegerField(null=True, blank=True)
    flowers_irm_average = models.FloatField(null=True, blank=True)
    
    flowers_nonirm_item1 = models.IntegerField(null=True, blank=True)
    flowers_nonirm_item2 = models.IntegerField(null=True, blank=True)
    flowers_nonirm_item3 = models.IntegerField(null=True, blank=True)
    flowers_nonirm_item4 = models.IntegerField(null=True, blank=True)
    flowers_nonirm_item5 = models.IntegerField(null=True, blank=True)
    flowers_nonirm_item6 = models.IntegerField(null=True, blank=True)
    flowers_nonirm_item7 = models.IntegerField(null=True, blank=True)
    flowers_nonirm_item8 = models.IntegerField(null=True, blank=True)
    flowers_nonirm_item9 = models.IntegerField(null=True, blank=True)
    flowers_nonirm_item10 = models.IntegerField(null=True, blank=True)
    flowers_nonirm_average = models.FloatField(null=True, blank=True)
    
    # % Green boll Infestation
    green_irm_item1 = models.IntegerField(null=True, blank=True)
    green_irm_item2 = models.IntegerField(null=True, blank=True)
    green_irm_item3 = models.IntegerField(null=True, blank=True)
    green_irm_item4 = models.IntegerField(null=True, blank=True)
    green_irm_item5 = models.IntegerField(null=True, blank=True)
    green_irm_item6 = models.IntegerField(null=True, blank=True)
    green_irm_item7 = models.IntegerField(null=True, blank=True)
    green_irm_item8 = models.IntegerField(null=True, blank=True)
    green_irm_item9 = models.IntegerField(null=True, blank=True)
    green_irm_item10 = models.IntegerField(null=True, blank=True)
    green_irm_average = models.FloatField(null=True, blank=True)
    
    green_nonirm_item1 = models.IntegerField(null=True, blank=True)
    green_nonirm_item2 = models.IntegerField(null=True, blank=True)
    green_nonirm_item3 = models.IntegerField(null=True, blank=True)
    green_nonirm_item4 = models.IntegerField(null=True, blank=True)
    green_nonirm_item5 = models.IntegerField(null=True, blank=True)
    green_nonirm_item6 = models.IntegerField(null=True, blank=True)
    green_nonirm_item7 = models.IntegerField(null=True, blank=True)
    green_nonirm_item8 = models.IntegerField(null=True, blank=True)
    green_nonirm_item9 = models.IntegerField(null=True, blank=True)
    green_nonirm_item10 = models.IntegerField(null=True, blank=True)
    green_nonirm_average = models.FloatField(null=True, blank=True)
    
    # % Locule Damage
    locule_irm_item1 = models.IntegerField(null=True, blank=True)
    locule_irm_item2 = models.IntegerField(null=True, blank=True)
    locule_irm_item3 = models.IntegerField(null=True, blank=True)
    locule_irm_item4 = models.IntegerField(null=True, blank=True)
    locule_irm_item5 = models.IntegerField(null=True, blank=True)
    locule_irm_item6 = models.IntegerField(null=True, blank=True)
    locule_irm_item7 = models.IntegerField(null=True, blank=True)
    locule_irm_item8 = models.IntegerField(null=True, blank=True)
    locule_irm_item9 = models.IntegerField(null=True, blank=True)
    locule_irm_item10 = models.IntegerField(null=True, blank=True)
    locule_irm_average = models.FloatField(null=True, blank=True)
    
    locule_nonirm_item1 = models.IntegerField(null=True, blank=True)
    locule_nonirm_item2 = models.IntegerField(null=True, blank=True)
    locule_nonirm_item3 = models.IntegerField(null=True, blank=True)
    locule_nonirm_item4 = models.IntegerField(null=True, blank=True)
    locule_nonirm_item5 = models.IntegerField(null=True, blank=True)
    locule_nonirm_item6 = models.IntegerField(null=True, blank=True)
    locule_nonirm_item7 = models.IntegerField(null=True, blank=True)
    locule_nonirm_item8 = models.IntegerField(null=True, blank=True)
    locule_nonirm_item9 = models.IntegerField(null=True, blank=True)
    locule_nonirm_item10 = models.IntegerField(null=True, blank=True)
    locule_nonirm_average = models.FloatField(null=True, blank=True)
    
    # Open Boll Infestation
    open_ball_irm_item1 = models.IntegerField(null=True, blank=True)
    open_ball_irm_item2 = models.IntegerField(null=True, blank=True)
    open_ball_irm_item3 = models.IntegerField(null=True, blank=True)
    open_ball_irm_item4 = models.IntegerField(null=True, blank=True)
    open_ball_irm_item5 = models.IntegerField(null=True, blank=True)
    open_ball_irm_item6 = models.IntegerField(null=True, blank=True)
    open_ball_irm_item7 = models.IntegerField(null=True, blank=True)
    open_ball_irm_item8 = models.IntegerField(null=True, blank=True)
    open_ball_irm_item9 = models.IntegerField(null=True, blank=True)
    open_ball_irm_item10 = models.IntegerField(null=True, blank=True)
    open_ball_irm_average = models.FloatField(null=True, blank=True)
    
    open_ball_nonirm_item1 = models.IntegerField(null=True, blank=True)
    open_ball_nonirm_item2 = models.IntegerField(null=True, blank=True)
    open_ball_nonirm_item3 = models.IntegerField(null=True, blank=True)
    open_ball_nonirm_item4 = models.IntegerField(null=True, blank=True)
    open_ball_nonirm_item5 = models.IntegerField(null=True, blank=True)
    open_ball_nonirm_item6 = models.IntegerField(null=True, blank=True)
    open_ball_nonirm_item7 = models.IntegerField(null=True, blank=True)
    open_ball_nonirm_item8 = models.IntegerField(null=True, blank=True)
    open_ball_nonirm_item9 = models.IntegerField(null=True, blank=True)
    open_ball_nonirm_item10 = models.IntegerField(null=True, blank=True)
    open_ball_nonirm_average = models.FloatField(null=True, blank=True)
    
    # Av Pheromone trap catches (No.) Per Trap/week
    pheromone_irm_item1 = models.IntegerField(null=True, blank=True)
    pheromone_irm_item2 = models.IntegerField(null=True, blank=True)
    pheromone_irm_item3 = models.IntegerField(null=True, blank=True)
    pheromone_irm_item4 = models.IntegerField(null=True, blank=True)
    pheromone_irm_item5 = models.IntegerField(null=True, blank=True)
    pheromone_irm_item6 = models.IntegerField(null=True, blank=True)
    pheromone_irm_item7 = models.IntegerField(null=True, blank=True)
    pheromone_irm_item8 = models.IntegerField(null=True, blank=True)
    pheromone_irm_item9 = models.IntegerField(null=True, blank=True)
    pheromone_irm_item10 = models.IntegerField(null=True, blank=True)
    pheromone_irm_average = models.FloatField(null=True, blank=True)
    
    pheromone_nonirm_item1 = models.IntegerField(null=True, blank=True)
    pheromone_nonirm_item2 = models.IntegerField(null=True, blank=True)
    pheromone_nonirm_item3 = models.IntegerField(null=True, blank=True)
    pheromone_nonirm_item4 = models.IntegerField(null=True, blank=True)
    pheromone_nonirm_item5 = models.IntegerField(null=True, blank=True)
    pheromone_nonirm_item6 = models.IntegerField(null=True, blank=True)
    pheromone_nonirm_item7 = models.IntegerField(null=True, blank=True)
    pheromone_nonirm_item8 = models.IntegerField(null=True, blank=True)
    pheromone_nonirm_item9 = models.IntegerField(null=True, blank=True)
    pheromone_nonirm_item10 = models.IntegerField(null=True, blank=True)
    pheromone_nonirm_average = models.FloatField(null=True, blank=True)
    
    # % incidence
    incidence_irm_item1 = models.IntegerField(null=True, blank=True)
    incidence_irm_item2 = models.IntegerField(null=True, blank=True)
    incidence_irm_item3 = models.IntegerField(null=True, blank=True)
    incidence_irm_item4 = models.IntegerField(null=True, blank=True)
    incidence_irm_item5 = models.IntegerField(null=True, blank=True)
    incidence_irm_item6 = models.IntegerField(null=True, blank=True)
    incidence_irm_item7 = models.IntegerField(null=True, blank=True)
    incidence_irm_item8 = models.IntegerField(null=True, blank=True)
    incidence_irm_item9 = models.IntegerField(null=True, blank=True)
    incidence_irm_item10 = models.IntegerField(null=True, blank=True)
    incidence_irm_average = models.FloatField(null=True, blank=True)
    
    incidence_nonirm_item1 = models.IntegerField(null=True, blank=True)
    incidence_nonirm_item2 = models.IntegerField(null=True, blank=True)
    incidence_nonirm_item3 = models.IntegerField(null=True, blank=True)
    incidence_nonirm_item4 = models.IntegerField(null=True, blank=True)
    incidence_nonirm_item5 = models.IntegerField(null=True, blank=True)
    incidence_nonirm_item6 = models.IntegerField(null=True, blank=True)
    incidence_nonirm_item7 = models.IntegerField(null=True, blank=True)
    incidence_nonirm_item8 = models.IntegerField(null=True, blank=True)
    incidence_nonirm_item9 = models.IntegerField(null=True, blank=True)
    incidence_nonirm_item10 = models.IntegerField(null=True, blank=True)
    incidence_nonirm_average = models.FloatField(null=True, blank=True)
    
    # % locular damage
    locular_damage_irm1 = models.IntegerField(null=True, blank=True)
    locular_damage_irm2 = models.IntegerField(null=True, blank=True)
    locular_damage_irm3 = models.IntegerField(null=True, blank=True)
    locular_damage_irm4 = models.IntegerField(null=True, blank=True)
    locular_damage_irm5 = models.IntegerField(null=True, blank=True)
    locular_damage_irm6 = models.IntegerField(null=True, blank=True)
    locular_damage_irm7 = models.IntegerField(null=True, blank=True)
    locular_damage_irm8 = models.IntegerField(null=True, blank=True)
    locular_damage_irm9 = models.IntegerField(null=True, blank=True)
    locular_damage_irm10 = models.IntegerField(null=True, blank=True)
    locular_damage_irm_average = models.FloatField(null=True, blank=True)
    
    locular_damage_nonirm1 = models.IntegerField(null=True, blank=True)
    locular_damage_nonirm2 = models.IntegerField(null=True, blank=True)
    locular_damage_nonirm3 = models.IntegerField(null=True, blank=True)
    locular_damage_nonirm4 = models.IntegerField(null=True, blank=True)
    locular_damage_nonirm5 = models.IntegerField(null=True, blank=True)
    locular_damage_nonirm6 = models.IntegerField(null=True, blank=True)
    locular_damage_nonirm7 = models.IntegerField(null=True, blank=True)
    locular_damage_nonirm8 = models.IntegerField(null=True, blank=True)
    locular_damage_nonirm9 = models.IntegerField(null=True, blank=True)
    locular_damage_nonirm10 = models.IntegerField(null=True, blank=True)
    locular_damage_nonirm_average = models.FloatField(null=True, blank=True)
    
    number_of_message = models.IntegerField(null=True, blank=True)
    delivered_to_number_of_farmer = models.IntegerField(null=True, blank=True)
    any_relevant_information = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name_of_investigator}-{self.week}-{self.standard_week}-{self.month}-{self.district}-{self.jassid_irm_average}-{self.jassid_nonirm_average}"
    

class monthly_physical_progress(models.Model):
    user_id = models.CharField(max_length=100,default='')
    date_field = models.DateField(null=True, blank=True)
    physical_date = models.CharField(max_length=100, null=True, blank=True)
    week = models.CharField(max_length=100, null=True, blank=True)
    name_of_investigator = models.CharField(max_length=100, null=True, blank=True)
    month = models.CharField(max_length=100, null=True, blank=True)
    year = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)

    pheromone_traps = models.CharField(max_length=100, null=True, blank=True)
    splat = models.CharField(max_length=100, null=True, blank=True)
    pb_rope = models.CharField(max_length=100, null=True, blank=True)
    neem_insecticides = models.CharField(max_length=100, null=True, blank=True)
    flonicamid = models.CharField(max_length=100, null=True, blank=True)
    trichocards = models.CharField(max_length=100, null=True, blank=True)
    quinalphos = models.CharField(max_length=100, null=True, blank=True)
    chlorpyriphos = models.CharField(max_length=100, null=True, blank=True)
    profenophos = models.CharField(max_length=100, null=True, blank=True)

    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user_id}-{self.date_field}-{self.district}"


class extension_activities_carried_out(models.Model):
    user_id = models.CharField(max_length=100,default='')
    date_field = models.DateField(null=True, blank=True)
    physical_date = models.CharField(max_length=100, null=True, blank=True)
    week = models.CharField(max_length=100, null=True, blank=True)
    name_of_investigator = models.CharField(max_length=100, null=True, blank=True)
    month = models.CharField(max_length=100, null=True, blank=True)
    year = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)

    # fields for number and benificiary farmers
    popular_artical_number = models.CharField(max_length=100, null=True, blank=True)
    popular_artical_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    popular_artical_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    press_release_number = models.CharField(max_length=100, null=True, blank=True)
    press_release_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    press_release_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    # Extension Material
    extension_material_booklet_number = models.CharField(max_length=100, null=True, blank=True)
    extension_material_booklet_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    extension_material_booklet_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    extension_material_leaflet_number = models.CharField(max_length=100, null=True, blank=True)
    extension_material_leaflet_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    extension_material_leaflet_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    extension_material_pamphlet_number = models.CharField(max_length=100, null=True, blank=True)
    extension_material_pamphlet_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    extension_material_pamphlet_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    extension_material_poster_number = models.CharField(max_length=100, null=True, blank=True)
    extension_material_poster_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    extension_material_poster_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    # Literature Distributed
    literature_distributed_booklet_number = models.CharField(max_length=100, null=True, blank=True)
    literature_distributed_booklet_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    literature_distributed_booklet_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    literature_distributed_leaflet_number = models.CharField(max_length=100, null=True, blank=True)
    literature_distributed_leaflet_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    literature_distributed_leaflet_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    literature_distributed_pamphlet_number = models.CharField(max_length=100, null=True, blank=True)
    literature_distributed_pamphlet_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    literature_distributed_pamphlet_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    # Voice Messages sent
    voice_messages_number = models.CharField(max_length=100, null=True, blank=True)
    voice_messages_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    voice_messages_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    # Field Visits
    field_visit_number = models.CharField(max_length=100, null=True, blank=True)
    field_visit_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    field_visit_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    # Farmer mela / Kisan mela
    farmer_mela_number = models.CharField(max_length=100, null=True, blank=True)
    farmer_mela_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    farmer_mela_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    # exhibition arranged
    exhibition_arranged_number = models.CharField(max_length=100, null=True, blank=True)
    exhibition_arranged_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    exhibition_arranged_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    # Farmers field training organized
    farmer_training_number = models.CharField(max_length=100, null=True, blank=True)
    farmer_training_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    farmer_training_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    # Training/ Workshop
    training_number = models.CharField(max_length=100, null=True, blank=True)
    training_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    training_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    # TV Show
    tv_show_number = models.CharField(max_length=100, null=True, blank=True)
    tv_show_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    tv_show_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    # Radio Talks
    radio_talks_numbers = models.CharField(max_length=100, null=True, blank=True)
    radio_talks_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    radio_talks_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    # Sensitization Workshop to ginning mills
    sensitization_workshop_number = models.CharField(max_length=100, null=True, blank=True)
    sensitization_workshop_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    sensitization_workshop_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    # Farmers Queries Replied
    farmers_queries_number = models.CharField(max_length=100, null=True, blank=True)
    farmers_queries_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    farmers_queries_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    # Lecture Delivered in training
    lectures_delivered_number = models.CharField(max_length=100, null=True, blank=True)
    lectures_delivered_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    lectures_delivered_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    # News clips
    news_clips_number = models.CharField(max_length=100, null=True, blank=True)
    news_clips_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    news_clips_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)

    # Visit of farmer to station/personal contact
    visit_of_farmers_numbers = models.CharField(max_length=100, null=True, blank=True)
    visit_of_farmers_beneficiary_male = models.CharField(max_length=100, null=True, blank=True)
    visit_of_farmers_beneficiary_female = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return f"{self.user_id}-{self.date_field}-{self.district}"
