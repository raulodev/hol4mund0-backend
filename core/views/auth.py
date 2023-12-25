import re
import random
import string
import requests
from requests_oauthlib import OAuth1
from django.conf import settings
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import User


class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        username = request.data.get("username")

        if not verify_credentials(email, username, request.data):
            return Response(
                {
                    "error": "Los datos proporcionados no son correctos",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if email_exists(email):
            user = User.objects.get(email=email)

        else:
            if username_exists(username):
                username = create_random_username()

            user = User.objects.create(
                username=username,
                email=email,
                first_name=request.data.get("first_name", ""),
                provider=request.data.get("provider"),
                description=request.data.get("description", ""),
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": user.username,
                "token": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


def email_exists(email: str) -> bool:
    return User.objects.filter(email=email).exists()


def username_exists(username: str) -> bool:
    return User.objects.filter(username=username).exists()


def create_random_username() -> str:
    letters = string.ascii_lowercase
    numbers = string.digits
    chars = letters + numbers
    return "".join(random.choice(chars) for _ in range(15))


def verify_credentials(email, username, data) -> bool:
    """verificar que los datos enviados son correctos"""

    provider = data.get("provider")

    providers = ("github", "twitter")

    if not username or not email or provider not in providers:
        return False

    elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        return False

    # Comprobar las credenciales de github
    if provider == "github":
        access_token = data.get("access_token")

        if not access_token:
            return False

        resp = requests.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if resp.status_code != 200:
            return False

    # Comprobar las credenciales en twitter
    elif provider == "twitter":
        oauth_token = data.get("oauth_token")
        oauth_token_secret = data.get("oauth_token_secret")

        if not oauth_token or not oauth_token_secret:
            return False

        auth = OAuth1(
            settings.CONSUMER_KEY,
            settings.CONSUMER_SECRET,
            oauth_token,
            oauth_token_secret,
        )

        resp = requests.get(
            "https://api.twitter.com/1.1/account/verify_credentials.json", auth=auth
        )


        if resp.status_code != 200:
            return False


    return True
