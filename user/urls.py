from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegistrationView, RequestOTPView, VerifyOTPView, CustomTokenObtainPairView

app_name = "user"

urlpatterns = [
    path("register", UserRegistrationView.as_view(), name="register"),
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('otp/request', RequestOTPView.as_view(), name='request_otp'),
    path('otp/verify', VerifyOTPView.as_view(), name='verify_otp'),
]
