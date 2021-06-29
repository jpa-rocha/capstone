from django.contrib import auth
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import MiscStats, League, Player, PlayingTime, ShootingStats, Team, AerialDuels, PossessionStats, PassingStats, PassTypesStats, DefensiveStats, GoalShotCreationStats, GoalkeepingStats
from .dataloader import team_mgmt, player_mgmt, time_mgmt, miscstats_mgmt, aerialstats_mgmt, shootingstats_mgmt, possessionstats_mgmt, passingstats_mgmt, passtypesstats_mgmt, defensivestats_mgmt, goalshotcreationstats_mgmt, goalkeepingstats_mgmt
import pandas as pd
import csv
import json


# Create your views here.
def index(request):
    pass 

    return render(request, "scout/index.html")

def player(request, id):
    pass

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