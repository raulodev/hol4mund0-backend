from rest_framework import generics, permissions

from core.serializers.users import UserSerializers


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
