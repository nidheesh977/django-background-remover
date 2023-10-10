from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name = "login"),
    path("logout/", views.logout_view, name = "logout"),
    path("signup/", views.SignupView.as_view(), name = "signup"),
    path("forgot-password/", views.ForgotPassword.as_view(), name = "forgot-password"),
]