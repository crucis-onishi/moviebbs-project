from django import forms
from .models import Comment

class SearchForm(forms.Form):
        keyword = forms.CharField(label='検索', max_length=100)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
