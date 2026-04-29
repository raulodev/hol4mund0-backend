from rest_framework import serializers


class SocialLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    description = serializers.CharField()
    username = serializers.CharField()
    provider = serializers.CharField()
    access_token = serializers.CharField()
    oauth_token = serializers.CharField()
    oauth_token_secret = serializers.CharField()
