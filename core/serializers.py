from django.conf import settings
from rest_framework import serializers
from core.models import (
    Article,
    User,
    Comment,
    Like,
    ReportArticle,
    ReportComment,
    ReportUser,
)


class LikeSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author_id = serializers.ReadOnlyField(source="author.id")
    article_id = serializers.ReadOnlyField(source="article.id")

    class Meta:
        model = Like
        fields = ["id", "author", "author_id", "article_id", "article", "created_at"]


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    author_first_name = serializers.ReadOnlyField(source="author.first_name")
    author_description = serializers.ReadOnlyField(source="author.description")
    preview_image_author = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d %b %Y", read_only=True)
    replies = RecursiveField(many=True, read_only=True)
    parent_comment_author_username = serializers.ReadOnlyField(
        source="parent_comment.author.username"
    )
    parent_comment_author_first_name = serializers.ReadOnlyField(
        source="parent_comment.author.first_name"
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "author_id",
            "author_first_name",
            "preview_image_author",
            "author_description",
            "created_at",
            "article",
            "content",
            "parent_comment",
            "parent_comment_author_username",
            "parent_comment_author_first_name",
            "replies",
        ]

    def get_preview_image_author(self, obj):
        request = self.context.get("request")
        if request is not None:
            return f"{settings.API_BASE_URL}/user/{obj.author.id}/image"
        return None


class ArticleSerializer(serializers.ModelSerializer):
    author_id = serializers.ReadOnlyField(source="author.id")
    author_username = serializers.ReadOnlyField(source="author.username")
    author_first_name = serializers.ReadOnlyField(source="author.first_name")
    author_last_name = serializers.ReadOnlyField(source="author.last_name")
    author_preview_profile_image = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d %b %Y", read_only=True)
    updated_at = serializers.DateTimeField(format="%d %b %Y", read_only=True)
    likes = serializers.SerializerMethodField()
    count_likes = serializers.SerializerMethodField()
    preview_cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id",
            "author_id",
            "author_username",
            "author_first_name",
            "author_last_name",
            "author_preview_profile_image",
            "title",
            "content",
            "is_draft",
            "created_at",
            "updated_at",
            "tags",
            "slug",
            "views",
            "cover_image",
            "preview_cover_image",
            "likes",
            "count_likes",
            "comments",
        ]

    def get_count_likes(self, obj):
        likes = Like.objects.filter(article=obj.id)
        return len([like.author.id for like in likes])

    def get_likes(self, obj):
        request = self.context.get("request")
        if request is not None:
            return f"{settings.API_BASE_URL}/article/{obj.id}/likes/"
        return None

    def get_comments(self, obj):
        request = self.context.get("request")
        if request is not None:
            return f"{settings.API_BASE_URL}/article/{obj.id}/comments/"
        return None

    def get_preview_cover_image(self, obj):
        request = self.context.get("request")
        if request is not None:
            return f"{settings.API_BASE_URL}/article/{obj.id}/cover"
        return None

    def get_author_preview_profile_image(self, obj):
        request = self.context.get("request")
        if request is not None:
            return f"{settings.API_BASE_URL}/user/{obj.author.id}/image"
        return None


class UserSerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    preview_profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "description",
            "profile_image",
            "preview_profile_image",
            "provider",
            "first_name",
            "last_name",
            "website_url",
            "facebook_url",
            "instagram_url",
            "whatsapp_url",
            "telegram_url",
            "twitter_url",
            "github_url",
            "linkedin_url",
            "articles",
            "comments",
            "likes",
        ]
        read_only_fields = ["id", "email"]

    def get_articles(self, obj):
        request = self.context.get("request")
        if request is not None:
            return f"{settings.API_BASE_URL}/user/{obj.id}/articles/"
        return None

    def get_comments(self, obj):
        request = self.context.get("request")
        if request is not None:
            return f"{settings.API_BASE_URL}/user/{obj.id}/comments/"
        return None

    def get_preview_profile_image(self, obj):
        request = self.context.get("request")
        if request is not None:
            return f"{settings.API_BASE_URL}/user/{obj.id}/image"
        return None


class ReportArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = ReportArticle
        fields = ["id", "author", "article", "content", "created"]


class ReportCommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = ReportComment
        fields = ["id", "author", "comment", "content", "created"]


class ReportUserSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = ReportUser
        fields = ["id", "author", "user", "content", "created"]
