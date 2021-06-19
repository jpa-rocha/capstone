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


print(shootingstats)
