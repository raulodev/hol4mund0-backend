from django_filters import rest_framework as filters
from rest_framework import generics, permissions

from core.models import Article
from core.permissions import IAuthorOrReadOnly
from core.serializers.articles import ArticleSerializers


class ArticleFilter(filters.FilterSet):
    class Meta:
        model = Article
        fields = {"title": ["icontains"], "author": ["exact"], "is_draft": ["exact"]}


class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.filter(is_draft=False).order_by("-id")
    serializer_class = ArticleSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = ArticleFilter

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializers
    permission_classes = [IAuthorOrReadOnly]
