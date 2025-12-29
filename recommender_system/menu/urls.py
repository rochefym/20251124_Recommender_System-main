from django.urls import path
from .views import MenuItemListCreate, MenuItemDetail, MenuByDayView, UploadMenuCSV, MenuDayList

urlpatterns = [
    path("items/", MenuItemListCreate.as_view()),
    path("items/<int:pk>/", MenuItemDetail.as_view()),
    path("day/<int:day_index>/", MenuByDayView.as_view()),
    path("days/", MenuDayList.as_view()),
    path("upload-csv/", UploadMenuCSV.as_view()),
]
