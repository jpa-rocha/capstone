from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    # DB management urls
    path('team-mgmt', views.team_mgmt, name='team-mgmt'),
    path('player-mgmt', views.player_mgmt, name='player-mgmt'),
    path('time-mgmt', views.time_mgmt, name='time-mgmt'),

    # Login, logout & register
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
]
