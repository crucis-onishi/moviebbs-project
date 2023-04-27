from django.urls import path
from . import views
from django.urls import path, include

app_name = 'moviebbs'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('category/<str:category_name>/', views.CategoryView.as_view(), name='category'),
    path('parent-category/<str:category_parent>/', views.ParentView.as_view(), name='parent_category'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('api/category/get/', views.ajax_get_category, name='ajax_get_category'),
    path('comment/<int:pk>/', views.CommentView.as_view(), name='comment'),
    path('<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
    path('youtube_search/', views.YoutubeSearchView.as_view(), name='youtube_search'),
]
