from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import generics

from core.permissions import IsOwnerOrReadOnly
from core.serializers import CommentSerializer
from core.models import Comment


class CommentViewSets(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsListView(generics.ListAPIView):
    """Retorna los comentarios de un artículo"""

    serializer_class = CommentSerializer

    def get_queryset(self):
        article = self.kwargs["article"]
        return Comment.objects.filter(article=article, parent_comment=None)


class UserCommentsListView(generics.ListAPIView):
    """Retorna los comentarios de un usuario"""

    serializer_class = CommentSerializer

    def get_queryset(self):
        author = self.kwargs["author"]
        return Comment.objects.filter(author=author)
