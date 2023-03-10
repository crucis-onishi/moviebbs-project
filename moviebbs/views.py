from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .models import Category, Article, Comment # モデル
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SearchForm
from django.core.paginator import Paginator

from django.http import HttpResponse
from django.views.generic import View
from . import get_data_api
import json

from .forms import CommentForm


class IndexView(generic.ListView):
    model = Article
    template_name = 'moviebbs/index.html'
    paginate_by = 10  # 1ページあたりの表示数

    def get_queryset(self):
        queryset = super().get_queryset()
        # このメソッドでクエリセットを加工することができます。
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 10  # ページ番号の表示数
        max_index = len(paginator.page_range)
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        if start_index + page_numbers_range > max_index:
            end_index = max_index
        else:
            end_index = start_index + page_numbers_range

        context['page_numbers'] = paginator.page_range[start_index:end_index]
        return context

class DetailView(generic.DetailView):
    model = Article
    template_name = 'moviebbs/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()

        # 動画のメタ情報
        movie_id = self.object.movie_id
        movie_meta = get_data_api.get_movie_meta(movie_id)

        context['movie_title'] = movie_meta['movie_title']
        context['channeltitle'] = movie_meta['channeltitle']
        # context['movie_player'] = movie_meta['movie_player']

        # コメントフォーム
        context['comment_form'] = CommentForm

        # コメントオブジェクト
        comments = self.object.comments.all()
        context['comments'] = comments

        return context

class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Article
    fields = ['text', 'movie_url', 'category']
    template_name = 'moviebbs/create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.movie_id = get_data_api.get_movie_id(form.cleaned_data['movie_url'])

        return super(CreateView, self).form_valid(form)

class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Article
    success_url = reverse_lazy('moviebbs:index')
    template_name = 'moviebbs/delete.html'

class CommentView(LoginRequiredMixin, generic.edit.CreateView):
    model = Comment
    form_class = CommentForm

    #格納する値をチェック
    def form_valid(self, form):
        form.instance.user = self.request.user
        article_pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)

        comment = form.save(commit=False)
        comment.target = article
        comment.save()

        return redirect('moviebbs:detail', pk=article_pk)

class YoutubeSearchView(View):
    def get(self, request, *args, **kwargs):
        keyword = request.GET['word']
        youtube_df = get_data_api.youtube_search(keyword)
        json_record = youtube_df.reset_index().to_json(orient='records')
        data = []
        data = json.loads(json_record)

        context = {
                "word":keyword,
                'data':data,
        }
        return  render(request, 'moviebbs/result.html', context)
