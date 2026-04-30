from rest_framework import serializers

from core.models import Article
from core.serializers.users import PublicUserSerializer


class ArticleSerializers(serializers.ModelSerializer):
    author = PublicUserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"
        depth = 1
