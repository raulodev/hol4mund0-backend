from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenVerifyView

from core.views.articles import views as articles_views
from core.views.comments import views as comments_views
from core.views.reports import views as reports_views
from core.views.likes import views as likes_views
from core.views.users import views as users_views
from core.views.auth import views as auth_views

router = routers.DefaultRouter()


router.register("api/articles", articles_views.ArticleViewset)
router.register("api/users", users_views.UserViewSet)
router.register("api/comments", comments_views.CommentViewSets)
router.register("api/reportarticle", reports_views.ReportArticleViewSet)
router.register("api/reportcomment", reports_views.ReportCommentViewSet)
router.register("api/reportuser", reports_views.ReportUserViewSet)
router.register("api/like", likes_views.LikeViewSet)


# authentication

# router.register(
#     "api/auth/register",
#     viewset=auth_views.RegistrationViewSet,
#     basename="auth-register",
# )

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api/auth/register/", auth_views.RegistrationViewSet.as_view()),
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # path("api/token/verify/", TokenVerifyView.as_view()),
]


# urls para los artículos
urlpatterns += [
    path(
        "api/search/",
        articles_views.SearchView.as_view(),
    ),
    path(
        "api/all/articles/",
        articles_views.ListAllArticlesView.as_view(),
    ),
    path(
        "api/article/read/<str:author>/<slug:slug>/",
        articles_views.ReadArticleView.as_view(),
    ),
    path(
        "api/article/edit/<slug:slug>/",
        articles_views.RetrieveArticleView.as_view(),
    ),
    path(
        "api/article/<int:pk>/cover/",
        articles_views.GetCoverImageView.as_view(),
    ),
    path(
        "api/article/<int:article>/comments/",
        comments_views.CommentsListView.as_view(),
    ),
    path(
        "api/article/<int:article>/likes/",
        likes_views.GetLikesViews.as_view(),
    ),
]

# urls para los usuarios
urlpatterns += [
    path("api/getme/", users_views.GetMeView.as_view()),
    path(
        "api/user/<int:author>/articles/",
        articles_views.UserArticleListView.as_view(),
    ),
    path(
        "api/user-articles/<str:author>/list/",
        articles_views.UserArticleNotDraftListView.as_view(),
    ),
    path(
        "api/user/<int:author>/comments/",
        comments_views.UserCommentsListView.as_view(),
    ),
    path(
        "api/user/<str:username>/detail/",
        users_views.UserDetailViewUsername.as_view(),
    ),
    path(
        "api/user/<int:pk>/image/",
        users_views.GetImageUser.as_view(),
    ),
]
