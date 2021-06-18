from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, FloatField, IntegerField
from django.db.models.fields.related import ForeignKey

# Create your models here.
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

class MiscStats(models.Model):
    player = ForeignKey(Player, on_delete=CASCADE, primary_key=True)
    yellowcards = IntegerField()
    redcards = IntegerField()
    twoyellows = IntegerField()
    foulscommited = IntegerField()
    foulsdrawn = IntegerField()
    offsides = IntegerField()
    PKwon = IntegerField()
    PKconceded = IntegerField()
    owngoals = IntegerField()
    ballsrecovered = IntegerField()
    def serialize(self):
        return {
            'player' : self.player.name,
            'yellowcards' : self.yellowcards,
            'redcards' : self.redcards,
            '2yellows' : self.twoyellows,
            'foulscommited' : self.foulscommited,
            'foulsdrawn' : self.foulsdrawn,
            'offsides' : self.offsides,
            'PKwon' : self.PKwon,
            'PKconceded' : self.PKconceded,
            'OG' : self.owngoals,
            'ballsrecovered' : self.ballsrecovered
        }
    def __str__(self):
        return self.player.name

class AerialDuels(models.Model):
    player = ForeignKey(Player, on_delete=CASCADE, primary_key=True)
    won = IntegerField()
    lost = IntegerField()
    percentagewon = FloatField()
    def serialize(self):
        return {
            'player' : self.player.name,
            'aerialwon' : self.won,
            'aeriallost' : self.lost,
            'percentagewon' : self.percentagewon
        }
    def __str__(self):
        return self.player.name