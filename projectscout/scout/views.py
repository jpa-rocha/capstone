from django.contrib import auth
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import MiscStats, League, Player, PlayingTime, SalaryStats, ShootingStats, Team, AerialDuels, PossessionStats, PassingStats, PassTypesStats, DefensiveStats, GoalShotCreationStats, GoalkeepingStats, TeamStats
from .dataloader import genteamstats_mgmt, salary_mgmt, team_mgmt, player_mgmt, time_mgmt, miscstats_mgmt, aerialstats_mgmt, shootingstats_mgmt, possessionstats_mgmt, passingstats_mgmt, passtypesstats_mgmt, defensivestats_mgmt, goalshotcreationstats_mgmt, goalkeepingstats_mgmt
import pandas as pd
import numpy as np
import csv
import json
from itertools import chain


# Create your views here.
def index(request):
    teams = Team.objects.all()
    teams = teams.order_by('league').all()
    leagues = League.objects.all()
    return render(request, "scout/index.html",{
        'teams' : teams,
        'leagues' : leagues
    })

def player(request, player_id):
    playerobj = Player.objects.get(id=player_id)


    return render(request, "scout/player.html", {
        'player' : playerobj
    })

def team(request, team_name):
    team = Team.objects.get(name=team_name)
    league = League.objects.get(name=team.league)
    teamstats = TeamStats.objects.get(team = team)
    players = Player.objects.filter(team = team)
    salaryinfo = SalaryStats.objects.filter(player__in=players)
    
    # Salary information for selected team
    startersalary = []
    reservesalary = []
    for player in salaryinfo:
        if player.status == 'Starter':
            startersalary.append(player.weeklysalary)
        elif player.status == 'Reserve':
             reservesalary.append(player.weeklysalary)

    startersalary = round(sum(startersalary),2)
    reservesalary = round(sum(reservesalary),2)

    totalsalary = startersalary + reservesalary

    # Salary information for the league
    totalstartersalaries = []
    totalreservesalaries = []
    leagueteams = Team.objects.filter(league=league)
    leagueplayers = Player.objects.filter(team__in = leagueteams)
    leaguesalaries = SalaryStats.objects.filter(player__in=leagueplayers)
    for team in leagueteams:
        teamstartersalary = []
        teamreservesalary = []
        teamplayers = leagueplayers.filter(team = team)
        teamsalaries = leaguesalaries.filter(player__in=teamplayers)
        for player in teamsalaries:
            if player.status == 'Starter':
                teamstartersalary.append(player.weeklysalary)
            elif player.status == 'Reserve':
                teamreservesalary.append(player.weeklysalary)
        teamstartersalary = sum(teamstartersalary)
        teamreservesalary = sum(teamreservesalary)

        totalstartersalaries.append(teamstartersalary)
        totalreservesalaries.append(teamreservesalary)

    
    # Starting salaries
    maxstartersalary = round(max(totalstartersalaries),2)
    minstartersalary = round(min(totalstartersalaries),2)
    medianstartersalary = round(np.percentile(totalstartersalaries,50),2)
    percentile25startersalary = round(np.percentile(totalstartersalaries,25),2)
    percentile75startersalary = round(np.percentile(totalstartersalaries,75),2)

    # Reserve salaries
    maxreservesalary = round(max(totalreservesalaries),2)
    minreservesalary = round(min(totalreservesalaries),2)
    medianreservesalary = round(np.percentile(totalreservesalaries,50),2)
    percentile25reservesalary = round(np.percentile(totalreservesalaries,25),2)
    percentile75reservesalary = round(np.percentile(totalreservesalaries,75),2)

    # Total salaries
    maxtotalsalary = maxstartersalary + maxreservesalary
    mintotalsalary = minstartersalary + minreservesalary
    mediantotalsalary = medianstartersalary + medianreservesalary
    percentile25totalsalary = percentile25startersalary + percentile25reservesalary
    percentile75totalsalary = percentile75startersalary + percentile25reservesalary


    
    return render(request, "scout/team.html", {
        'team' : team_name,
        'teamstats' : teamstats,
        'startersalary' : startersalary,
        'reservesalary' : reservesalary,
        'totalsalary' : totalsalary,
        'maxstartersalary' : maxstartersalary,
        'maxreservesalary' : maxreservesalary,
        'maxtotalsalary' : maxtotalsalary,
        'medianstartersalary' : medianstartersalary,
        'medianreservesalary' : medianreservesalary,
        'mediantotalsalary' : mediantotalsalary,
        'minstartersalary' : minstartersalary,
        'minreservesalary' : minreservesalary,
        'mintotalsalary' : mintotalsalary,
        'percentile25totalsalary' : percentile25totalsalary,
        'percentile25startersalary' : percentile25startersalary,
        'percentile25reservesalary' : percentile25reservesalary,
        'percentile75reservesalary' : percentile75reservesalary,
        'percentile75startersalary' : percentile75startersalary,
        'percentile75totalsalary' : percentile75totalsalary,


    })

def league(request, league_name):
    league = League.objects.get(name=league_name)
    teams = Team.objects.filter(league=league.id)
    return render(request, "scout/league.html", {
        'teams' : teams
    })


