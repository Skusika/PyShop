from django.urls import path
from .views import (
    RegistrationAPIView,
    LogoutAPIView,
    GetUserView,
    CustomTokenRefreshView,
    CustomTokenObtainPairView,
)

app_name = "auth_app"
urlpatterns = [
    path("register/", RegistrationAPIView.as_view(), name="registration"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="login_refresh"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("me/", GetUserView.as_view(), name="get_user")
]
