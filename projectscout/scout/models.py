from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey

# Create your models here.
#class User(AbstractUser):
 #   pass

class League(models.Model):
    name = CharField(max_length=20)
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
    def __str__(self):
        return self.name

class Team(models.Model):
    name = CharField(max_length=70)
    league = ForeignKey(League, on_delete=CASCADE)
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'league': self.league.name
            
        }