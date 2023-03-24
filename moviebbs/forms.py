from django import forms
from .models import Article, Comment

class SearchForm(forms.Form):
        keyword = forms.CharField(label='検索', max_length=100)

class CreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('text', 'movie_url', 'category',)
        labels = {
            'text':'この動画について',
            'movie_url':'Youtube動画のURL',
            'category':'カテゴリー選択',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text':'',
        }
