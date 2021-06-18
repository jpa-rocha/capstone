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
from .models import MiscStats, League, Player, PlayingTime, Team, AerialDuels
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

        # Directs EXPECTED GENERAL STATS updates to the appropriate manager
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
                print(team)
                league = League.objects.get(name = team[1])
                teamcheck = Team.objects.filter(name = team[0], league=league)
                if teamcheck.exists():
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

            

def miscstats_mgmt(request):
     if request.method == 'POST':
        try:
            miscstatsfile = request.FILES['misc'].read().decode('UTF-8').splitlines()
            # Ready CSV
            miscstats = csv.reader(miscstatsfile)
            miscstatslist = []
            for entry in miscstats:
                miscstatslist.append(entry)
            miscstatslist = miscstatslist[2:]
            # List wasn't looping properly into DB, had to make diferent list based on original range for each iteration
            rangestats = range(len(miscstatslist))
            for i in rangestats:
                miscstatslist = miscstatslist[i:]
                for entry in miscstatslist:
                    player = Player.objects.get(id = entry[0])
                    statcheck = MiscStats.objects.filter(player = player.id)
                    if statcheck.exists():
                        pass
                    else:
                        newstat = MiscStats.objects.create(player=player, yellowcards = entry[1], redcards = entry[2],
                                                            twoyellows = entry[3], foulscommited = entry[4], foulsdrawn = entry[5],
                                                            offsides = entry[6], PKwon = entry[7], PKconceded = entry[8],
                                                            owngoals = entry[9], ballsrecovered = entry[10])
                        newstat.save()
                    
            result = 'Y'
            return result

        except:
            result = 'N'
            return result
            
def aerialstats_mgmt(request):
    if request.method == 'POST':
        try:
            aerialstatsfile = request.FILES['aerial'].read().decode('UTF-8').splitlines()
            # Ready CSV
            aerialstats = csv.reader(aerialstatsfile)
            aerialstatslist = []
            for entry in aerialstats:
                aerialstatslist.append(entry)
            aerialstatslist = aerialstatslist[2:]
            # List wasn't looping properly into DB, had to make diferent list based on original range for each iteration
            rangestats = range(len(aerialstatslist))
            for i in rangestats:
                aerialstatslist = aerialstatslist[i:]
                for entry in aerialstatslist:
                    player = Player.objects.get(id = entry[0])
                    statcheck = AerialDuels.objects.filter(player = player.id)
                    if statcheck.exists():
                        pass
                    else:
                        newstat = AerialDuels.objects.create(player=player, won = entry[1], lost = entry[2], percentagewon = entry[3])
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