def upload_files(request):
    if request.method == 'POST':

        # Directs TEAM updates to the appropriate manager
        if request.POST.get('teams'):
            try:
                if request.FILES['teams'].name == 'teams.csv':
                    if team_mgmt(request) == 'Y':
                        return HttpResponse(status=204)
                    else: 
                        return HttpResponse(status=500)
                else:
                    return render(request, 'scout/upload.html', {
                        'errorteam' : 'You tried to upload the wrong file.'
                    })
            except:
                return render(request, 'scout/upload.html', {
                        'errorteam' : 'You did not upload a file.'
                    })

        # Directs PLAYER updates to the appropriate manager
        elif request.POST.get('players'):
            try:
                if request.FILES['players'].name == 'players.csv':
                    if player_mgmt(request) == 'Y':
                        return HttpResponse(status=204)
                    else: 
                        return HttpResponse(status=500)
                else:
                    return render(request, 'scout/upload.html', {
                        'errorplayer' : 'You tried to upload the wrong file.'
                    })
            except:
                return render(request, 'scout/upload.html', {
                        'errorplayer' : 'You did not upload a file.'
                    })

        # Directs TIME updates to the appropriate manager
        elif request.POST.get('time'):
            try:
                if request.FILES['time'].name == 'time.csv':
                    if time_mgmt(request) == 'Y':
                        return HttpResponse(status=204)
                    else: 
                        return HttpResponse(status=500)
                else:
                    return render(request, 'scout/upload.html', {
                        'errortime' : 'You tried to upload the wrong file.'
                    })
            except:
                return render(request, 'scout/upload.html', {
                        'errortime' : 'You did not upload a file.'
                    })

        # Directs MISC STATS updates to the appropriate manager
        elif request.POST.get('misc'):
            try:
                if request.FILES['misc'].name == 'miscstats.csv':
                    if miscstats_mgmt(request) == 'Y':
                        return HttpResponse(status=204)
                    else: 
                        return HttpResponse(status=500)
                else:
                    return render(request, 'scout/upload.html', {
                        'errorgeneral' : 'You tried to upload the wrong file.'
                    })
            except:
                return render(request, 'scout/upload.html', {
                        'errormisc' : 'You tried to upload the wrong file.'
                    })

        # Directs AERIAL STATS updates to the appropriate manager
        elif request.POST.get('aerial'):
            try:
                if request.FILES['aerial'].name == 'aerialstats.csv':
                    if aerialstats_mgmt(request) == 'Y':
                        return HttpResponse(status=204)
                    else: 
                        return HttpResponse(status=500)
                else:
                    return render(request, 'scout/upload.html', {
                        'erroraerial' : 'You tried to upload the wrong file.'
                    })
            except:
                 return render(request, 'scout/upload.html', {
                        'erroraerial' : 'You tried to upload the wrong file.'
                    })

        # Directs SHOOTING STATS updates to the appropriate manager
        elif request.POST.get('shooting'):
            try:
                if request.FILES['shooting'].name == 'shootingstats.csv':
                    if shootingstats_mgmt(request) == 'Y':
                        return HttpResponse(status=204)
                    else: 
                        return HttpResponse(status=500)
                else:
                    return render(request, 'scout/upload.html', {
                        'errorshooting' : 'You tried to upload the wrong file.'
                    })
            except:
                 return render(request, 'scout/upload.html', {
                        'errorshooting' : 'You tried to upload the wrong file.'
                    })

        # Directs POSSESSION STATS updates to the appropriate manager
        elif request.POST.get('possession'):
            try:
                if request.FILES['possession'].name == 'possessionstats.csv':
                    if possessionstats_mgmt(request) == 'Y':
                        return HttpResponse(status=204)
                    else: 
                        return HttpResponse(status=500)
                else:
                    return render(request, 'scout/upload.html', {
                        'errorpossession' : 'You tried to upload the wrong file.'
                    })
            except:
                 return render(request, 'scout/upload.html', {
                        'errorpossession' : 'You tried to upload the wrong file.'
                    })
        # Directs PASSING STATS updates to the appropriate manager
        elif request.POST.get('passing'):
            try:
                if request.FILES['passing'].name == 'passingstats.csv':
                    if passingstats_mgmt(request) == 'Y':
                        return HttpResponse(status=204)
                    else: 
                        return HttpResponse(status=500)
                else:
                    return render(request, 'scout/upload.html', {
                        'errorpassing' : 'You tried to upload the wrong file.'
                    })
            except:
                 return render(request, 'scout/upload.html', {
                        'errorpassing' : 'You tried to upload the wrong file.'
                    })

        # Directs PASS TYPES STATS updates to the appropriate manager
        elif request.POST.get('passtypes'):
            try:
                if request.FILES['passtypes'].name == 'passtypesstats.csv':
                    if passtypesstats_mgmt(request) == 'Y':
                        return HttpResponse(status=204)
                    else: 
                        return HttpResponse(status=500)
                else:
                    return render(request, 'scout/upload.html', {
                        'errorpasstypes' : 'You tried to upload the wrong file.'
                    })
            except:
                 return render(request, 'scout/upload.html', {
                        'errorpasstypes' : 'You tried to upload the wrong file.'
                    })

        # Directs DEFENSIVE STATS updates to the appropriate manager
        elif request.POST.get('defensive'):
            try:
                if request.FILES['defensive'].name == 'defensivestats.csv':
                    if defensivestats_mgmt(request) == 'Y':
                        return HttpResponse(status=204)
                    else: 
                        return HttpResponse(status=500)
                else:
                    return render(request, 'scout/upload.html', {
                        'errordefensive' : 'You tried to upload the wrong file.'
                    })
            except:
                 return render(request, 'scout/upload.html', {
                        'errordefensive' : 'You tried to upload the wrong file.'
                    })

        # Directs GOAL/SHOT CREATING STATS updates to the appropriate manager
        elif request.POST.get('goalshotcreation'):
            try:
                if request.FILES['goalshotcreation'].name == 'goalshotcreationstats.csv':
                    if goalshotcreationstats_mgmt(request) == 'Y':
                        return HttpResponse(status=204)
                    else: 
                        return HttpResponse(status=500)
                else:
                    return render(request, 'scout/upload.html', {
                        'errorgoalshotcreation' : 'You tried to upload the wrong file.'
                    })
            except:
                 return render(request, 'scout/upload.html', {
                        'errorgoalshotcreation' : 'You tried to upload the wrong file.'
                    })

        # Directs GOALKEEPING STATS updates to the appropriate manager
        elif request.POST.get('goalkeeping'):
            try:
                if request.FILES['goalkeeping'].name == 'fullgoalkeepingstats.csv':
                    if goalkeepingstats_mgmt(request) == 'Y':
                        return HttpResponse(status=204)
                    else: 
                        return HttpResponse(status=500)
                else:
                    return render(request, 'scout/upload.html', {
                        'errorgoalkeeping' : 'You tried to upload the wrong file.'
                    })
            except:
                 return render(request, 'scout/upload.html', {
                        'errorgoalkeeping' : 'You tried to upload the wrong file.'
                    })       

        # Directs SALARY STATS updates to the appropriate manager
        elif request.POST.get('salary'):
            try:
                if request.FILES['salary'].name == 'fixedcontractinfo.json':
                    
                    if salary_mgmt(request) == 'Y':
                        return HttpResponse(status=204)
                    else: 
                        return HttpResponse(status=500)
                else:
                    return render(request, 'scout/upload.html', {
                        'errorsalary' : 'You tried to upload the wrong file.'
                    })
            except:
                return render(request, 'scout/upload.html', {
                        'errorsalary' : 'You tried to upload the wrong file.'
                    }) 
        
        # Directs GENERAL TEAM STATS updates to the appropriate manager
        elif request.POST.get('genteamstats'):
            try:
                if request.FILES['genteamstats'].name == 'cleanleaguestats.csv':
                    
                    if genteamstats_mgmt(request) == 'Y':
                        return HttpResponse(status=204)
                    else: 
                        return HttpResponse(status=500)
                else:
                    return render(request, 'scout/upload.html', {
                        'errorgenteamstats' : 'You tried to upload the wrong file.'
                    })
            except:
                return render(request, 'scout/upload.html', {
                        'errorgenteamstats' : 'You tried to upload the wrong file.'
                    })                                                                                                                                     
    else:
        return render(request, 'scout/upload.html')

