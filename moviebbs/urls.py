from django.urls import path
from . import views
from django.urls import path, include
from django.views.generic import TemplateView

app_name = 'moviebbs'

urlpatterns = [
    # path('test/', views.sample_view, name='sample_view'),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('category/<str:category_name>/', views.CategoryView.as_view(), name='category'),
    path('parent-category/<str:category_parent>/', views.ParentView.as_view(), name='parent_category'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('api/category/get/', views.ajax_get_category, name='ajax_get_category'),
    path('comment/<int:pk>/', views.CommentView.as_view(), name='comment'),
    path('<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
    path('youtube_search/', views.YoutubeSearchView.as_view(), name='youtube_search'),
    path('dear_creator/', TemplateView.as_view(template_name="moviebbs/dear_creator.html"), name='dear_creator'),
    path('google5173443084b9a048.html/', views.google_search_console, name='google_search_console'),
]
