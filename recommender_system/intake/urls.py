from django.urls import path
from .views import CalculateIntake

urlpatterns = [
    path("calculate/", CalculateIntake.as_view()),
]