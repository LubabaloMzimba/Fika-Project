from django.urls import path
from .views import CreateRideView


urlpatterns = [
    path('request/', CreateRideView.as_view(), name='request-ride')
]