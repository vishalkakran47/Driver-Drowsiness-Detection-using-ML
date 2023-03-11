from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagelogin_show, name='pagelogin_show'),
    path('signup/', views.pageregister_show, name='pageregister_show'),
    path('index/', views.index_show, name='index_show'),
    path('video_feed/',views.video_feed, name='video_feed'),
    path('analytics/',views.analytics, name='analytics'),
]
