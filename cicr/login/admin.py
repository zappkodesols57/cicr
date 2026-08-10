from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,investigator_user,admin_user,Advisory,Banner,Financial_Year

class CustomUserAdmin(admin.ModelAdmin):
    model = User
    # Use 'user_id' for ordering if you want to order by user_id
    ordering = ['user_id']
    # List of fields to be displayed in the admin
    list_display = ('user_id', 'user_district', 'first_name', 'last_name', 'email_id', 'is_active','is_superuser','is_admin','is_investigator')

    # Fields to be used in search
    search_fields = ('user_id', 'user_district', 'first_name', 'last_name', 'email_id')

    # Fields to be used in filtering
    list_filter = ('is_staff', 'is_active', 'is_superuser')


# Register your custom user admin
admin.site.register(User, CustomUserAdmin)

admin.site.register(investigator_user)
admin.site.register(admin_user)

admin.site.register(Advisory)

admin.site.register(Banner)
admin.site.register(Financial_Year)
