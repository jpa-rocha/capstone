from collections import OrderedDict
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import MiscStats, League, Player, PlayingTime, SalaryStats, ShootingStats, Team, AerialDuels, PossessionStats, PassingStats, PassTypesStats, DefensiveStats, GoalShotCreationStats, GoalkeepingStats, TeamStats
from .dataloader import genteamstats_mgmt, salary_mgmt, team_mgmt, player_mgmt, time_mgmt, miscstats_mgmt, aerialstats_mgmt, shootingstats_mgmt, possessionstats_mgmt, passingstats_mgmt, passtypesstats_mgmt, defensivestats_mgmt, goalshotcreationstats_mgmt, goalkeepingstats_mgmt
import numpy as np
import pandas as pd
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
    teamstats = TeamStats.objects.get(team = team)
    players = Player.objects.filter(team = team)
    salaryinfo = SalaryStats.objects.filter(player__in=players)
    leagues = League.objects.all()

    # Salary information for selected team
    startersalary =[]
    reservesalary =[]
    for player in salaryinfo:
        if player.status == 'Starter':
            startersalary.append(player.weeklysalary)           
        elif player.status == 'Reserve':
            reservesalary.append(player.weeklysalary)
   
    startersalary = round(sum(startersalary),2)
    reservesalary = round(sum(reservesalary),2)
    totalsalary = startersalary + reservesalary

    return render(request, "scout/team.html", {
        'team' : team_name,
        'teamstats' : teamstats,
        'startersalary' : startersalary,
        'reservesalary' : reservesalary,
        'totalsalary' : totalsalary,
        'leagues' : leagues
    })

