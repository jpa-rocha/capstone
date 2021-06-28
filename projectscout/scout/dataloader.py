from .models import MiscStats, League, Player, PlayingTime, ShootingStats, Team, AerialDuels, PossessionStats, PassingStats, PassTypesStats, DefensiveStats, GoalShotCreationStats, GoalkeepingStats
import csv

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

def shootingstats_mgmt(request):
    if request.method == 'POST':
        try:
            shootingstatsfile = request.FILES['shooting'].read().decode('UTF-8').splitlines()
            # Ready CSV
            shootingstats = csv.reader(shootingstatsfile)
            shootingstatslist = []
            for entry in shootingstats:
                shootingstatslist.append(entry)
            shootingstatslist = shootingstatslist[2:]
            # List wasn't looping properly into DB, had to make diferent list based on original range for each iteration
            rangestats = range(len(shootingstatslist))
            for i in rangestats:
                shootingstatslist = shootingstatslist[i:]
                for entry in shootingstatslist:
                    player = Player.objects.get(id = entry[0])
                    statcheck = ShootingStats.objects.filter(player = player.id)
                    if statcheck.exists():
                        pass
                    else:
                        newstat = ShootingStats.objects.create(player=player, goals = entry[1], shots = entry[2],
                                                            shotsontarget = entry[3], pershotsontarget = entry[4],
                                                            shotsper90 = entry[5], shotsontargetper90 = entry[6], 
                                                            goalspershot = entry[7], goalpershotontarget = entry[8],
                                                            avgdistance = entry[9], freekick = entry[10], PKmade = entry[11],
                                                            PKattempted = entry[12], exgoals = entry[13], exnonPKgoals = entry[14],
                                                            nonPKexgoalspershot = entry[15], goalsminusexgoals = entry[16],
                                                            nonpkgoalsminusexnonPKgoals = entry[17])
                        newstat.save()
    
            result = 'Y'
            return result

        except:
            result = 'N'
            return result

def possessionstats_mgmt(request):
    if request.method == 'POST':
        try:
            possessionstatsfile = request.FILES['possession'].read().decode('UTF-8').splitlines()
            # Ready CSV
            possessionstats = csv.reader(possessionstatsfile)
            possessionstatslist = []
            for entry in possessionstats:
                possessionstatslist.append(entry)
            possessionstatslist = possessionstatslist[2:]
            # List wasn't looping properly into DB, had to make diferent list based on original range for each iteration
            rangestats = range(len(possessionstatslist))
            for i in rangestats:
                possessionstatslist = possessionstatslist[i:]
                for entry in possessionstatslist:
                    player = Player.objects.get(id = entry[0])
                    statcheck = PossessionStats.objects.filter(player = player.id)
                    if statcheck.exists():
                        pass
                    else:
                        newstat = PossessionStats.objects.create(player=player, touches = entry[1], defensivebox = entry[2],
                                                            defensive3rd = entry[3], middle3rd = entry[4],
                                                            attacking3rd = entry[5], attackingbox = entry[6], 
                                                            liveball = entry[7], sucessfuldribbles = entry[8],
                                                            attempteddribbles = entry[9], dribblesucesspercentage = entry[10], 
                                                            playerspassed = entry[11], carries = entry[12], totaldistance = entry[13], 
                                                            progressivedistance = entry[14], progressivecarries = entry[15], 
                                                            carrieslast3rd = entry[16], carriesattackingbox = entry[17], miscarries = entry[18],
                                                            disarmed = entry[19], targeted = entry[20], recieved = entry[21],
                                                            recievedsucesspercentage = entry[22], progressivepassesrecieved = entry[23])
                        
                        newstat.save()
            
            result = 'Y'
            return result

        except:
            result = 'N'
            return result

