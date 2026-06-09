from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import authenticate

from .models import User, DriverProfile



class RegisterSerializer(serializers.ModelSerializer):

    phone_number = PhoneNumberField()

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password',
            'password_confirm',
            'role',
        ]

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                {"password": "Password do not match."}
            )
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):

    phone_number = PhoneNumberField()
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"phone_number": "User with this phone number does not exist."}
            )
        
        user = authenticate(
            request=self.context.get('request'),
            username = user.email,
            password = password

        )

        if not user:
            raise serializers.ValidationError(
                'Incorrect password.'
    )

        if not user.is_active:
            raise serializers.ValidationError(
                'This account has been suspended.'
            )

        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'role',
            'is_active',
            'is_staff',
            'date_joined',
        ]
        read_only_fields = [
            'id',
            'date_joined',
            'is_staff',
            'is_active',
        ]

class DriverProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = DriverProfile
        fields  = [
            'id',
            'license_number',
            'license_expiry_date',
            'car_make',
            'car_model',
            'plate_number',
            'is_available',
            'verification_status',
            'license_photo',
            'profile_photo',
        ]
        read_only_fields = [
            'id',
            'is_available',
            'verification_status',
        ]