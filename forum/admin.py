from django.contrib import admin
from .models import Comment, Forum


class CommentInline(admin.StackedInline):
    model = Comment


class ForumAdmin(admin.ModelAdmin):
    inlines = [CommentInline]


admin.site.register(Forum, ForumAdmin)
