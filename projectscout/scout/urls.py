from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('player/<int:player_id>', views.player, name='player'),
    
    # DB management urls
    path('upload', views.upload_files, name='upload'),
    # Login, logout & register
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
]
