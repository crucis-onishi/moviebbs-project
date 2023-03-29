from django import forms
from .models import ParentCategory, Article, Comment

class SearchForm(forms.Form):
        keyword = forms.CharField(label='検索', max_length=100)

class CreateForm(forms.ModelForm):
    # 親カテゴリの選択欄を定義
    parent_category = forms.ModelChoiceField(
        label='親カテゴリー選択',
        queryset=ParentCategory.objects,
        required=False
    )
    class Meta:
        model = Article
        fields = ['text', 'movie_url', 'parent_category', 'category']
        labels = {
            'text':'コメント',
            'movie_url':'Youtube動画のURL',
            'parent_category':'親カテゴリー選択',
            'category':'カテゴリー選択',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text':'',
        }
