from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, FloatField, IntegerField
from django.db.models.fields.files import FileField
from django.db.models.fields.related import ForeignKey

# Create your models here.
class DataStorage(models.Model):
    file = FileField(upload_to='uploads/')



class League(models.Model):
    name = CharField(max_length=20)
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name
        }
    def __str__(self):
        return self.name

class Team(models.Model):
    name = CharField(max_length=70)
    league = ForeignKey(League, on_delete=CASCADE)
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'league' : self.league.name
        }
    def __str__(self):
        return self.name

class Player(models.Model):
    name = CharField(max_length = 200)
    country = CharField(max_length=3)
    position = CharField(max_length=5)
    yearborn = IntegerField()
    team = ForeignKey(Team, on_delete=models.PROTECT, related_name='team')
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'position' : self.position,
            'born' : self.yearborn,
            'team' : self.team.name
        }
    def __str__(self):
        return self.name

class PlayingTime(models.Model):
    player = ForeignKey(Player, on_delete=CASCADE, primary_key=True)
    matchesplayed = IntegerField()
    starts = IntegerField()
    minutes = IntegerField()
    minutesper90 = FloatField()
    def serialize(self):
        return {
            'player' : self.player.name,
            'matches' : self.matchesplayed,
            'starts' : self.starts,
            'minutes' : self.minutes,
            'per90' : self.minutesper90
        }
    def __str__(self):
        return self.player.name

class GeneralStats(models.Model):
    player = ForeignKey(Player, on_delete=CASCADE, primary_key=True)
    goals = IntegerField()
    assists = IntegerField()
    nonPKgoals = IntegerField()
    PKgoals = IntegerField()
    attemptedPK = IntegerField()
    yellowcards = IntegerField()
    redcards = IntegerField()
    def serialize(self):
        return {
            'player' : self.player.name,
            'goals' : self.goals,
            'assists' : self.assists,
            'nonPkgoals' : self.nonPKgoals,
            'PKgoals' : self.PKgoals,
            'attemptedPK' : self.attemptedPK,
            'yellowcards' : self.yellowcards,
            'redcards' : self.redcards
        }
    def __str__(self):
        return self.player.name

class ExpectedGeneralStats(models.Model):
    player = ForeignKey(Player, on_delete=CASCADE, primary_key=True)
    expectedgoals = FloatField()
    nonPKexpectedgoals = FloatField()
    expectedassists = FloatField()
    exnonPKgoalsandassists = FloatField()
    def serialize(self):
        return {
            'player' : self.player.name,
            'xgoals' : self.expectedgoals,
            'nonPKxgoals' : self.nonPKexpectedgoals,
            'xassists' : self.expectedassists,
            'xnonPKganda' : self.exnonPKgoalsandassists
        }  
    def __str__(self):
        return self.player.name

class GeneralStatsPer90(models.Model):
    player = ForeignKey(Player, on_delete=CASCADE, primary_key=True)
    goals = FloatField()
    assists = FloatField()
    goalsplusassists = FloatField()
    nonPKgoals = FloatField()
    nonPKgoalsplusassists = FloatField()
    def serialize(self):
        return {
            'player' : self.player.name,
            'goals' : self.goals,
            'assists' : self.assists,
            'goals+assists' : self.goalsplusassists,
            'nonPkgoals' : self.nonPKgoals,
            'nonPKgoals+assists' : self.nonPKgoalsplusassists,
        }
    def __str__(self):
        return self.player.name

class ExpectedGeneralStatsPer90(models.Model):
    player = ForeignKey(Player, on_delete=CASCADE, primary_key=True)
    exgoals = FloatField()
    exassists = FloatField()
    exgoalsplusassists = FloatField()
    exnonPKgoals = FloatField()
    exnonPKgoalsplusassists = FloatField()
    def serialize(self):
        return {
            'player' : self.player.name,
            'exgoals' : self.exgoals,
            'exassists' : self.exassists,
            'exgoals+assists' : self.exgoalsplusassists,
            'exnonPkgoals' : self.exnonPKgoals,
            'exnonPKgoals+assists' : self.exnonPKgoalsplusassists,
        }
    def __str__(self):
        return self.player.name