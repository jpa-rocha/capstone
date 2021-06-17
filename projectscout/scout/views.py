from django.contrib import auth
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.forms.widgets import Textarea
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.files import File
from django.shortcuts import render
from django.urls import reverse
from .models import ExpectedGeneralStats, ExpectedGeneralStatsPer90, GeneralStats, GeneralStatsPer90, League, Player, PlayingTime, Team, DataStorage
import csv
import json


# Create your views here.
def index(request):
    return render(request, "scout/index.html")


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

        # Directs GENERAL STATS updates to the appropriate manager
        elif request.POST.get('general'):
            try:
                if request.FILES['general'].name == 'generalstats.csv':
                    if genstats_mgmt(request) == 'Y':
                        return HttpResponse(status=204)
                    else: 
                        return HttpResponse(status=500)
                else:
                    return render(request, 'scout/upload.html', {
                        'errorgeneral' : 'You tried to upload the wrong file.'
                    })
            except:
                return render(request, 'scout/upload.html', {
                        'errorgeneral' : 'You tried to upload the wrong file.'
                    })

        # Directs EXPECTED GENERAL STATS updates to the appropriate manager
        elif request.POST.get('exgen'):
            try:
                if request.FILES['exgen'].name == 'expectedgeneralstats.csv':
                    if exgenstats_mgmt(request) == 'Y':
                        return HttpResponse(status=204)
                    else: 
                        return HttpResponse(status=500)
                else:
                    return render(request, 'scout/upload.html', {
                        'errorexgen' : 'You tried to upload the wrong file.'
                    })
            except:
                 return render(request, 'scout/upload.html', {
                        'errorexgen' : 'You tried to upload the wrong file.'
                    })


        elif request.POST.get('generalper90'):
            try:
                if request.FILES['generalper90'].name == 'generalstatsper90.csv':
                    if genstatsper90_mgmt(request) == 'Y':
                        return HttpResponse(status=204)
                    else: 
                        return HttpResponse(status=500)
                else:
                    return render(request, 'scout/upload.html', {
                        'errorgeneralper90' : 'You tried to upload the wrong file.'
                    })
            except:
                return render(request, 'scout/upload.html', {
                        'errorgeneralper90' : 'You tried to upload the wrong file.'
                    }) 

        elif request.POST.get('exgenper90'):
            try:
                if request.FILES['exgenper90'].name == 'expectedgeneralstatsper90.csv':
                    if exgenstatsper90_mgmt(request) == 'Y':
                        return HttpResponse(status=204)
                    else: 
                        return HttpResponse(status=500)
                else:
                    return render(request, 'scout/upload.html', {
                        'errorexgenper90' : 'You tried to upload the wrong file.'
                    })
            except:
                 return render(request, 'scout/upload.html', {
                        'errorexgenper90' : 'You tried to upload the wrong file.'
                    })      
    else:
        return render(request, 'scout/upload.html')


def team_mgmt(request):
    if request.method == 'POST':
        try:
            teamsfile = request.FILES['teams'].read().decode('UTF-8').splitlines()
            # Ready CSV
            teams = csv.reader(teamsfile)
            teamlist =[]
            for team in teams:
                teamlist.append(team)
            teamlist = teamlist[1:]
            for entry in teamlist:
                entry[1] = entry[1].split()
                del entry[1][0]
                entry[1] = ' '.join(entry[1])
                
            # Create team info in DB with corresponding league
            for team in teamlist:
                league = League.objects.get(name = team[1])
                teamcheck = Team.objects.get(name = team[0], league=league)
                if teamcheck:
                    pass
                else:
                    newteam = Team.objects.create(name = team[0], league=league)
                    newteam.save()      
            result = 'Y'
            return result
        except:
            result = 'N'
            return result


def player_mgmt(request):
    print('getting here')
    if request.method == 'POST':
        try:
            playerfile = request.FILES['players'].read().decode('UTF-8').splitlines()
            # Ready CSV
            players = csv.reader(playerfile)
            playerlist = []
            for player in players:
                playerlist.append(player)
            playerlist = playerlist[1:]
            for player in playerlist:
                player[0] = player[0].split('\\')
                player[0] = player[0][0]
                print(player[0])
                if len(player[2])>2:
                    player[2] = player[2][:2] + '/' + player[2][2:]
                player[4] = float(player[4])
                player[4] = int(player[4])
                
            # Create players into the DB
            for player in playerlist:
                team = Team.objects.get(name = player[3])
                playercheck = Player.objects.filter(name = player[0], team=team)
                if playercheck.exists():
                    pass
                else:
                    newplayer = Player.objects.create(name = player[0], country = player[1], position = player[2], team=team, yearborn = player[4])
                    newplayer.save()      
            
            result = 'Y'
            return result
        except:
            result = 'N'
            return result

            

def time_mgmt(request):
    if request.method == 'POST':
        try:
            timefile = request.FILES['time'].read().decode('UTF-8').splitlines()
            # Ready CSV
            time = csv.reader(timefile)
            timelist = []
            for entry in time:
                timelist.append(entry)
            timelist = timelist[2:]

            # Enter time stats into DB
            for entry in timelist:
                player = Player.objects.get(id = entry[0])
                statcheck = PlayingTime.objects.filter(player = player.id)
                if statcheck.exists():
                    pass
                else:
                    newstat = PlayingTime.objects.create(player=player, matchesplayed = entry[1], starts = entry[2],
                                                        minutes = entry[3], minutesper90 = entry[4])
                    newstat.save()
            result = 'Y'
            return result

        except:
            result = 'N'
            return result

            

