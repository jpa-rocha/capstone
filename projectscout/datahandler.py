import pandas as pd

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

# Cleaned general stats CSV
standardstats = pd.read_csv('scout/csv data/standard.csv')
generalstats = pd.read_csv('scout/csv data/standard.csv', usecols=[0,12,13,14,15,16,17,18])
generalstats.to_csv('scout/csv data/cleaned/generalstats.csv', index=False)

# Cleaned expected gen stats CSV
exgenstats = pd.read_csv('scout/csv data/standard.csv', usecols=[0,24,25,26,27])
exgenstats.to_csv('scout/csv data/cleaned/expectedgeneralstats.csv', index=False)

# Cleaned general stats per 90 CSV
genstats90 = pd.read_csv('scout/csv data/standard.csv', usecols=[0,19,20,21,22,23])
genstats90.to_csv('scout/csv data/cleaned/generalstatsper90.csv', index=False)

# Cleaned expected general stats per 90
exgenstatsper90 = pd.read_csv('scout/csv data/standard.csv', usecols=[0,28,29,30,31,32])
exgenstatsper90.to_csv('scout/csv data/cleaned/expectedgeneralstatsper90.csv', index=False)

print(exgenstatsper90)
