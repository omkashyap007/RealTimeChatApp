from django.urls import path, include
from authentication import views as auth_views

urlpatterns = [
    path("login/",  auth_views.LoginPage, name="auth-login"),
    path("register/",  auth_views.RegisterPage, name="auth-register"),
    path("logout/", auth_views.LogoutPage, name="auth-logout"),
]
