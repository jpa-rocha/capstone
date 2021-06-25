from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import F
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

class ShootingStats(models.Model):
    
    #Standard stats
    player = ForeignKey(Player, on_delete=CASCADE, primary_key=True)
    goals = IntegerField()
    shots = IntegerField()
    shotsontarget = IntegerField()
    pershotsontarget = FloatField()
    shotsper90 = FloatField()
    shotsontargetper90 = FloatField()
    goalspershot = FloatField()
    goalpershotontarget = FloatField()
    avgdistance = FloatField()
    freekick = IntegerField()
    PKmade = IntegerField()
    PKattempted = IntegerField()

    #Expected Stats
    exgoals = FloatField()
    exnonPKgoals = FloatField()
    nonPKexgoalspershot = FloatField()
    goalsminusexgoals = FloatField()
    nonpkgoalsminusexnonPKgoals = FloatField()

    def serialize(self):
        return {
            'player' : self.player.name,
            'goals' : self.goals,
            'shots' : self.shots,
            'shotsontarget' : self.shotsontarget,
            'pershotsontarget' : self.pershotsontarget,
            'shotsper90' : self.shotsper90,
            'shotsontargetper90' : self.shotsontargetper90,
            'goalspershot' : self.goalspershot,
            'goalspershotontarget' : self.goalpershotontarget,
            'avgdistance' : self.avgdistance,
            'freekick' : self.freekick,
            'PKmade' : self.PKmade,
            'PKattempted' : self.PKattempted,
            'exgoals' : self.exgoals,
            'exnonPKgoals' : self.exnonPKgoals,
            'nonPKexgoalspershot' : self.nonPKexgoalspershot,
            'goalminusexgoals' : self.goalsminusexgoals,
            'nonpkgoalsminusexnonPKgoals' : self.nonpkgoalsminusexnonPKgoals
        }
    def __str__(self):
        return self.player.name

class PossessionStats(models.Model):
    player = ForeignKey(Player, on_delete=CASCADE, primary_key=True)

    # Touches location
    touches = IntegerField()
    touchesdefbox = IntegerField()
    touchesdef3rd = IntegerField()
    touchesmid3rd = IntegerField()
    touchesatt3rd = IntegerField()
    touchesattbox = IntegerField()
    liveball = IntegerField()

    # Dribbling
    sucessfuldribbles = IntegerField()
    attempteddribbles = IntegerField()
    dribblesucesspercentage = FloatField()
    playerspassed = IntegerField()

    # Carries
    carries = IntegerField()
    totaldistance = IntegerField()
    progressivedistance = IntegerField()
    progressivecarries = IntegerField()
    carrieslast3rd = IntegerField()
    carriesattackingbox = IntegerField()
    miscarries = IntegerField()
    disarmed = IntegerField()

    # Recieving
    targeted = IntegerField()
    recieved = IntegerField()
    recievedsucesspercentage = FloatField()
    progressivepassesrecieved = IntegerField()

    def serialize(self):
        return {
            'player' : self.player.name,
            'touches': self.touches,
            'defensivebox' : self.touchesdefbox,
            'defensive3rd' : self.touchesdef3rd,
            'middle3rd' : self.touchesmid3rd,
            'attacking3rd' : self.touchesatt3rd,
            'attackingbox' : self.touchesattbox,
            'liveball' : self.liveball,
            'sucessfuldribbles' : self.sucessfuldribbles,
            'attempteddribbles' : self.attempteddribbles,
            'dribblesucesspercentage' : self.dribblesucesspercentage,
            'playerspassed' : self.playerspassed,
            'carries' : self.carries,
            'totaldistance' : self.totaldistance,
            'progressivedistance' : self.progressivedistance,
            'progressivecarries' : self.progressivecarries,
            'carrieslast3rd' : self.carrieslast3rd,
            'carriesattackingbox' : self.carriesattackingbox,
            'miscarries' : self.miscarries,
            'disarmed' : self.disarmed,
            'targeted' : self.targeted,
            'recieved' : self.recieved,
            'recievedsucesspercentage' : self.recievedsucesspercentage,
            'progressivepassesrecieved' : self.progressivepassesrecieved
        }
    def __str__(self):
        return self.player.name

