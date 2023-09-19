from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    ReportArticle,
    Article,
    Comment,
    ReportComment,
)

admin.site.register(User, UserAdmin)
admin.site.register(ReportArticle)
admin.site.register(Article)
admin.site.register(ReportComment)
admin.site.register(Comment)
