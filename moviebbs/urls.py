from django.urls import path
from . import views
from django.urls import path, include
from django.views.generic import TemplateView

from django.contrib.sitemaps.views import sitemap
from .sitemaps import ArticleSitemap  # サイトマップのクラス

app_name = 'moviebbs'

sitemaps = {
    'articles': ArticleSitemap,
}

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('dear_creator/', TemplateView.as_view(template_name="moviebbs/dear_creator.html"), name='dear_creator'),
    path('google5173443084b9a048.html/', views.google_search_console, name='google_search_console'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('youtube_search/', views.YoutubeSearchView.as_view(), name='youtube_search'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('comment/<int:pk>/', views.CommentView.as_view(), name='comment'),
    path('<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
    path('api/category/get/', views.ajax_get_category, name='ajax_get_category'),
    path('<slug:parent_category_slug>/', views.ParentView.as_view(), name='parent_category'),
    path('<slug:parent_category_slug>/<slug:category_slug>/', views.CategoryView.as_view(), name='category'),
]
