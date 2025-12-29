from django.urls import path
from .views import CalculateDRI

urlpatterns = [
    path("calculate/", CalculateDRI.as_view()),
]
