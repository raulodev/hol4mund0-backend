from rest_framework import serializers

from core.models import Article


class ArticleSerializers(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.id")

    class Meta:
        model = Article
        fields = "__all__"
