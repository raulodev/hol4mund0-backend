from django.contrib.auth.models import AbstractBaseUser, UserManager, Group, Permission
from django.db import models
from autoslug import AutoSlugField


def directory_profile_images(instance, filename):
    return "profiles/{0}/{1}".format(instance.username, filename)


def directory_covers(instance, filename):
    return "covers/{0}/{1}".format(instance.author.username, filename)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=255, blank=True)
    profile_image = models.ImageField(
        upload_to=directory_profile_images, blank=True, default="user.png"
    )
    provider = models.CharField(max_length=255, blank=True)

    website_url = models.CharField(max_length=255, blank=True)
    facebook_url = models.CharField(max_length=255, blank=True)
    instagram_url = models.CharField(max_length=255, blank=True)
    whatsapp_url = models.CharField(max_length=255, blank=True)
    telegram_url = models.CharField(max_length=255, blank=True)
    twitter_url = models.CharField(max_length=255, blank=True)
    github_url = models.CharField(max_length=255, blank=True)
    linkedin_url = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, blank=True)
    user_permissions = models.ManyToManyField(Permission, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, editable=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


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
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views += 1
        self.save()


class Like(models.Model):
    author = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name="likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, related_name="comments", on_delete=models.CASCADE
    )
    parent_comment = models.ForeignKey(
        "self", related_name="replies", null=True, blank=True, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.author.username


class ReportArticle(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.content


class ReportUser(models.Model):
    author = models.ForeignKey(
        User, related_name="report_user", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.content


class ReportComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.content