def passingstats_mgmt(request):
    if request.method == 'POST':
        try:
            passingstatsfile = request.FILES['passing'].read().decode('UTF-8').splitlines()
            # Ready CSV
            passingstats = csv.reader(passingstatsfile)
            passingstatslist = []
            for entry in passingstats:
                passingstatslist.append(entry)
            passingstatslist = passingstatslist[2:]
            # List wasn't looping properly into DB, had to make diferent list based on original range for each iteration
            rangestats = range(len(passingstatslist))
            for i in rangestats:
                passingstatslist = passingstatslist[i:]
                for entry in passingstatslist:
                    player = Player.objects.get(id = entry[0])
                    statcheck = PassingStats.objects.filter(player = player.id)
                    if statcheck.exists():
                        pass
                    else:
                        newstat = PassingStats.objects.create(player=player, totalcomplete = entry[1], totalattempted = entry[2],
                                                            totalcomppercentage = entry[3], totaldistance = entry[4],
                                                            progressivedistance = entry[5], shortcomplete = entry[6], 
                                                            shortattempted = entry[7], shortcompprecentage = entry[8],
                                                            mediumcomplete = entry[9], mediumattempted = entry[10], 
                                                            mediumcompprecentage = entry[11], longcomplete = entry[12], longattempted = entry[13], 
                                                            longcompprecentage = entry[14], assists = entry[15], 
                                                            exassists = entry[16], assistsminusexassists = entry[17], passledtoshot = entry[18],
                                                            passesintofinal3rd = entry[19], passesattackingbox = entry[20], crossintobox = entry[21],
                                                            progressivepasses = entry[22])
                        
                        newstat.save()
            
            result = 'Y'
            return result

        except:
            result = 'N'
            return result

def passtypesstats_mgmt(request):
    if request.method == 'POST':
        try:
            passtypesstatsfile = request.FILES['passtypes'].read().decode('UTF-8').splitlines()
            # Ready CSV
            passtypesstats = csv.reader(passtypesstatsfile)
            passtypesstatslist = []
            for entry in passtypesstats:
                passtypesstatslist.append(entry)
            passtypesstatslist = passtypesstatslist[2:]
            # List wasn't looping properly into DB, had to make diferent list based on original range for each iteration
            rangestats = range(len(passtypesstatslist))
            for i in rangestats:
                passtypesstatslist = passtypesstatslist[i:]
                for entry in passtypesstatslist:
                    player = Player.objects.get(id = entry[0])
                    statcheck = PassTypesStats.objects.filter(player = player.id)
                    if statcheck.exists():
                        pass
                    else:
                        newstat = PassTypesStats.objects.create(player=player, totalattempts = entry[1], liveball = entry[2],
                                                            deadball = entry[3], freekicks = entry[4],
                                                            throughball = entry[5], underpressure = entry[6], 
                                                            plus40yards = entry[7], crosses = entry[8],
                                                            cornerkicks = entry[9], CKinswing = entry[10], 
                                                            CKoutswing = entry[11], CKstraight = entry[12], groundpass = entry[13], 
                                                            lowpass = entry[14], highpass = entry[15], 
                                                            leftfootpass = entry[16], rightfootpass = entry[17], header = entry[18],
                                                            throwin = entry[19], other = entry[20], completed = entry[21],
                                                            offside = entry[22], outofbounds = entry[23], intercepted = entry[24], blocked = entry[25])
                        
                        newstat.save()
            
            result = 'Y'
            return result

        except:
            result = 'N'
            return result

def defensivestats_mgmt(request):
    if request.method == 'POST':
        try:
            defensivestatsfile = request.FILES['defensive'].read().decode('UTF-8').splitlines()
            # Ready CSV
            defensivestats = csv.reader(defensivestatsfile)
            defensivestatslist = []
            for entry in defensivestats:
                defensivestatslist.append(entry)
            defensivestatslist = defensivestatslist[2:]
            # List wasn't looping properly into DB, had to make diferent list based on original range for each iteration
            rangestats = range(len(defensivestatslist))
            for i in rangestats:
                defensivestatslist = defensivestatslist[i:]
                for entry in defensivestatslist:
                    player = Player.objects.get(id = entry[0])
                    statcheck = DefensiveStats.objects.filter(player = player.id)
                    if statcheck.exists():
                        pass
                    else:
                        newstat = DefensiveStats.objects.create(player=player, tackles = entry[1], tackleswon = entry[2],
                                                            tacklesdef3rd = entry[3], tacklesmid3rd = entry[4],
                                                            tacklesatt3rd = entry[5], dribblerstackled = entry[6], 
                                                            totalattempts = entry[7], sucessvsdribble = entry[8],
                                                            beatbydribble = entry[9], totalpressure = entry[10], 
                                                            sucessfulpressure = entry[11], presssucessper = entry[12], pressdef3rd = entry[13], 
                                                            pressmid3rd = entry[14], pressatt3rd = entry[15], 
                                                            blocks = entry[16], shotblocks = entry[17], shotontargetblocks = entry[18],
                                                            passblocks = entry[19], interceptions = entry[20], tacklesplusints = entry[21],
                                                            clearings = entry[22], errors = entry[23])
                        
                        newstat.save()
            
            result = 'Y'
            return result

        except:
            result = 'N'
            return result

