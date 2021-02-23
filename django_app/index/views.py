import dateparser
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import Http404, JsonResponse
from django.forms.utils import ErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth.models import User
from django.conf import settings

from fusionauth.fusionauth_client import FusionAuthClient
import pkce
import json
import urllib
#import requests


def get_or_create_user(user_id, request):
    user = User.objects.filter(username=user_id).first()

    if not user:
        user = User(username=user_id)
        user.save()

    return user


def get_login_url(request):
    #redirect_url = request.build_absolute_uri(reverse("dash"))
    #redirect_url = urllib.parse.quote(redirect_url)
    if ('pkce_verifier' in request.session) is False or ('code_challenge' in request.session) is False:
        code_verifier = pkce.generate_code_verifier(length=128)
        code_challenge = pkce.get_code_challenge(code_verifier)
        request.session['pkce_verifier'] = code_verifier
        request.session['code_challenge'] = code_challenge
    redirect_url = urllib.parse.quote(settings.LOGIN_REDIRECT_URL)
    login_url = f"{settings.FUSION_AUTH_BASE_URL}/oauth2/authorize"\
        f"?client_id={settings.FUSION_AUTH_APP_ID}&redirect_uri={redirect_url}&response_type=code"\
        f"&code_challenge={request.session['code_challenge']}&code_challenge_method=S256"
    return login_url


def is_user_login_ok(request):
    print("starting login")
    client = FusionAuthClient(settings.FUSION_AUTH_API_KEY, settings.FUSION_AUTH_INTERNAL_API_URL)

    code = request.GET.get("code")
    print(f"{code=}")

    if not code:
        print("no code")
        return False

    try:
        #redirect_url = request.build_absolute_uri(reverse("dash"))
        redirect_url = settings.LOGIN_REDIRECT_URL
        print(f"{redirect_url=}")
        # if you are using version 1.19.x of the python library or later, use this
        r = client.exchange_o_auth_code_for_access_token_using_pkce(
            code,
            redirect_url,
            request.session['pkce_verifier'],
            client_id=settings.FUSION_AUTH_APP_ID,
            client_secret=settings.FUSION_AUTH_CLIENT_SECRET)
        was_successful = r.was_successful()
        print(f"{was_successful=}")
        if was_successful:
            access_token = r.success_response["access_token"]
            user_id = r.success_response["userId"]
            get_or_create_user(user_id, request)
            return user_id
        else:
            print(r.error_response)
            return False

    except Exception as exc:
        print(f"{exc=}")


class HomeView(View):
    def get(self, request):
        num_users = User.objects.count()
        login_url = get_login_url(request)
        return render(request, "index/fhome.html", {"login_url": login_url, "num_users": num_users},)


class DashView(View):
    def get(self, request):

        login_url = get_login_url(request)
        user_id = is_user_login_ok(request)

        if not user_id:
            return redirect(login_url)

        birthday = None
        user = None

        try:
            client = FusionAuthClient(settings.FUSION_AUTH_API_KEY, settings.FUSION_AUTH_INTERNAL_API_URL)
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

        return render(request, "index/dash.html", {"user": user, "birthday": birthday})

    def post(self, request):

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
                "index/dash.html",
                {"message": "Couldn't parse birthday. Please use YYYY-MM-DD",
                    "user_id": user_id},
            )

        try:
            client = FusionAuthClient(
                settings.FUSION_AUTH_API_KEY, settings.FUSION_AUTH_INTERNAL_API_URL
            )
            r = client.patch_user(
                user_id, {"user": {"birthDate": normalised_birthday}}
            )
            if r.was_successful():
                print(r.success_response)
                return render(
                    request,
                    "index/dash.html",
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
                    "index/dash.html",
                    {"message": "Something went wrong",
                        "user": r.error_response["user"]},
                )
        except Exception as e:
            print(e)
            return render(
                request,
                "index/dash.html",
                {"message": "Something went wrong"},
            )


class SignupView(View):
    def get(self, request):
        login_url = get_login_url(request)
        return render(request, "registration/signup.html", {"login_url": login_url},)


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        request.session.clear()
        # redirect_url = request.build_absolute_uri("fhome")
        url = f"{settings.FUSION_AUTH_BASE_URL}/oauth2/logout?client_id={settings.FUSION_AUTH_APP_ID}"
        return redirect(url)
