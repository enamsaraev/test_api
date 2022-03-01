from django.contrib import admin

from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    """Панель поста в админке"""
    list_display = ['title', 'user', 'created_at']


admin.site.register(models.Subscription)
# Register your models here.