class PassingStats(models.Model):
    player = ForeignKey(Player, on_delete=CASCADE, primary_key=True)

    # Total pass stats
    totalcomplete = IntegerField()
    totalattempted = IntegerField()
    totalcomppercentage = FloatField()
    totaldistance = IntegerField()
    progressivedistance = IntegerField()

    # Short pass stats
    shortcomplete = IntegerField()
    shortattempted = IntegerField()
    shortcompprecentage = FloatField()

    # Medium pass stats
    mediumcomplete = IntegerField()
    mediumattempted = IntegerField()
    mediumcompprecentage = FloatField()

    # Long pass stats
    longcomplete = IntegerField()
    longattempted = IntegerField()
    longcompprecentage = FloatField()

    # General pass stats
    assists = IntegerField()
    exassists = FloatField()
    assistsminusexassists = FloatField()
    passledtoshot = IntegerField()
    passesintofinal3rd = IntegerField()
    passesattackingbox = IntegerField()
    crossintobox = IntegerField()
    progressivepasses = IntegerField()

    def serialize(self):
        return {
            'player' : self.player.name,
            'totalcomplete' : self.totalcomplete,
            'totalattempted' : self.totalattempted,
            'totalcomppercentage' : self.totalcomppercentage,
            'totaldistance' : self.totaldistance,
            'progressivedistance' : self.progressivedistance,
            'shortcomplete' : self.shortcomplete,
            'shortattempted' : self.shortattempted,
            'shortcompprecentage' : self.shortcompprecentage,
            'mediumcomplete' : self.mediumcomplete,
            'mediumattempted' : self.mediumattempted,
            'mediumcompprecentage' : self.mediumcompprecentage,
            'longcomplete' : self.longcomplete,
            'longattempted' : self.longattempted,
            'longcompprecentage' : self.longcompprecentage,
            'assists' : self.assists,
            'exassists' : self.exassists,
            'assistsminusexassists' : self.assistsminusexassists,
            'passledtoshot' : self.passledtoshot,
            'passesintofinal3rd' : self.passesintofinal3rd,
            'passesattackingbox' : self.passesattackingbox,
            'crossintobox' : self.crossintobox,
            'progressivepasses' : self.progressivepasses,
        }
    def __str__(self):
        return self.player.name

class PassTypesStats(models.Model):
    player = ForeignKey(Player, on_delete=CASCADE, primary_key=True)
    totalattempts = IntegerField()

    # Pass types
    liveball = IntegerField()
    deadball = IntegerField()
    freekicks = IntegerField()
    throughball = IntegerField()
    underpressure = IntegerField()
    plus40yards = IntegerField()
    crosses = IntegerField()
    cornerkicks = IntegerField()

    # Corner kicks
    CKinswing = IntegerField()
    CKoutswing = IntegerField()
    CKstraight = IntegerField()

    # Height
    groundpass = IntegerField()
    lowpass = IntegerField()
    highpass = IntegerField()

    # Body Parts
    leftfootpass = IntegerField()
    rightfootpass = IntegerField()
    header = IntegerField()
    throwin = IntegerField()
    other = IntegerField()

    # Outcomes
    completed = IntegerField()
    offside = IntegerField()
    outofbounds = IntegerField()
    intercepted = IntegerField()
    blocked = IntegerField()

    def serialize(self):
        return {
            'player' : self.player.name,
            'totalattempts' : self.totalattempts,
            'liveball' : self.liveball,
            'deadball' : self.deadball,
            'freekicks' : self.freekicks,
            'throughball' : self.throughball,
            'underpressure' : self.underpressure,
            'plus40yards' : self.plus40yards,
            'crosses' : self.crosses,
            'cornerkicks' : self.cornerkicks,
            'CKinswing' : self.CKinswing,
            'CKoutswing' : self.CKoutswing,
            'CKstraight' : self.CKstraight,
            'groundpass' : self.groundpass,
            'lowpass' : self.lowpass,
            'highpass' : self.highpass,
            'leftfootpass' : self.leftfootpass,
            'rightfootpass' : self.rightfootpass,
            'header' : self.header,
            'throwin' : self.throwin,
            'other' : self.other,
            'completed' : self.completed,
            'offside' : self.offside,
            'outofbounds' : self.outofbounds,
            'intercepted' : self.intercepted,
            'blocked' : self.blocked,
        }
    def __str__(self):
        return self.player.name

