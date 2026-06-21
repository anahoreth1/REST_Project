from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, UserCreateView, UserCreateViewById

urlpatterns = [
    path("users/", UserCreateView.as_view()),
    path("users/<int:user_id>/", UserCreateViewById.as_view()),
    path("users/login/", LoginView.as_view()),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
