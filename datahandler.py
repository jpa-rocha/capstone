import pandas as pd


playerinfo = pd.read_csv('csv data/playerinfo.csv')
playerinfo['Unnamed: 2'][1:] = playerinfo['Unnamed: 2'][1:].str.slice(start=-3)
playerinfo.to_csv('csv data/playerinfo.csv', index=False)


print(playerinfo['Unnamed: 4'])