def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'scout/login.html', {
                'message': 'Invalid username and/or password.'
            })
    else:
        return render(request, 'scout/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'scout/register.html', {
                'message': 'Passwords must match.'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'scout/register.html', {
                'message': 'Username already taken.'
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'scout/register.html')

# APIs
# teams
def teamapi(request, team_name):
    team = Team.objects.get(name=team_name)
    players = Player.objects.filter(team_id=team.id)
    misc = MiscStats.objects.filter(player__in = players)
    aerial = AerialDuels.objects.filter(player__in = players)
    shooting = ShootingStats.objects.filter(player__in = players)
    possession = PossessionStats.objects.filter(player__in = players)
    passing = PassingStats.objects.filter(player__in = players)
    passtypes = PassTypesStats.objects.filter(player__in = players)
    defensive = DefensiveStats.objects.filter(player__in = players)
    gsc = GoalShotCreationStats.objects.filter(player__in = players)
    goalkeeping = GoalkeepingStats.objects.filter(player__in = players)
    salaries = SalaryStats.objects.filter(player__in = players)
    teamreport = chain(players, misc, aerial, shooting, possession, passing, passtypes, defensive, gsc, goalkeeping, salaries)

    return JsonResponse([player.serialize() for player in teamreport], safe=False)


#players = Player.objects.prefetch_related('playingtime',
#                                              'misc',
 #                                             'aerial',
  #                                            'shooting',
   #                                           'possession',
    #                                          'passing',
     #                                         'passtypes',
      #                                        'defensive',
       #                                       'gsc',
        #                                      'goalkeeping',
         #                                     'salaries').filter(team_id=team.id)