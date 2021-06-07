import pandas as pd
import numpy as np

playerinfo = pd.read_csv('csv data/playerinfo.csv')
playerinfo['Unnamed: 5'][1:].str.replace('es La Liga', 'La Liga')


#playerinfo.to_csv('csv data/playerinfo.csv', index=False)


print(playerinfo['Unnamed: 5'][1:].str.replace('es La Liga', 'La Liga'))