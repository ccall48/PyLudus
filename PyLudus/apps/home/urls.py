from PyLudus.apps.home.views import dash, home, logout, signup
from django.urls import path


urlpatterns = [
    path("", home.HomeView.as_view(), name="fhome"),
    path("dash", dash.DashView.as_view(), name="dash"),
    path("signup", signup.SignupView.as_view(), name="signup"),
    path("logout", logout.LogoutView.as_view(), name="logout"),
]
