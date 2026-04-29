from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import Article, ArticleView, Comment, Like, User, UserProfile

admin.site.register(User, UserAdmin)
admin.site.register(Article)
admin.site.register(ArticleView)
admin.site.register(Like)
admin.site.register(UserProfile)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    raw_id_fields = ("parent_comment", "author", "article")
