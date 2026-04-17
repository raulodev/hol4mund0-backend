from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


def directory_profile_images(instance, filename):
    return "profiles/{0}/{1}".format(instance.username, filename)


def directory_covers(instance, filename):
    return "covers/{0}/{1}".format(instance.author.username, filename)


class User(AbstractUser):
    class AuthProviderChoices(models.TextChoices):
        GITHUB = "GITHUB"
        TWITTER = "TWITTER"

    email = models.EmailField(_("email address"), unique=True)
    auth_provider = models.CharField(choices=AuthProviderChoices.choices, max_length=7)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_image = models.ImageField(
        upload_to=directory_profile_images, blank=True, null=True
    )
    description = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True)
    facebook = models.URLField(max_length=255, blank=True)
    instagram = models.URLField(max_length=255, blank=True)
    whatsapp = models.URLField(max_length=255, blank=True)
    telegram = models.URLField(max_length=255, blank=True)
    twitter = models.URLField(max_length=255, blank=True)
    github = models.URLField(max_length=255, blank=True)
    linkedin = models.URLField(max_length=255, blank=True)


class Article(models.Model):
    author = models.ForeignKey(User, related_name="articles", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    is_draft = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover_image = models.ImageField(upload_to=directory_covers, blank=True)
    tags = models.CharField(max_length=300)
    slug = AutoSlugField(populate_from="title", unique_with=["author__username"])

    def __str__(self):
        return self.title

    def increment_views(self):
        # TODO: add view
        ...


class ArticleView(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="views")
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    author = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name="likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["author", "article"]


class Comment(models.Model):
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, related_name="comments", on_delete=models.CASCADE
    )
    parent_comment = models.ForeignKey(
        "self", related_name="replies", null=True, blank=True, on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author