def goalshotcreationstats_mgmt(request):
    if request.method == 'POST':
        try:
            goalshotcreationstatsfile = request.FILES['goalshotcreation'].read().decode('UTF-8').splitlines()
            # Ready CSV
            goalshotcreationstats = csv.reader(goalshotcreationstatsfile)
            goalshotcreationstatslist = []
            for entry in goalshotcreationstats:
                goalshotcreationstatslist.append(entry)
            goalshotcreationstatslist = goalshotcreationstatslist[2:]
            # List wasn't looping properly into DB, had to make diferent list based on original range for each iteration
            rangestats = range(len(goalshotcreationstatslist))
            for i in rangestats:
                goalshotcreationstatslist = goalshotcreationstatslist[i:]
                for entry in goalshotcreationstatslist:
                    player = Player.objects.get(id = entry[0])
                    statcheck = GoalShotCreationStats.objects.filter(player = player.id)
                    if statcheck.exists():
                        pass
                    else:
                        newstat = GoalShotCreationStats.objects.create(player=player, shotcreatingactions = entry[1], shotcreatingactionsper90 = entry[2],
                                                            SCAliveballpass = entry[3], SCAdeadballpass = entry[4],
                                                            SCAdribble = entry[5], SCAshots = entry[6], 
                                                            SCAfoulsdrawn = entry[7], SCAdefensiveaction = entry[8],
                                                            goalcreatingaction = entry[9], goalcreatingactionper90 = entry[10], 
                                                            GCAliveballpass = entry[11], GCAdeadballpass = entry[12], GCAdribble = entry[13], 
                                                            GCAshots = entry[14], GCAfoulsdrawn = entry[15], 
                                                            GCAdefensiveaction = entry[16])
                        
                        newstat.save()
            
            result = 'Y'
            return result

        except:
            result = 'N'
            return result
def goalkeepingstats_mgmt(request):
    if request.method == 'POST':
        try:
            goalkeepingstatsfile = request.FILES['goalkeeping'].read().decode('UTF-8').splitlines()
            # Ready CSV
            goalkeepingstats = csv.reader(goalkeepingstatsfile)
            goalkeepingstatslist = []
            for entry in goalkeepingstats:
                goalkeepingstatslist.append(entry)
            goalkeepingstatslist = goalkeepingstatslist[2:]
            for player in goalkeepingstatslist:
                player[0] = player[0].split('\\')
                player[0] = player[0][0]
            # List wasn't looping properly into DB, had to make diferent list based on original range for each iteration
            rangestats = range(len(goalkeepingstatslist))
            for i in rangestats:
                goalkeepingstatslist = goalkeepingstatslist[i:]
                for entry in goalkeepingstatslist:
                    team = Team.objects.get(name = entry[1])
                    player = Player.objects.get(name = entry[0], team=team)
                    statcheck = GoalkeepingStats.objects.filter(player = player.id)
                    
                    if statcheck.exists():
                        pass
                    else:
                        newstat = GoalkeepingStats.objects.create(player=player, goalsallowed = entry[2], goalsallowedper90 = entry[3], 
                                                                  shotsontargetagainst = entry[4], saves = entry[5], savesper = entry[6], 
                                                                  wins = entry[7], draws = entry[8], losses = entry[9], cleansheets = entry[10], 
                                                                  cleansheetsper = entry[11], PKtotal = entry[12], PKallowed = entry[13], 
                                                                  PKsaved = entry[14], PKmissed = entry[15], PKsaveper = entry[16], FKgoals = entry[17], 
                                                                  CKgoals = entry[18], OGgoals = entry[19], exgoalsallowed = entry[20], 
                                                                  exgoalsallowedperSoT = entry[21], exgoalsallowedminusgoalsallowed = entry[22], 
                                                                  exgoalsallowedminusgoalsallowedper90 = entry[23], passesover40yrdscompleted = entry[24], 
                                                                  passesover40yrdsattempted = entry[25], passesover40yrdscmpper = entry[26],
                                                                  passesattempted = entry[27], throwsattempted = entry[28], passlaunchper = entry[29], 
                                                                  passavglength = entry[30], GKattempted = entry[31], GKlaunchper = entry[32], 
                                                                  GKavglength = entry[33], attemptedcrosses = entry[34], crossesstoped = entry[35], 
                                                                  crossstopper = entry[36], DAOB = entry[37], DAOBper90 = entry[38], DAOBavgdistance = entry[39])

                        newstat.save()
            
            result = 'Y'
            return result
        except:
            result = 'N'
            return result
