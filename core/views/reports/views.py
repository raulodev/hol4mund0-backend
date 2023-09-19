from rest_framework import permissions
from rest_framework import viewsets

from core.serializers import (
    ReportArticleSerializer,
    ReportCommentSerializer,
    ReportUserSerializer,
)
from core.models import ReportArticle, ReportComment, ReportUser


class ReportArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ReportArticleSerializer
    queryset = ReportArticle.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReportCommentViewSet(viewsets.ModelViewSet):
    serializer_class = ReportCommentSerializer
    queryset = ReportComment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReportUserViewSet(viewsets.ModelViewSet):
    serializer_class = ReportUserSerializer
    queryset = ReportUser.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
