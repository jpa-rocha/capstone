from django.contrib import admin
from .models import League, MiscStats, Team, Player, PlayingTime
# Register your models here.
admin.site.register(League)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(PlayingTime)
admin.site.register(MiscStats)