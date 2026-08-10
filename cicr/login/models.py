from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission

class CustomUserManager(BaseUserManager):
    def _create_user(self, user_id, password, **extra_fields):
        if not user_id:
            raise ValueError("user_id Must Be Provided")
        if not password:
            raise ValueError("Password Must Be Provided")    

        user = self.model(
            user_id=user_id,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_id, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(user_id, password, **extra_fields)    

    def create_superuser(self, user_id, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(user_id, password, **extra_fields)    

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(db_index=True, unique=True, max_length=500, default='')
    salutation = models.CharField(max_length=500, default='', blank=True, null=True)
    first_name = models.CharField(max_length=500, default='', blank=True, null=True)
    middle_name = models.CharField(max_length=500, default='', blank=True, null=True)
    last_name = models.CharField(max_length=500, default='', blank=True, null=True)
    designation = models.CharField(max_length=500, default='', blank=True, null=True)
    category = models.CharField(max_length=500, default='', blank=True, null=True)
    mobile_number = models.CharField(max_length=240, unique=True, blank=True, null=True)
    email_id = models.EmailField(max_length=700, default='', blank=True, null=True)
    role_assign = models.CharField(max_length=500, default='', blank=True, null=True)
    joining_date = models.CharField(max_length=500, default='', blank=True, null=True)
    user_district = models.CharField(max_length=500, default='', blank=True, null=True)
    address = models.CharField(max_length=980, default='', blank=True, null=True)
    generated_pass = models.CharField(max_length=100, default='', blank=True, null=True)
    
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_user = models.BooleanField(default=False) 
    is_admin = models.BooleanField(default=False)
    is_farmer = models.BooleanField(default=False)
    is_investigator = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions_list', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['mobile_number', 'email_id', 'first_name', 'middle_name', 'last_name', ]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)




class investigator_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salutation = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    is_investigator = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    district = models.CharField(max_length=250, default="", null=True, blank=True)
    gender=models.CharField(max_length=100,default="",null=True,blank=True)

    def __str__(self):
        return f'{self.user} {self.email}'



class admin_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salutation = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    is_admin = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    district = models.CharField(max_length=250, default="", null=True, blank=True)
    gender=models.CharField(max_length=100,default="",null=True,blank=True)

    def __str__(self):
        return f'{self.user} {self.email}'




class Advisory(models.Model):
    week_en = models.CharField(max_length=10,null=True, blank=True)
    week_hi = models.CharField(max_length=10,null=True, blank=True)
    week_gu = models.CharField(max_length=10,null=True, blank=True)
    date_range_en = models.CharField(max_length=255,null=True, blank=True)
    date_range_hi = models.CharField(max_length=255,null=True, blank=True)
    date_range_gu = models.CharField(max_length=255,null=True, blank=True)
    month_en = models.CharField(max_length=20,null=True, blank=True)
    month_hi = models.CharField(max_length=20,null=True, blank=True)
    month_gu = models.CharField(max_length=20,null=True, blank=True)
    start_date_en = models.CharField(max_length=255,null=True, blank=True)
    start_date_hi = models.CharField(max_length=255,null=True, blank=True)
    start_date_gu = models.CharField(max_length=255,null=True, blank=True)
    path_pdf_en = models.FileField(upload_to='advisories/en/', max_length=255,null=True, blank=True)
    path_pdf_hi = models.FileField(upload_to='advisories/hi/', max_length=255,null=True, blank=True)
    path_pdf_gu = models.FileField(upload_to='advisories/gu/', max_length=255,null=True, blank=True)

    lang_1 = models.CharField(max_length=10, null=True, blank=True)
    lang_1_pdf = models.FileField(upload_to='advisories/', max_length=255,null=True, blank=True)
    lang_2 = models.CharField(max_length=10, null=True, blank=True)
    lang_2_pdf = models.FileField(upload_to='advisories/', max_length=255,null=True, blank=True)
    lang_3 = models.CharField(max_length=10, null=True, blank=True)
    lang_3_pdf = models.FileField(upload_to='advisories/', max_length=255,null=True, blank=True)
    lang_4 = models.CharField(max_length=10, null=True, blank=True)
    lang_4_pdf = models.FileField(upload_to='advisories/', max_length=255,null=True, blank=True)
    lang_5 = models.CharField(max_length=10, null=True, blank=True)
    lang_5_pdf = models.FileField(upload_to='advisories/', max_length=255,null=True, blank=True)
    lang_6 = models.CharField(max_length=10, null=True, blank=True)
    lang_6_pdf = models.FileField(upload_to='advisories/', max_length=255,null=True, blank=True)
    lang_7 = models.CharField(max_length=10, null=True, blank=True)
    lang_7_pdf = models.FileField(upload_to='advisories/', max_length=255,null=True, blank=True)


    def __str__(self):
        return f"Weekly Advisory {self.week_en}"


class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return f"Banner {self.id}"


class Financial_Year(models.Model):
    financial_year = models.CharField(max_length=10, null=True,blank=True)  # Format: 2024-2025
    
    def __str__(self):
        return f"Year {self.financial_year}"  
        