class DefensiveStats(models.Model):
    player = ForeignKey(Player, on_delete=CASCADE, primary_key=True)

    # Tackles
    tackles = IntegerField()
    tackleswon = IntegerField()
    tacklesdef3rd = IntegerField()
    tacklesmid3rd = IntegerField()
    tacklesatt3rd = IntegerField()

    # VS Dribble
    dribblerstackled = IntegerField()
    totalattempts = IntegerField()
    sucessvsdribble = FloatField()
    beatbydribble = IntegerField()

    # Pressures
    totalpressure = IntegerField()
    sucessfulpressure = IntegerField()
    presssucessper = FloatField()
    pressdef3rd = IntegerField()
    pressmid3rd = IntegerField()
    pressatt3rd = IntegerField()

    # Blocks
    blocks = IntegerField()
    shotblocks = IntegerField()
    shotontargetblocks = IntegerField()
    passblocks = IntegerField()

    # General
    interceptions = IntegerField()
    tacklesplusints = IntegerField()
    clearings = IntegerField()
    errors = IntegerField()

    def serialize(self):
        return {
            'player' : self.player.name,
            'tackles' : self.tackles,
            'tackleswon' : self.tackleswon,
            'tacklesdef3rd' : self.tacklesdef3rd,
            'tacklesmid3rd' : self.tacklesmid3rd,
            'tacklesatt3rd' : self.tacklesatt3rd,
            'dribblerstackled' : self.dribblerstackled,
            'totalattempts' : self.totalattempts,
            'sucessvsdribble' : self.sucessvsdribble,
            'beatbydribble' : self.beatbydribble,
            'totalpressure' : self.totalpressure,
            'sucessfulpressure' : self.sucessfulpressure,
            'presssucessper' : self.presssucessper,
            'pressdef3rd' : self.pressdef3rd,
            'pressmid3rd' : self.pressmid3rd,
            'pressatt3rd' : self.pressatt3rd,
            'blocks' : self.blocks,
            'shotblocks' : self.shotblocks,
            'shotontargetblocks' : self.shotontargetblocks,
            'passblocks' : self.passblocks,
            'interceptions' : self.interceptions,
            'tacklesplusints' : self.tacklesplusints,
            'clearings' : self.clearings,
            'errors' : self.errors,
        }
    def __str__(self):
        return self.player.name

class GoalShotCreationStats(models.Model):
    player = ForeignKey(Player, on_delete=CASCADE, primary_key=True)

    # Shot creating actions
    shotcreatingactions = IntegerField()
    shotcreatingactionsper90 = FloatField()

    # Shot creating action types
    SCAliveballpass = IntegerField()
    SCAdeadballpass = IntegerField()
    SCAdribble = IntegerField()
    SCAshots = IntegerField()
    SCAfoulsdrawn = IntegerField()
    SCAdefensiveaction = IntegerField()

    # Goal creating actions
    goalcreatingaction = IntegerField()
    goalcreatingactionper90 = FloatField()

    # Goal creating action types
    GCAliveballpass = IntegerField()
    GCAdeadballpass = IntegerField()
    GCAdribble = IntegerField()
    GCAshots = IntegerField()
    GCAfoulsdrawn = IntegerField()
    GCAdefensiveaction = IntegerField()

    def serialize(self):
        return {
            'player' : self.player.name,
            'shotcreatingactions' : self.shotcreatingactions,
            'shotcreatingactionsper90' : self.shotcreatingactionsper90,
            'SCAliveballpass' : self.SCAliveballpass,
            'SCAdeadballpass' : self.SCAdeadballpass,
            'SCAdribble' : self.SCAdribble,
            'SCAshots' : self.SCAshots,
            'SCAfoulsdrawn' : self.SCAfoulsdrawn,
            'SCAdefensiveaction' : self.SCAdefensiveaction,
            'goalcreatingaction' : self.goalcreatingaction,
            'goalcreatingactionper90' : self.goalcreatingactionper90,
            'GCAliveballpass' : self.GCAliveballpass,
            'GCAdeadballpass' : self.GCAdeadballpass,
            'GCAdribble' : self.GCAdribble,
            'GCAshots' : self.GCAshots,
            'GCAfoulsdrawn' : self.GCAfoulsdrawn,
            'GCAdefensiveaction' : self.GCAdefensiveaction,
        }
    def __str__(self):
        return self.player.name

