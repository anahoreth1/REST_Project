from django.urls import path
from .views import UserCreateView, UserCreateViewById

urlpatterns = [
    path("users/", UserCreateView.as_view()),
    path("users/<int:user_id>/", UserCreateViewById.as_view())
]
