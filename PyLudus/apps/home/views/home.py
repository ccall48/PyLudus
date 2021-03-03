from PyLudus.apps.home.views import get_login_url
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


class HomeView(View):
    """The for the website."""

    def get(self, request: WSGIRequest) -> HttpResponse:
        """HTTP GET: Return the view template."""
        num_users = User.objects.count()
        login_url = get_login_url(request)
        return render(
            request,
            "home/fhome.html",
            {"login_url": login_url, "num_users": num_users},
        )
