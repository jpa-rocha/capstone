from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, IntegerField
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