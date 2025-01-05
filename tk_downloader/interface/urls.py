from django.urls import path
from interface import views

urlpatterns = [
    path('', views.downloader_tiktok, name='downloader_tiktok'),
]