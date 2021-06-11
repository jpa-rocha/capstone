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
standardstats = pd.read_csv('scout/csv data/standard.csv')
playingtime = pd.read_csv('scout/csv data/standard.csv', usecols=[0,8,9,10,11])
playingtime.to_csv('scout/csv data/cleaned/time.csv', index=False)


print(playingtime)
