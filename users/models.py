from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):

    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not phone_number:
            raise ValueError('Users must have a phone number')
        
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, phone_number, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):

    RIDER = 'rider'
    DRIVER = 'driver'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (RIDER, 'Rider'),
        (DRIVER, 'Driver'),
        (ADMIN, 'Admin'),
    ]

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name', 'role']

    def __str__(self):
        return f'{self.email} ({self.role})'



class DriverProfile(models.Model):

    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

    VERIFICATION_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(max_length=20, unique=True)
    license_expiry_date = models.DateField()
    car_make = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    plate_number = models.CharField(max_length=20, unique=True)
    is_available = models.BooleanField(default=False)
    verification_status = models.CharField(max_length=10, choices=VERIFICATION_CHOICES, default = PENDING )


    def __str__(self):
        return f'{self.user.email} - {self.verification_status }'