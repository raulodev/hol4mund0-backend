from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import parsers
from rest_framework import status

from core.serializers import ArticleSerializer
from core.permissions import IsOwnerOrReadOnly
from core.pagination import CustomPagination
from core.models import Article


class ArticleViewset(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    pagination_class = CustomPagination
    queryset = Article.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ListAllArticlesView(generics.ListAPIView):
    """
    Devuelve una lista de artículos para la página
    principal con paginación y excluyendo los borradores
    """

    serializer_class = ArticleSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Article.objects.all().filter(is_draft=False)


class UserArticleListView(generics.ListAPIView):
    """
    Devuelve todos los artículos de un usuario
    """

    serializer_class = ArticleSerializer

    def get_queryset(self):
        author = self.kwargs["author"]
        return Article.objects.filter(author=author)


class UserArticleNotDraftListView(generics.ListAPIView):
    """
    Devuelve todos los artículos que no son borradores
    de un usuario por su nombre de usuario
    """

    serializer_class = ArticleSerializer

    def get_queryset(self):
        username = self.kwargs["author"]
        return Article.objects.filter(author__username=username, is_draft=False)


class RetrieveArticleView(generics.RetrieveAPIView):
    """
    Retorna los datos de un artículos por su slug
    - Vista creada para editar el artículo
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "slug"


class GetCoverImageView(APIView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get("pk"))
        image_data = open(article.cover_image.path, "rb").read()
        return HttpResponse(
            image_data, content_type="image/jpeg", status=status.HTTP_200_OK
        )


class ReadArticleView(APIView):
    """
    Retorna los datos de un artículos por su slug y autor
    y suma una vista
    - Vista creada para leer el artículo
    """

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        article = get_object_or_404(
            Article, author__username=kwargs.get("author"), slug=kwargs.get("slug")
        )
        article.increment_views()
        serializer = ArticleSerializer(article, context={"request": request})
        return Response(serializer.data)


class SearchView(APIView):
    def post(self, request, *args, **kwargs):
        query = request.data.get("query")

        articles = Article.objects.filter(title__icontains=query, is_draft=False)[:10]

        results = []
        for article in articles:
            results.append(
                {
                    "id": article.id,
                    "title": article.title,
                    "slug": article.slug,
                    "author": article.author.username,
                    "first_name": article.author.first_name,
                }
            )

        return Response(
            results,
            status=status.HTTP_200_OK,
        )
