from PyLudus.apps.home.views import get_login_url
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


class SignupView(View):
    """Account signup view, renders sign up page with unique url."""

    def get(self, request: WSGIRequest) -> HttpResponse:
        """HTTP GET: Return the view template."""
        login_url = get_login_url(request)
        return render(
            request,
            "registration/signup.html",
            {"login_url": login_url},
        )
