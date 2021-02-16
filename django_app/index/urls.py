from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='fhome'),
    path('dash', views.DashView.as_view(), name='dash'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('logout', views.LogoutView.as_view(), name='logout'),
]
