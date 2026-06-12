from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, DriverProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('driver/profile/', DriverProfileView.as_view(), name='driver-profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]