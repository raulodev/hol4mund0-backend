from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView

from core.views.articles import ArticleDetailView, ArticleListCreateView
from core.views.likes import SyncLikeView
from core.views.users import MeView

urlpatterns = [
    path("v1/token/", TokenObtainPairView.as_view()),
    path("v1/articles/", ArticleListCreateView.as_view()),
    path("v1/articles/<int:pk>/", ArticleDetailView.as_view()),
    path("v1/me/", MeView.as_view()),
    path("v1/likes/", SyncLikeView.as_view()),
    path("v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
