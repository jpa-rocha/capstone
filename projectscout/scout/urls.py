from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('player/<int:player_id>', views.player, name='player'),
    path('team/<str:team_name>', views.team, name='team'),
    path('league/<str:league_name>', views.league, name='league'),
    
    # DB management urls
    path('upload', views.upload_files, name='upload'),
    # Login, logout & register
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),

    #APIs
    path('teamapi/<str:team_name>', views.teamapi, name='teamapi'),
    path('teamsalaryapi/<str:team_name>', views.teamsalaryapi, name='teamsalaryapi'),
    path('salaryoverviewapi/<str:lORt_name>', views.salaryoverviewapi, name='salaryoverviewapi'),
    path('totalsalaryapi', views.totalsalaryapi, name='totalsalaryapi'),
    path('leaguesalaryapi/<str:league_name>', views.leaguesalaryapi, name='leaguesalaryapi'),
    path('salarygoalsapi/<str:div>', views.salarygoalsapi, name='salarygoalsapi'),
]
