from django.urls import path
from . import views

app_name = "remove_bg"

urlpatterns = [
    path("", views.TestView.as_view(), name = "test"),
    path("download/", views.DownloadImages.as_view(), name = "download"),
]