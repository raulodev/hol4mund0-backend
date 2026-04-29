from rest_framework import serializers

from core.models import Comment
from core.serializers.common import RecursiveField


class CreateCommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.id")

    class Meta:
        model = Comment
        fields = "__all__"
