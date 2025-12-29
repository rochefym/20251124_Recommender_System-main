# recommendations/urls.py
from django.urls import path
from .views import GenerateRecommendationView

urlpatterns = [
    path("generate/", GenerateRecommendationView.as_view()),
]