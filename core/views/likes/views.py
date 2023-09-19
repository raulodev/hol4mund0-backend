from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status

from core.serializers import LikeSerializer
from core.models import Like


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        article_id = data.get("article")

        try:
            like = Like.objects.get(author=user, article=article_id)
            like.delete()

            return Response(
                {"detail": "Ya existe un like para este usuario y artículo."},
                status=status.HTTP_204_NO_CONTENT,
            )

        except Like.DoesNotExist:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(author=user)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )


class GetLikesViews(APIView):
    """
    Retorna los id de los usuarios que le han dado like a la publicación
    """

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        likes = Like.objects.filter(article=kwargs.get("article"))
        return Response([like.author.id for like in likes])
