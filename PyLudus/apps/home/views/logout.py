from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import View


class LogoutView(View):
    """Account logout view, for clearing the session."""

    def get(self, request: WSGIRequest) -> HttpResponse:
        """HTTP GET: Return the view template and clear the session."""
        request.session.clear()
        # redirect_url = request.build_absolute_uri("fhome")
        url = (f"{settings.FUSION_AUTH_BASE_URL}/oauth2/logout"
               f"?client_id={settings.FUSION_AUTH_APP_ID}")
        return redirect(url)
