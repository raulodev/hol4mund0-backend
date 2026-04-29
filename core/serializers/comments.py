from rest_framework import serializers

from core.models import Comment
from core.serializers.common import RecursiveField
from core.serializers.users import PublicUserSerializer


class CreateCommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.id")
    article = serializers.ReadOnlyField(source="article.id")

    class Meta:
        model = Comment
        fields = "__all__"


class ListCommentSerializer(serializers.ModelSerializer):
    replies = RecursiveField(many=True, read_only=True)
    author = PublicUserSerializer()

    class Meta:
        model = Comment
        fields = ("id", "author", "content", "replies")
        depth = 1
