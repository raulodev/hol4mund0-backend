from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView

from core.views.articles import ArticleDetail, ArticleListCreateAPIView

urlpatterns = [
    path("v1/token/", TokenObtainPairView.as_view()),
    path("v1/articles/", ArticleListCreateAPIView.as_view()),
    path("v1/articles/<int:pk>/", ArticleDetail.as_view()),
    path("v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
