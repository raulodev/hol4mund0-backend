from rest_framework import generics

from core.models import Comment
from core.permissions import IsAuthorOrReadOnly
from core.serializers.comments import CreateCommentSerializer


class CreateCommentView(generics.CreateAPIView):
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class DeleteCommentView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
