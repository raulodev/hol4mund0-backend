from rest_framework import generics, status
from rest_framework.response import Response
from core.models import Article, Comment
from core.permissions import IsAuthorOrReadOnly
from core.serializers.comments import CreateCommentSerializer, ListCommentSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(parent_comment=None).order_by("id")
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ListCommentSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return super().get_queryset().filter(article_id=self.kwargs["article"])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, article_id=self.kwargs["article"])

    def create(self, request, *args, **kwargs):
        if not Article.objects.filter(id=kwargs["article"]).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        return super().create(request, *args, **kwargs)


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
