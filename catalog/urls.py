from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('musics/', views.MusicListView.as_view(), name = 'music'),
    path('musics/<int:num>/', views.MusicDetailView.as_view(), name = 'music_detail'),
    path('my_musics/', views.user_love_song_view.as_view(), name = 'my_musics'),
    path('add_music/', views.music_create, name = 'music-create'),
    path('like_music/<int:num>', views.like_music, name = 'like'),
    path('unlike_music/<int:num>', views.unlike_music, name = 'unlike'),
    path('register/', views.register_view, name='register'),

]
