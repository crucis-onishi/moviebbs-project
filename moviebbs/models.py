from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class ParentCategory(models.Model):
    name = models.CharField('親カテゴリ名', max_length=255, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField('カテゴリ名', max_length=255, unique=True)
    parent = models.ForeignKey(ParentCategory, verbose_name='親カテゴリ', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True)
    movie_url = models.URLField(max_length=255)
    movie_id = models.CharField(max_length=50)
    movie_platform = models.CharField(max_length=50, default='youtube')
    category = models.ForeignKey(Category, verbose_name='カテゴリ', on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('moviebbs:detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'created_at'
