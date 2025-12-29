from django.urls import path
from .views import GetOllamaLLMResponseView

urlpatterns = [
    path("prompt/", GetOllamaLLMResponseView.as_view()),
]



