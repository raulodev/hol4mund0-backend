import re
import random
import string
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import User


class RegistrationViewSet(APIView):
    permission_classes = [permissions.AllowAny]
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        username = request.data.get("username")

        if not is_valid(email, username):
            return Response(
                {
                    "error": "el username o email no son  válidos",
                    "username": username,
                    "email": email,
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
                provider=request.data.get("provider", ""),
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


def is_valid(email, username) -> bool:
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        return False

    if not username:
        return False

    return True
