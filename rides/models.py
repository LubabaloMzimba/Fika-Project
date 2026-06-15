from django.db import models
from users.models import User



class Ride(models.Model):


    REQUESTED = 'requested'
    ACCEPTED = 'accepted'
    ONGOING = 'ongoing'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


    STATUS_CHOICES = [
        (REQUESTED, 'Requested'),
        (ACCEPTED, 'Accepted'),
        (ONGOING, 'Ongoing'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    rider = models.ForeignKey(User, 
                              on_delete=models.PROTECT, 
                              related_name='rides_as_rider'
                            )
    
    driver = models.ForeignKey(User,
                                 on_delete=models.PROTECT, 
                                 related_name='rides_as_driver',
                                 null=True,
                                 blank=True
                                )
    
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default=REQUESTED
                            )
    
    pickup_address = models.CharField(max_length=255)
    pickup_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_longitude = models.DecimalField(max_digits=9, decimal_places=6)

    dropoff_address = models.CharField(max_length=255)
    dropoff_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    dropoff_longitude = models.DecimalField(max_digits=9, decimal_places=6)

    pickup_otp = models.CharField(max_length=6, blank=True, null=True)
    dropoff_otp = models.CharField(max_length=6, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.rider} → {self.driver} ({self.status})'