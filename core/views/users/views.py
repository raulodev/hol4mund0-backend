from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics
from rest_framework import viewsets

from core.serializers import UserSerializer
from core.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserDetailViewUsername(generics.RetrieveAPIView):
    """Devuelve los datos del usuario por el campo username"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"


class GetImageUser(APIView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get("pk"))
        image_data = open(user.profile_image.path, "rb").read()
        return HttpResponse(image_data, content_type="image/jpeg")


class GetMeView(APIView):
    http_method_names = ["post"]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(instance=request.user, context={"request": request})
        return Response(serializer.data)
