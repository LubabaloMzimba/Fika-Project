from django.urls import path
from .views import AcceptRideView, CreateRideView, AvailableRidesView


urlpatterns = [
    path('request/', CreateRideView.as_view(), name='request-ride'),
    path('available/', AvailableRidesView.as_view(), name='available-rides'),
    path('<int:ride_id>/accept/', AcceptRideView.as_view(), name='accept-ride'),
]