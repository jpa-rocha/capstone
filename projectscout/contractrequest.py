import json
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

teamcsv = pd.read_csv('scout/csv data/playerinfo.csv', usecols=['Squad'])
teamlist = []
teamcorrect = []
teams = set()
for team in teamcsv['Squad']:
    teamlist.append(team)
for team in teamlist:
    team = team.replace(' ', '-')
    teamcorrect.append(team)
    
teamfile = open('teams.txt', 'a')
for team in teamcorrect:
    teams.add(team)

for team in teams:
   teamfile.write(team.lower() + '\n')

teamfile.close()
teamfile = open('teamfix.txt', 'r')
teaminput = set()
for line in teamfile:
    teaminput.add(line.rstrip('\n'))

teamfile.close()

createfile = input('Create new contracts file?\n')

if createfile == 'y':
    path = r'C:\\Users\\janos\\Desktop\\Pro\\cs50\\Project-Scout\\projectscout\\chromedriver.exe'
    driver = webdriver.Chrome(executable_path = path)
    delay = 5
    for team in teaminput:
        driver.get(f'http://www.capology.com/club/{team}/salaries/')
        
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
            print ("Page is ready!")
        except TimeoutException:
            print ("Loading took too much time!")

        data = myElem.find_elements_by_tag_name("tr")
        file = open('full.txt', 'a', encoding="utf-8")
        for elem in data:
            elem = elem.find_elements_by_tag_name("td")

            for i in elem[2:]:
                if i.get_attribute("class") != " verified-column center-align border-right-column":
                    file.write(i.text + '\n')
                    print(i.text)
            file.write('\r')
else:
    pass

convertjson = input('Convert contract file to json? \n')

if convertjson == 'y':
    contractfile = 'full.txt'
    

    with open(contractfile, 'r', encoding="utf-8" ) as fh:
        dict1 = {}
        dict2 = {}
        playernum = 0
        fields = ['name', 'weeklysalary', 'yearlysalary', 'position', 'age', 'status', 'expirationdate', 'length', 'estimatedtotal']
        fieldlen = len(fields)
        i = 0
        for line in fh:
            if line == '\n':
                dict1.update({playernum: dict2.copy()})
                playernum = playernum + 1
            else:
                description = line.strip('\n')
                dict2[fields[i]] = description 
                i = i+1
                if i == fieldlen:
                    i = 0
        

    out_file = open("contractinfo.json", "w", encoding="utf-8")
    json.dump(dict1, out_file, indent = 4, ensure_ascii=False)
    out_file.close()

with open('contractinfo.json', 'r', encoding='utf-8') as cont:
    contracts = json.load(cont)
    print(contracts['0'])
    for i in contracts:
        print(contracts[str(i)]['name'])