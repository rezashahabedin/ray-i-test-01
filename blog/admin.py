from django.contrib import admin
from .models import Post, Category
from django.contrib.auth.models import User


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_date')
    list_filter = ("status", 'created_date')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}



admin.site.register(Category)
admin.site.register(Post, PostAdmin)
