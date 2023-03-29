from django.contrib import admin
from .models import ParentCategory, Category, Article, Comment

admin.site.register(ParentCategory)
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Comment)
