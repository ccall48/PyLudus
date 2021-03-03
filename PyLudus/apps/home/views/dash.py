import dateparser
from PyLudus.apps.home.views import get_login_url, is_user_login_ok
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from fusionauth.fusionauth_client import FusionAuthClient


class DashView(View):
    """The main landing page for the website."""

    def get(self, request: WSGIRequest) -> HttpResponse:
        """HTTP GET: Return the view template."""
        login_url = get_login_url(request)
        user_id = is_user_login_ok(request)

        if not user_id:
            return redirect(login_url)

        birthday = None
        user = None

        try:
            client = FusionAuthClient(
                settings.FUSION_AUTH_API_KEY, settings.FUSION_AUTH_INTERNAL_API_URL
            )
            print(f"{user_id=}")
            r = client.retrieve_user(user_id)
            if r.was_successful():
                user = r.success_response["user"]
                print(f"{user=}")
                birthday = r.success_response["user"].get("birthDate", None)
                print(f"{birthday=}")
            else:
                print("couldn't get user")
                print(r.error_response)
            print("render dashboard with ", user_id)
        except Exception as e:
            print("Error occurred while communicating with Fusion API")
            print(e)
            return redirect(login_url)

        return render(request, "home/dash.html", {"user": user, "birthday": birthday})

    def post(self, request: HttpRequest) -> HttpResponse:
        """HTTP POST: Set user birthdate."""
        birthday = request.POST.get("birthday")
        user_id = request.POST.get("user_id")
        normalised_birthday = None
        print(f"{birthday=}")
        print(f"{user_id=}")

        try:
            dt = dateparser.parse(birthday)
            normalised_birthday = dt.strftime("%Y-%m-%d")
        except Exception as e:
            print(e)
            print("Couldn't parse birthday")

        if not normalised_birthday:
            return render(
                request,
                "home/dash.html",
                {
                    "message": "Couldn't parse birthday. Please use YYYY-MM-DD",
                    "user_id": user_id,
                },
            )

        try:
            client = FusionAuthClient(
                settings.FUSION_AUTH_API_KEY, settings.FUSION_AUTH_INTERNAL_API_URL
            )
            r = client.patch_user(user_id, {"user": {"birthDate": normalised_birthday}})
            if r.was_successful():
                print(r.success_response)
                return render(
                    request,
                    "home/dash.html",
                    {
                        "message": "Your birthday has been set",
                        "birthday": normalised_birthday,
                        "user": r.success_response["user"],
                    },
                )
            else:
                print(r.error_response)
                return render(
                    request,
                    "home/dash.html",
                    {
                        "message": "Something went wrong",
                        "user": r.error_response["user"],
                    },
                )
        except Exception as e:
            print(e)
            return render(
                request,
                "home/dash.html",
                {"message": "Something went wrong"},
            )
