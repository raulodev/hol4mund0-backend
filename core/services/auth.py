from abc import ABC, abstractmethod
from typing import Literal

import requests
from django.conf import settings
from requests_oauthlib import OAuth1


class BaseAuthProvider(ABC):
    @abstractmethod
    def is_credentials_valid(self, data: dict) -> bool:
        raise NotImplementedError


class DefaultAuthProvider(BaseAuthProvider):
    def is_credentials_valid(self, data: dict):
        return False


class GithubAuthProvider(BaseAuthProvider):
    def is_credentials_valid(self, data: dict):
        access_token = data.get("access_token")

        if not access_token:
            return False

        resp = requests.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if resp.status_code != 200:
            return False

        return True


class TwitterAuthProvider(BaseAuthProvider):
    def is_credentials_valid(self, data: dict):
        oauth_token = data.get("oauth_token")
        oauth_token_secret = data.get("oauth_token_secret")

        if not oauth_token or not oauth_token_secret:
            return False

        auth = OAuth1(
            settings.TWITTER_ACCESS_KEY,
            settings.TWITTER_SECRET_KEY,
            oauth_token,
            oauth_token_secret,
        )

        resp = requests.get(
            "https://api.twitter.com/1.1/account/verify_credentials.json", auth=auth
        )

        if resp.status_code != 200:
            return False

        return True


class AuthProviderFactory:
    def __init__(self):
        self.providers = {
            "github": GithubAuthProvider(),
            "twitter": TwitterAuthProvider(),
        }

    def get_provider(self, provider: Literal["github", "twitter"]) -> BaseAuthProvider:
        return self.providers.get(provider, DefaultAuthProvider())


auth_provider_factory = AuthProviderFactory()
