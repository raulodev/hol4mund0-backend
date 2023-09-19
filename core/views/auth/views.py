from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from core.serializers import RegisterSerializer
from core.models import User


class RegistrationViewSet(APIView):
    permission_classes = [permissions.AllowAny]
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data["email"])
        except ObjectDoesNotExist:
            try :
                # Si existe un usuario con el mismo "username"
                # cambiar a uno random
                user = User.objects.get(username=request.data["username"])
                request.data["username"]
            except ObjectDoesNotExist :
                pass
            
            
            user = User.objects.create(**request.data)

        serializer = RegisterSerializer(instance=user, context={"request": request})

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": serializer.data,
                "token": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
