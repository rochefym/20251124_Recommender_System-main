from django.urls import path
from .views import RagQueryByPatientView, RagQueryChineseView, RagQueryInChineseByPatientView, RagQueryView

urlpatterns = [
    path("query/", RagQueryView.as_view()),
    path("query", RagQueryView.as_view()),
    path("query/tr-cn/", RagQueryChineseView.as_view()),
    path("query/tr-cn", RagQueryChineseView.as_view()),
    path("recommendations/patient/<int:patient_id>", RagQueryByPatientView.as_view()),
    path("recommendations/patient/<int:patient_id>/", RagQueryByPatientView.as_view()),
    path("recommendations/patient/<int:patient_id>//", RagQueryByPatientView.as_view()),
    path("recommendations/patient/<int:patient_id>/tr-cn/", RagQueryInChineseByPatientView.as_view()),
    path("recommendations/patient/<int:patient_id>/tr-cn", RagQueryInChineseByPatientView.as_view()),
]
