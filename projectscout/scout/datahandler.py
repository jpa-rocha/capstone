import pandas as pd


playerinfo = pd.read_csv('csv data/playerinfo.csv')
players = pd.read_csv('csv data/playerinfo.csv', usecols=['Player', 'Nation', 'Pos', 'Squad', 'Born'])
teams = pd.read_csv('csv data/playerinfo.csv', usecols=['Squad', 'Comp'])
teams.to_csv('csv data/teams.csv', index=False)
players.to_csv('csv data/players.csv', index=False)


teams = teams.drop_duplicates()
teams.to_csv('csv data/teams.csv', index=False)
teams_nodup = pd.read_csv('csv data/teams.csv')


print(players)
