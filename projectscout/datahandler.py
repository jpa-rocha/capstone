import pandas as pd
import json

# Cleaned player CSV
playerinfo = pd.read_csv('scout/csv data/playerinfo.csv')
players = pd.read_csv('scout/csv data/playerinfo.csv', usecols=['Player', 'Nation', 'Pos', 'Squad', 'Born'])
players.to_csv('scout/csv data/cleaned/players.csv', index=False)

# Cleaned teams CSV
teams = pd.read_csv('scout/csv data/playerinfo.csv', usecols=['Squad', 'Comp'])
teams.to_csv('scout/csv data/cleaned/teams.csv', index=False)
teams = teams.drop_duplicates()
teams.to_csv('scout/csv data/cleaned/teams.csv', index=False)

# Cleaned time stats CSV
playingtime = pd.read_csv('scout/csv data/standard.csv', usecols=[0,8,9,10,11])
playingtime.to_csv('scout/csv data/cleaned/time.csv', index=False)

# Cleaned misc stats CSV
miscstats = pd.read_csv('scout/csv data/misc.csv', usecols=[0,9,10,11,12,13,14,18,19,20,21])
miscstats.fillna(0, inplace=True)
miscstats.to_csv('scout/csv data/cleaned/miscstats.csv', index=False)

# Cleaned aerial stats CSV
aerialstats = pd.read_csv('scout/csv data/misc.csv', usecols=[0,22,23,24])
aerialstats.fillna(0, inplace=True)
aerialstats.to_csv('scout/csv data/cleaned/aerialstats.csv', index=False)

# Cleaned shooting stats CSV
shootingstats = pd.read_csv('scout/csv data/shooting.csv',usecols=[0,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])
shootingstats.fillna(0, inplace=True)
shootingstats.to_csv('scout/csv data/cleaned/shootingstats.csv', index=False)

# Cleaned possession stats CSV
possessionstats = pd.read_csv('scout/csv data/possession.csv',usecols=[0,9,10,11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,29,30,31,32])
possessionstats.fillna(0, inplace=True)
possessionstats.to_csv('scout/csv data/cleaned/possessionstats.csv', index=False)

# Cleaned passing stats CSV
passingstats = pd.read_csv('scout/csv data/passing.csv',usecols=[0,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])
passingstats.fillna(0, inplace=True)
passingstats.to_csv('scout/csv data/cleaned/passingstats.csv', index=False)

# Cleaned pass types stats CSV
passtypestats = pd.read_csv('scout/csv data/passtypes.csv',usecols=[0,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33])
passtypestats.fillna(0, inplace=True)
passtypestats.to_csv('scout/csv data/cleaned/passtypesstats.csv', index=False)

# Cleaned defensive stats CSV
defensivestats = pd.read_csv('scout/csv data/defensiveactions.csv',usecols=[0,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
defensivestats.fillna(0, inplace=True)
defensivestats.to_csv('scout/csv data/cleaned/defensivestats.csv', index=False)

# Cleaned goal/shot creation stats CSV
goalshotcreationstats = pd.read_csv('scout/csv data/goalshotcreation.csv',usecols=[0,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
goalshotcreationstats.fillna(0, inplace=True)
goalshotcreationstats.to_csv('scout/csv data/cleaned/goalshotcreationstats.csv', index=False)

# Cleaned goalkeeping stats CSV
goalkeepingstats = pd.read_csv('scout/csv data/goalkeeping.csv')
advgoalkeepingstats = pd.read_csv('scout/csv data/advgoalkeeping.csv')
fullgoalkeepingstats = goalkeepingstats.merge(advgoalkeepingstats, left_on = 'Unnamed: 0', right_on = 'Unnamed: 0')
fullgoalkeepingstats.to_csv('scout/csv data/fullgoalkeeping.csv', index=False)
finalgoalkeepingstats = pd.read_csv('scout/csv data/fullgoalkeeping.csv', usecols=[1,4,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,37,38,39,40,41,42,
                                                                                  43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59])
finalgoalkeepingstats.fillna(0, inplace=True)
finalgoalkeepingstats.to_csv('scout/csv data/cleaned/fullgoalkeepingstats.csv', index=False)

# Cleaned Salary information JSON
with open('contractinfo.json', 'r',encoding='utf-8') as file:
    contracts = json.load(file)
    for i in contracts:
        contracts[str(i)]['weeklysalary'] = contracts[str(i)]['weeklysalary'].replace(',','')
        contracts[str(i)]['yearlysalary'] = contracts[str(i)]['weeklysalary'].replace(',','')
        contracts[str(i)]['estimatedtotal'] = contracts[str(i)]['weeklysalary'].replace(',','')
        if contracts[str(i)]['weeklysalary'][0] == '£':
            contracts[str(i)]['weeklysalary'] = float(contracts[str(i)]['weeklysalary'][1:]) * 1.6
        elif contracts[str(i)]['weeklysalary'][0] == '€':
            contracts[str(i)]['weeklysalary'] = float(contracts[str(i)]['weeklysalary'][1:])
        if contracts[str(i)]['yearlysalary'][0] == '£':  
            contracts[str(i)]['yearlysalary'] = float(contracts[str(i)]['yearlysalary'][1:]) * 1.6
        elif contracts[str(i)]['yearlysalary'][0] == '€':  
            contracts[str(i)]['yearlysalary'] = float(contracts[str(i)]['yearlysalary'][1:]) 
        if contracts[str(i)]['estimatedtotal'][0] == '£': 
            contracts[str(i)]['estimatedtotal'] = float(contracts[str(i)]['estimatedtotal'][1:]) * 1.6
        elif contracts[str(i)]['estimatedtotal'][0] == '€':
            contracts[str(i)]['estimatedtotal'] = float(contracts[str(i)]['estimatedtotal'][1:])
        
        contracts[str(i)]['length'] = int(contracts[str(i)]['length'][0])
    fixedfile = open('fixedcontractinfo.json', 'w',encoding='utf-8')
    json.dump(contracts, fixedfile, indent = 4, ensure_ascii=False)
    fixedfile.close()


