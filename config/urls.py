from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.views.generic import TemplateView   # 追加

urlpatterns = [
    path('moviebbs/', include('moviebbs.urls')),
    path('admin/', admin.site.urls),
    path('',  RedirectView.as_view(url='/moviebbs/')),
    path('accounts/', include('allauth.urls')), #追加
]
