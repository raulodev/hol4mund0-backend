from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from core.models import Like
from core.serializers.likes import LikeSerializer


@extend_schema(
    summary="Create or remove a like on a publication",
    description="If a like already exists for the specified article, it is removed. Otherwise, a new like is created.",
    request=LikeSerializer,
    responses={
        201: LikeSerializer,
        204: {},
    },
)
class SyncLikeView(generics.CreateAPIView):
    """
    If the like of a publication exists,
    it is removed otherwise it is created
    """

    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        like, is_deleted = Like.objects.create_or_delete(
            author=request.user, article_id=request.data.get("article")
        )
        if is_deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
