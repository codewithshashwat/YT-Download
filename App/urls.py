# downloader/urls.py
from django.urls import path
from . import views

app_name = 'App'

urlpatterns = [
    path('', views.home, name='home'),
    path('download/', views.download_video, name='download_video'),
    path('download_file/<str:resolution>/<str:video_id>/', views.download_file, name='download_file'),
]