def league(request, league_name):
    league = League.objects.get(name=league_name)
    teams = Team.objects.filter(league=league.id)
    teams = teams.order_by('name').all()
    leagues = League.objects.all()
    return render(request, "scout/league.html", {
        'teams' : teams,
        'leagues' : leagues
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
# Calls db and collects some player information

#Calls db and collects player salary information, does the math to identify certain percentiles and the average
def salaryoverviewapi(request, lORt_name):
        dicttotalstartersalaries = {}
        dicttotalreservesalaries = {}
        dicttotalsalaries = {}
        userteam = Team.objects.get(name = lORt_name)
        league = userteam.league
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

            dicttotalstartersalaries[team.name] = sum(teamstartersalary)
            dicttotalreservesalaries[team.name] = sum(teamreservesalary)
            dicttotalsalaries[team.name] = round(sum(teamstartersalary)) + round(sum(teamreservesalary))

        orderedstartersalaries = sorted(dicttotalstartersalaries.items(), key=lambda x: x[1])
        startersalarieslist = []
        for entry in orderedstartersalaries:
            startersalarieslist.append(entry[1])

        orderedreservesalaries = sorted(dicttotalreservesalaries.items(), key=lambda x: x[1])
        reservesalarieslist = []
        for entry in orderedreservesalaries:
            reservesalarieslist.append(entry[1])

        orderedtotalsalaries = sorted(dicttotalsalaries.items(), key=lambda x: x[1])
        totalsalarieslist = []
        for entry in orderedtotalsalaries:
            totalsalarieslist.append(entry[1])
        
        startersalaryoverview = {}
        startersalaryoverview['Lowest'] = float(round(np.min(startersalarieslist),2))
        startersalaryoverview['25th Percentile'] = float(round(np.percentile(startersalarieslist, 25)))
        startersalaryoverview['Median'] = float(round(np.percentile(startersalarieslist, 50)))
        startersalaryoverview['75th Percentile'] = float(round(np.percentile(startersalarieslist, 75)))
        startersalaryoverview['Highest'] = float(round(np.max(startersalarieslist),2))
        startersalaryoverview[f'{lORt_name}'] = float(round(dicttotalstartersalaries[f'{lORt_name}'],2))
        startersalaryoverview = sorted(startersalaryoverview.items(), key=lambda x: x[1])

        reservesalaryoverview = {}
        reservesalaryoverview['Lowest'] = float(round(np.min(reservesalarieslist),2))
        reservesalaryoverview['25th Percentile'] = float(round(np.percentile(reservesalarieslist, 25)))
        reservesalaryoverview['Median'] = float(round(np.percentile(reservesalarieslist, 50)))
        reservesalaryoverview['75th Percentile'] = float(round(np.percentile(reservesalarieslist, 75)))
        reservesalaryoverview['Highest'] = float(round(np.max(reservesalarieslist),2))
        reservesalaryoverview[f'{lORt_name}'] = float(round(dicttotalreservesalaries[f'{lORt_name}'],2))
        reservesalaryoverview = sorted(reservesalaryoverview.items(), key=lambda x: x[1])

        totalsalaryoverview = {}
        totalsalaryoverview['Lowest'] = float(round(np.min(totalsalarieslist),2))
        totalsalaryoverview['25th Percentile'] = float(round(np.percentile(totalsalarieslist, 25)))
        totalsalaryoverview['Median'] = float(round(np.percentile(totalsalarieslist, 50)))
        totalsalaryoverview['75th Percentile'] = float(round(np.percentile(totalsalarieslist, 75)))
        totalsalaryoverview['Highest'] = float(round(np.max(totalsalarieslist),2))
        totalsalaryoverview[f'{lORt_name}'] = float(round(dicttotalsalaries[f'{lORt_name}'],2))
        totalsalaryoverview = sorted(totalsalaryoverview.items(), key=lambda x: x[1])

        teamsalaryoverview = {}
        teamsalaryoverview['starters'] = startersalaryoverview
        teamsalaryoverview['reserves'] = reservesalaryoverview
        teamsalaryoverview['total'] = totalsalaryoverview
       
        return JsonResponse(teamsalaryoverview, safe=False)
        
    
# Salary information for a single team
def teamsalaryapi(request, team_name):
    team = Team.objects.get(name=team_name)
    players = Player.objects.filter(team_id=team.id)
    salaries = SalaryStats.objects.filter(player__in = players)

    return JsonResponse([player.serialize() for player in salaries], safe=False)

# Salary information for the league
def leaguesalaryapi(request, league_name):
    league = League.objects.get(name=league_name)
    # Salary information for the league
    dicttotalstartersalaries = {}
    dicttotalreservesalaries = {}
    dicttotalsalaries = {}
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

        dicttotalstartersalaries[team.name] = sum(teamstartersalary)
        dicttotalstartersalaries = OrderedDict(sorted(dicttotalstartersalaries.items()))
        dicttotalreservesalaries[team.name] = sum(teamreservesalary)
        dicttotalreservesalaries = OrderedDict(sorted(dicttotalreservesalaries.items()))
        dicttotalsalaries[team.name] = round(sum(teamstartersalary)) + round(sum(teamreservesalary))
        dicttotalsalaries = OrderedDict(sorted(dicttotalsalaries.items()))
    
    leaguesalaries = []
    leaguesalaries.append(dicttotalstartersalaries)
    leaguesalaries.append(dicttotalreservesalaries)
    leaguesalaries.append(dicttotalsalaries)
    return  JsonResponse(leaguesalaries, safe=False)


def totalsalaryapi(request):
    league = League.objects.all()
    # Salary information for the league
    dicttotalstartersalaries = {}
    dicttotalreservesalaries = {}
    dicttotalsalaries = {}
    for league in league:
        leagueteams = Team.objects.filter(league=league)
        leagueplayers = Player.objects.filter(team__in = leagueteams)
        leaguesalaries = SalaryStats.objects.filter(player__in=leagueplayers)
        teamstartersalary = []
        teamreservesalary = []
        for team in leagueteams:
            teamplayers = leagueplayers.filter(team = team)
            teamsalaries = leaguesalaries.filter(player__in=teamplayers)
            for player in teamsalaries:
                if player.status == 'Starter':
                    teamstartersalary.append(player.weeklysalary)
                elif player.status == 'Reserve':
                    teamreservesalary.append(player.weeklysalary)

        dicttotalstartersalaries[league.name] = round(sum(teamstartersalary))
        dicttotalreservesalaries[league.name] = round(sum(teamreservesalary))
        dicttotalsalaries[league.name] = round(sum(teamstartersalary)) + round(sum(teamreservesalary))
        
        leaguesalaries = []
        leaguesalaries.append(dicttotalstartersalaries)
        leaguesalaries.append(dicttotalreservesalaries)
        leaguesalaries.append(dicttotalsalaries)
    return  JsonResponse(leaguesalaries, safe=False)

# Salary and goal inforamtion for all leagues or a single league
def salarygoalsapi(request, div):
    if div == "ALL":
        players = Player.objects.all()
        playersdf = pd.DataFrame(Player.objects.all().values())
        goals = pd.DataFrame(ShootingStats.objects.filter(player__in = players).order_by('-goals').values())
        salaries = pd.DataFrame(list(SalaryStats.objects.filter(player__in = players).values()))
        report = pd.merge(goals, salaries, on='player_id')
        report = report.rename(columns={'player_id': 'id'})
        finalreport = pd.merge(playersdf, report, on='id')
        finalreport = finalreport.sort_values(by=['goals'], ascending=False)
        finalreport = finalreport.set_index('id')
        finalreport = finalreport.head(100)
        finalreport = json.loads(json.dumps(list(finalreport.T.to_dict().values())))
        return JsonResponse(finalreport, safe=False)
    else:
        league = League.objects.get(name=div)
        if league:
            leagueteams = Team.objects.filter(league=league)
            players = Player.objects.filter(team__in = leagueteams)
            playersdf = pd.DataFrame(Player.objects.filter(team__in = leagueteams).values())
            goals = pd.DataFrame(ShootingStats.objects.filter(player__in = players).order_by('-goals').values())
            salaries = pd.DataFrame(list(SalaryStats.objects.filter(player__in = players).values()))
            report = pd.merge(goals, salaries, on='player_id')
            report = report.rename(columns={'player_id': 'id'})
            finalreport = pd.merge(playersdf, report, on='id')
            finalreport = finalreport.sort_values(by=['goals'], ascending=False)
            finalreport = finalreport.set_index('id')
            finalreport = finalreport.head(50)
            finalreport = json.loads(json.dumps(list(finalreport.T.to_dict().values())))
            return JsonResponse(finalreport, safe=False)

# Salary and assists inforamtion for all leagues or a single league
def salaryassistsapi(request, div):
    if div == "ALL":
        players = Player.objects.all()
        playersdf = pd.DataFrame(Player.objects.all().values())
        assists = pd.DataFrame(PassingStats.objects.filter(player__in = players).order_by('-assists').values())
        salaries = pd.DataFrame(list(SalaryStats.objects.filter(player__in = players).values()))
        report = pd.merge(assists, salaries, on='player_id')
        report = report.rename(columns={'player_id': 'id'})
        finalreport = pd.merge(playersdf, report, on='id')
        finalreport = finalreport.sort_values(by=['assists'], ascending=False)
        finalreport = finalreport.set_index('id')
        finalreport = finalreport.head(100)
        finalreport = json.loads(json.dumps(list(finalreport.T.to_dict().values())))
        return JsonResponse(finalreport, safe=False)
    else:
        league = League.objects.get(name=div)
        if league:
            leagueteams = Team.objects.filter(league=league)
            players = Player.objects.filter(team__in = leagueteams)
            playersdf = pd.DataFrame(Player.objects.filter(team__in = leagueteams).values())
            assists = pd.DataFrame(PassingStats.objects.filter(player__in = players).order_by('-assists').values())
            salaries = pd.DataFrame(list(SalaryStats.objects.filter(player__in = players).values()))
            report = pd.merge(assists, salaries, on='player_id')
            report = report.rename(columns={'player_id': 'id'})
            finalreport = pd.merge(playersdf, report, on='id')
            finalreport = finalreport.sort_values(by=['assists'], ascending=False)
            finalreport = finalreport.set_index('id')
            finalreport = finalreport.head(50)
            finalreport = json.loads(json.dumps(list(finalreport.T.to_dict().values())))
            return JsonResponse(finalreport, safe=False)

# Salary and tackles inforamtion for all leagues or a single league
def salarytacklesapi(request, div):
    if div == "ALL":
        players = Player.objects.all()
        playersdf = pd.DataFrame(Player.objects.all().values())
        tackles = pd.DataFrame(DefensiveStats.objects.filter(player__in = players).order_by('-tackles').values())
        salaries = pd.DataFrame(list(SalaryStats.objects.filter(player__in = players).values()))
        report = pd.merge(tackles, salaries, on='player_id')
        report = report.rename(columns={'player_id': 'id'})
        finalreport = pd.merge(playersdf, report, on='id')
        finalreport = finalreport.sort_values(by=['tackles'], ascending=False)
        finalreport = finalreport.set_index('id')
        finalreport = finalreport.head(100)
        finalreport = json.loads(json.dumps(list(finalreport.T.to_dict().values())))
        return JsonResponse(finalreport, safe=False)
    else:
        league = League.objects.get(name=div)
        if league:
            leagueteams = Team.objects.filter(league=league)
            players = Player.objects.filter(team__in = leagueteams)
            playersdf = pd.DataFrame(Player.objects.filter(team__in = leagueteams).values())
            tackles = pd.DataFrame(DefensiveStats.objects.filter(player__in = players).order_by('-tackles').values())
            salaries = pd.DataFrame(list(SalaryStats.objects.filter(player__in = players).values()))
            report = pd.merge(tackles, salaries, on='player_id')
            report = report.rename(columns={'player_id': 'id'})
            finalreport = pd.merge(playersdf, report, on='id')
            finalreport = finalreport.sort_values(by=['tackles'], ascending=False)
            finalreport = finalreport.set_index('id')
            finalreport = finalreport.head(50)
            finalreport = json.loads(json.dumps(list(finalreport.T.to_dict().values())))
            return JsonResponse(finalreport, safe=False)