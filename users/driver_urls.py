from django.urls import path
from .views import DriverProfileView

urlpatterns = [
    path('profile/', DriverProfileView.as_view(), name='driver-profile'),
]