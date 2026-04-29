from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import User, UserProfile
from core.serializers.social_login import SocialLoginSerializer
from core.services.auth import auth_provider_factory


class SocialLoginView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SocialLoginSerializer
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        auth_provider = auth_provider_factory.get_provider(request.data.get("provider"))

        if not auth_provider.is_credentials_valid(request.data):
            raise AuthenticationFailed

        email = request.data.get("email")
        first_name = request.data.get("first_name", "")
        auth_provider = request.data.get("provider")
        description = request.data.get("description", "")

        user = User.objects.get_or_create(
            username=email,
            email=email,
            first_name=first_name,
            provider=auth_provider,
        )

        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                "description": description,
            },
        )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
