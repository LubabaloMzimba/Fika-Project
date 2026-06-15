from django.contrib import admin
from .models import Ride

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ['rider', 'driver', 'status', 'pickup_address', 'dropoff_address', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['rider__email', 'driver__email', 'pickup_address', 'dropoff_address']