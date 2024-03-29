from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .models import ParentCategory, Category, Article, Comment # モデル
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SearchForm, CreateForm
from django.core.paginator import Paginator

from django.http import JsonResponse
from django.http import HttpResponse

from django.views.generic import View
from . import get_data_api
import json

from django.db import models
from django.db.models import F, Max
from django.db.models.functions import Coalesce

from .forms import CreateForm, CommentForm

import logging

logger = logging.getLogger(__name__) # 現在のモジュールのロガーを取得

# def sample_view(request):
#     try:
#         # ここでエラーが発生する可能性のあるコードを記述します
#         result = 1 / 0  # 例として ZeroDivisionError を発生させるコード
#     except ZeroDivisionError as e:
#         logger.error(f"エラーが発生しました: {e}")
#         return HttpResponse("エラーが発生しました")

class IndexView(generic.ListView):
    model = Article
    template_name = 'moviebbs/index.html'
    paginate_by = 10  # 1ページあたりの表示数

    def get_queryset(self):
        queryset = super().get_queryset()

        # 最新のコメントのcreated_atまたはArticleのcreated_atで降順に並び替え
        queryset = queryset.annotate(
            latest_activity=Coalesce(
                Max(F('comments__created_at'), output_field=models.DateTimeField()),
                F('created_at')
            )
        ).order_by('-latest_activity')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ページネーション用のコンテキストデータ
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

class CategoryView(generic.ListView):
    model = Article
    template_name = 'moviebbs/category.html'
    paginate_by = 10  # 1ページあたりの表示数

    def get_queryset(self):
        # カテゴリーのスラッグに対応する記事をフィルタリング
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        queryset = Article.objects.filter(category=category)

        # 最新のコメントのcreated_atまたはArticleのcreated_atで降順に並び替え
        queryset = queryset.annotate(
            latest_activity=Coalesce(
                Max(F('comments__created_at'), output_field=models.DateTimeField()),
                F('created_at')
            )
        ).order_by('-latest_activity')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # フィルタリングしたカテゴリーオブジェクト
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        context['category'] = category

        # ページネーション用のコンテキストデータ
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

class ParentView(generic.ListView):
    model = Article
    template_name = 'moviebbs/parent_category.html'
    paginate_by = 10  # 1ページあたりの表示数

    def get_queryset(self):
        # 親カテゴリのスラッグに対応するカテゴリをフィルタリング
        parent_category = get_object_or_404(ParentCategory, slug=self.kwargs['parent_category_slug'])
        queryset = Article.objects.filter(category__parent=parent_category)

        # 最新のコメントのcreated_atまたはArticleのcreated_atで降順に並び替え
        queryset = queryset.annotate(
            latest_activity=Coalesce(
                Max(F('comments__created_at'), output_field=models.DateTimeField()),
                F('created_at')
            )
        ).order_by('-latest_activity')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # フィルタリングした親カテゴリオブジェクト
        parent_category = get_object_or_404(ParentCategory, slug=self.kwargs['parent_category_slug'])
        context['parent_category'] = parent_category

        # ページネーション用のコンテキストデータ
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
        movie_platform = self.object.movie_platform
        movie_meta = get_data_api.get_movie_meta(movie_id, movie_platform)

        context['movie_title'] = movie_meta['movie_title']
        context['channel_title'] = movie_meta['channel_title']
        context['movie_description'] = movie_meta['movie_description']

        # コメントフォーム
        context['comment_form'] = CommentForm

        # コメントオブジェクト
        comments = self.object.comments.all()
        context['comments'] = comments

        return context

class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Article
    form_class = CreateForm
    success_url = reverse_lazy('moviebbs:index')
    template_name = 'moviebbs/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 新規投稿フォーム
        context['create_form'] = CreateForm
        return context

    def form_valid(self, create_form):
        create_form.instance.user = self.request.user
        movie_url = create_form.cleaned_data["movie_url"]
        movie_platform = get_data_api.get_movie_platform(movie_url)

        # 動画IDの取得
        movie_id = get_data_api.get_movie_id(movie_url)

        create_form.instance.movie_id = movie_id
        create_form.instance.movie_platform = movie_platform

        return super().form_valid(create_form)


def ajax_get_category(request):
    pk = request.GET.get('pk')
    # pkパラメータがない、もしくはpk=空文字列だった場合は全カテゴリを返す
    if not pk:
        category_list = Category.objects.all()

    # pkがあれば、そのpkでカテゴリを絞り込む
    else:
        category_list = Category.objects.filter(parent__pk=pk)

    # [ {'name': 'サッカー', 'pk': '3'}, {...}, {...} ] という感じのリストになる
    category_list = [{'pk': category.pk, 'name': category.name} for category in category_list]

    # JSONで返す
    return JsonResponse({'categoryList': category_list})


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
        keyword = request.GET.get('word', '') or 'ゆっくり村' # デフォルト値として「ゆっくり村」を設定
        youtube_df = get_data_api.youtube_search(keyword)
        json_record = youtube_df.reset_index().to_json(orient='records')
        data = []
        data = json.loads(json_record)

        context = {
                "word":keyword,
                'data':data,
        }
        return  render(request, 'moviebbs/result.html', context)

def google_search_console(request):
    return render(request, 'google/google5173443084b9a048.html')
