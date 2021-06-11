from django.contrib import auth
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.forms.widgets import Textarea
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.files import File
from django.shortcuts import render
from django.urls import reverse
from .models import League, Player, PlayingTime, Team
import csv
import json


# Create your views here.
def index(request):
    return render(request, "scout/index.html")

def team_mgmt(request):
    # Ready CSV
    teamsfile = open('C:/Users/janos/Desktop/Pro/cs50/Project-Scout/projectscout/scout/csv data/cleaned/steams.csv', 'r', encoding= "utf-8")
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
    
    #team list should come from DB
    return render(request, "scout/team-mgmt.html",{
        'teams' : teamlist
        }
    )

def player_mgmt(request):
    # Ready CSV
    playerfile = open('C:/Users/janos/Desktop/Pro/cs50/Project-Scout/projectscout/scout/csv data/cleaned/players.csv', 'r', encoding= "utf-8")
    players = csv.reader(playerfile)
    playerlist = []
    for player in players:
        playerlist.append(player)
    playerlist = playerlist[1:]

    for player in playerlist:
        player[0] = player[0].split('\\')
        player[0] = player[0][0]
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
    playersall = Player.objects.all
    return render(request, "scout/player-mgmt.html",{
        'players' : playersall
        }
    )

def time_mgmt(request):
    # Ready CSV
    timefile = open('C:/Users/janos/Desktop/Pro/cs50/Project-Scout/projectscout/scout/csv data/cleaned/time.csv', 'r', encoding= "utf-8")
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


    times = PlayingTime.objects.all()
    



    return render(request, "scout/time-mgmt.html",{
        'times' : times
        }
    )





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