from django.urls import path
from .views import AcceptRideView, CreateRideView, AvailableRidesView, StartRideView, CompleteRideView


urlpatterns = [
    path('request/', CreateRideView.as_view(), name='request-ride'),
    path('available/', AvailableRidesView.as_view(), name='available-rides'),
    path('<int:ride_id>/accept/', AcceptRideView.as_view(), name='accept-ride'),
    path('<int:ride_id>/start/', StartRideView.as_view(), name='start-ride'),
    path('<int:ride_id>/complete/', CompleteRideView.as_view(), name='complete-ride'),
]