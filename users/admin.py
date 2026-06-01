from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, DriverProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_active']

    fieldsets = (
        (None, {'fields': ('email', 'password', 'phone_number')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('date_joined', 'last_login')}),
    )

    add_fieldsets = (
        (None, { 
            'classes': ('wide',),
            'fields': ('first_name', 'last_name','email', 'phone_number', 'role', 'password1', 'password2'),
        }),
    )

    readonly_fields = ['date_joined', 'last_login']



@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 
        'car_make', 
        'car_model', 
        'plate_number', 
        'is_available', 
        'verification_status'
    ]
    list_filter = ['verification_status', 'is_available']
    search_fields = ['user__email', 'license_number', 'plate_number']
    readonly_fields = ['user']