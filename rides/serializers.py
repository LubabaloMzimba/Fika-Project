from rest_framework import serializers
from .models import Ride
from users.serializers import UserSerializer


class CreateRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['pickup_address', 'pickup_latitude', 'pickup_longitude', 'dropoff_address', 'dropoff_latitude', 'dropoff_longitude']


class RideSerializer(serializers.ModelSerializer):
    rider = UserSerializer(read_only=True)
    driver = UserSerializer(read_only=True)

    class Meta:
        model = Ride
        fields = ['id', 'rider', 'driver', 'status', 'pickup_address', 'pickup_latitude', 'pickup_longitude', 'dropoff_address', 'dropoff_latitude', 'dropoff_longitude', 'created_at', 'updated_at', 'pickup_otp', 'dropoff_otp']