class GoalkeepingStats(models.Model):
    player = ForeignKey(Player, on_delete=CASCADE, primary_key=True)

    # Performance stats
    goalsallowed = IntegerField()
    goalsallowedper90 = FloatField()
    shotsontargetagainst = IntegerField()
    saves = IntegerField()
    savesper = FloatField()
    wins = IntegerField()
    draws = IntegerField()
    losses = IntegerField()
    cleansheets = IntegerField()
    cleansheetsper = FloatField()

    # PK stats
    PKtotal = IntegerField()
    PKallowed = IntegerField()
    PKsaved = IntegerField()
    PKmissed = IntegerField()
    PKsaveper = FloatField()

    # Deadball & Own goals stats
    FKgoals = IntegerField()
    CKgoals = IntegerField()
    OGgoals = IntegerField()
    
    # Expected stats
    exgoalsallowed = FloatField()
    exgoalsallowedperSoT = FloatField()
    exgoalsallowedminusgoalsallowed = FloatField()
    exgoalsallowedminusgoalsallowedper90 = FloatField()

    # Launched attacks
    passesover40yrdscompleted = IntegerField()
    passesover40yrdsattempted = IntegerField()
    passesover40yrdscmpper = FloatField()

    # Passes
    passesattempted = IntegerField()
    throwsattempted = IntegerField()
    passlaunchper = FloatField()
    passavglength = FloatField()

    # Goal kicks
    GKattempted = IntegerField()
    GKlaunchper = FloatField()
    GKavglength = FloatField()

    # Crosses 
    attemptedcrosses = IntegerField()
    crossesstoped = IntegerField()
    crossstopper = FloatField()

    # Sweeper
    DAOB = IntegerField()
    DAOBper90 = FloatField()
    DAOBavgdistance = FloatField()

    def serialize(self):
        return {
            'player' : self.player.name,
            'goalsallowed' : self.goalsallowed,
            'goalsallowedper90' : self.goalsallowedper90,
            'shotsontargetagainst' : self.shotsontargetagainst,
            'saves' : self.saves,
            'savesper' : self.savesper,
            'wins' : self.wins,
            'draws' : self.draws,
            'losses' : self.losses,
            'cleansheets' : self.cleansheets,
            'cleansheetsper' : self.cleansheetsper,
            'PKtotal' : self.PKtotal,
            'PKallowed' : self.PKallowed,
            'PKsaved' : self.PKsaved,
            'PKmissed' : self.PKmissed,
            'PKsaveper' : self.PKsaveper,
            'FKgoals' : self.FKgoals,
            'CKgoals' : self.CKgoals,
            'OGgoals' : self.OGgoals,
            'exgoalsallowed' : self.exgoalsallowed,
            'exgoalsallowedperSoT' : self.exgoalsallowedperSoT,
            'exgoalsallowedminusgoalsallowed' : self.exgoalsallowedminusgoalsallowed,
            'exgoalsallowedminusgoalsallowedper90' : self.exgoalsallowedminusgoalsallowedper90,
            'passesover40yrdscompleted' : self.passesover40yrdscompleted,
            'passesover40yrdsattempted' : self.passesover40yrdsattempted,
            'passesover40yrdscmpper' : self.passesover40yrdscmpper,
            'passesattempted' : self.passesattempted,
            'throwsattempted' : self.throwsattempted,
            'passlaunchper' : self.passlaunchper,
            'passavglength' : self.passavglength,
            'GKattempted' : self.GKattempted,
            'GKlaunchper' : self.GKlaunchper,
            'GKavglength' : self.GKavglength,
            'attemptedcrosses' : self.attemptedcrosses,
            'crossesstoped' : self.crossesstoped,
            'crossstopper' : self.crossstopper,
            'DAOB' : self.DAOB,
            'DAOBper90' : self.DAOBper90,
            'DAOBavgdistance' : self.DAOBavgdistance,
        }
    def __str__(self):
        return self.player.name

