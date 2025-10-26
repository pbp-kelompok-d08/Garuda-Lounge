# news/admin.py
from django.contrib import admin
from .models import News, Comment

# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'news_views', 'is_featured', 'created_at')
    list_filter  = ('category', 'is_featured', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)

# Register Comment model
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('news', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username', 'news__title')