def genstats_mgmt(request):
     if request.method == 'POST':
        try:
            genstatsfile = request.FILES['general'].read().decode('UTF-8').splitlines()
            # Ready CSV
            genstats = csv.reader(genstatsfile)
            genstatslist = []
            for entry in genstats:
                genstatslist.append(entry)
            genstatslist = genstatslist[2:]
            # List wasn't looping properly into DB, had to make diferent list based on original range for each iteration
            rangestats = range(len(genstatslist))
            for i in rangestats:
                genstatslist = genstatslist[i:]
                for entry in genstatslist:
                    player = Player.objects.get(id = entry[0])
                    statcheck = GeneralStats.objects.filter(player = player.id)
                    if statcheck.exists():
                        pass
                    else:
                        newstat = GeneralStats.objects.create(player=player, goals = entry[1], assists = entry[2],
                                                            nonPKgoals = entry[3], PKgoals = entry[4], attemptedPK = entry[5],
                                                            yellowcards = entry[6], redcards = entry[7])
                        newstat.save()
                
            result = 'Y'
            return result

        except:
            result = 'N'
            return result
            

def exgenstats_mgmt(request):
    if request.method == 'POST':
        try:
            exgenstatsfile = request.FILES['exgen'].read().decode('UTF-8').splitlines()
            # Ready CSV
            exgenstats = csv.reader(exgenstatsfile)
            exgenstatslist = []
            for entry in exgenstats:
                exgenstatslist.append(entry)
            exgenstatslist = exgenstatslist[2:]
            # List wasn't looping properly into DB, had to make diferent list based on original range for each iteration
            rangestats = range(len(exgenstatslist))
            for i in rangestats:
                exgenstatslist = exgenstatslist[i:]
                for entry in exgenstatslist:
                    player = Player.objects.get(id = entry[0])
                    statcheck = ExpectedGeneralStats.objects.filter(player = player.id)
                    if statcheck.exists():
                        pass
                    else:
                        if entry[1] =='':
                            entry[1] = 0
                        if entry[2] =='':
                            entry[2] = 0
                        if entry[3] =='':
                            entry[3] = 0
                        if entry[4] =='':
                            entry[4] = 0
                        newstat = ExpectedGeneralStats.objects.create(player=player, expectedgoals = entry[1], nonPKexpectedgoals = entry[2],
                                                            expectedassists = entry[3], exnonPKgoalsandassists = entry[4])
                        newstat.save()
                
            result = 'Y'
            return result

        except:
            result = 'N'
            return result

def genstatsper90_mgmt(request):
    if request.method == 'POST':
        try:
            genstatsper90file = request.FILES['generalper90'].read().decode('UTF-8').splitlines()
            # Ready CSV
            genstatsper90 = csv.reader(genstatsper90file)
            genstatsper90list = []
            for entry in genstatsper90:
                genstatsper90list.append(entry)
            genstatsper90list = genstatsper90list[2:]
            # List wasn't looping properly into DB, had to make diferent list based on original range for each iteration
            rangestats = range(len(genstatsper90list))
            for i in rangestats:
                genstatsper90list = genstatsper90list[i:]
                for entry in genstatsper90list:
                    player = Player.objects.get(id = entry[0])
                    statcheck = GeneralStatsPer90.objects.filter(player = player.id)
                    if statcheck.exists():
                        pass
                    else:
                        if entry[1] =='':
                            entry[1] = 0
                        if entry[2] =='':
                            entry[2] = 0
                        if entry[3] =='':
                            entry[3] = 0
                        if entry[4] =='':
                            entry[4] = 0
                        if entry[5] =='':
                            entry[5] = 0
                        newstat = GeneralStatsPer90.objects.create(player=player, goals = entry[1], assists = entry[2],
                                                            goalsplusassists = entry[3], nonPKgoals = entry[4], nonPKgoalsplusassists = entry[5])
                        newstat.save()
                
            result = 'Y'
            return result

        except:
            result = 'N'
            return result

def exgenstatsper90_mgmt(request):
    if request.method == 'POST':
        try:
            exgenstatsper90file = request.FILES['exgenper90'].read().decode('UTF-8').splitlines()
            # Ready CSV
            exgenstatsper90 = csv.reader(exgenstatsper90file)
            exgenstatsper90list = []
            for entry in exgenstatsper90:
                exgenstatsper90list.append(entry)
            exgenstatsper90list = exgenstatsper90list[2:]
            # List wasn't looping properly into DB, had to make diferent list based on original range for each iteration
            rangestats = range(len(exgenstatsper90list))
            for i in rangestats:
                exgenstatsper90list = exgenstatsper90list[i:]
                for entry in exgenstatsper90list:
                    player = Player.objects.get(id = entry[0])
                    statcheck = ExpectedGeneralStatsPer90.objects.filter(player = player.id)
                    if statcheck.exists():
                        pass
                    else:
                        if entry[1] =='':
                            entry[1] = 0
                        if entry[2] =='':
                            entry[2] = 0
                        if entry[3] =='':
                            entry[3] = 0
                        if entry[4] =='':
                            entry[4] = 0
                        if entry[5] =='':
                            entry[5] = 0
                        newstat = ExpectedGeneralStatsPer90.objects.create(player=player, exgoals = entry[1], exassists = entry[2],
                                                            exgoalsplusassists = entry[3], exnonPKgoals = entry[4], exnonPKgoalsplusassists = entry[5])
                        newstat.save()
                
            result = 'Y'
            return result

        except:
            result = 'N'
            return result


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