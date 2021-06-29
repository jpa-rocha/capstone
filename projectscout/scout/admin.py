from django.contrib import admin
from .models import MiscStats, League, Player, PlayingTime, ShootingStats, Team, AerialDuels, PossessionStats, PassingStats, PassTypesStats, DefensiveStats, GoalShotCreationStats, GoalkeepingStats
# Register your models here.
admin.site.register(League)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(PlayingTime)
admin.site.register(MiscStats)
admin.site.register(ShootingStats)
admin.site.register(AerialDuels)
admin.site.register(PossessionStats)
admin.site.register(PassingStats)
admin.site.register(PassTypesStats)
admin.site.register(DefensiveStats)
admin.site.register(GoalShotCreationStats)
admin.site.register(GoalkeepingStats)
