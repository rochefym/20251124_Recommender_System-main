from django.urls import path
from .views import UserProfileList, UserProfileDetail

urlpatterns = [
    path("", UserProfileList.as_view()),
    path("<int:pk>/", UserProfileDetail.as_view()),
]
