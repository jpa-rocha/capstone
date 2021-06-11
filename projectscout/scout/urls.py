from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('team-mgmt', views.team_mgmt, name='team-mgmt'),
    path('player-mgmt', views.player_mgmt, name='player-mgmt'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
]
