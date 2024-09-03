from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import CustomObtainPairView, UserRegistration, UserView, LogoutAPIView


app_name = "users"
urlpatterns = [
    path(
        "login/",
        CustomObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "login/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "register/",
        UserRegistration.as_view(),
        name="register",
    ),
    path(
        "",
        UserView.as_view(),
        name="user",
    ),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]
