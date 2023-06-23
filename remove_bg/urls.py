from django.urls import path
from . import views

app_name = "remove_bg"
urlpatterns = [
    path("", views.HomePage.as_view(), name = "homepage"),
]