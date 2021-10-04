# Distinctiveness and Complexity

This projects has a database of football players from the top 5 European Leagues, with different game statistics and salaries.
The plan was to have a fast way to check how much teams pay for different results and the difference in the amounts of capital even within the top 5.

# Files
## projectscout
> ### contractrequest.py
>> contractrequest.py uses selenium to collect salary information from an online application, the page only displays the salaries asyncronously so the page needs to be emulated to  have access to the data. After collection the data is saved as a json file.

> ### datahandler.py
>> datahandler.py is used to prepare the data to fit the models, it takes the csv files located in scout/csv data/ and contractinfo.json and takes the appropriate information from them/ formats the information properly.

> ### contractinfo.json & fixedcontractinfo.json
>>  Original data scrapped with contractrequest.py and corrected data fixed with datahandler.py.

> ### requirements.txt
>>  Requiered exension to make the project work.

> ### chromedrive.exe
>> Needed for selenium to work

## projectscout/scout
> ### views.py
>> Controls most of the structure of the application:
>>> ### index
>>> Sends the names of the teams and the leagues to the main page and renders it.
>>> ### team
>>> Collects the salary information and team stats (points, goals for and against, wins, loses & draws, etc.) and renders the team page.
>>> ### league
>>> Recieves the name of the league and sends it back with the names of the corresponding teams while rendering the league page.
>>> ### upload_files
>>> Renders the upload page (only accessible to staff) and controls the name of the file inputed to send to dataloader.py.
>>> ### login, logout & register
>>> Do what the names say - WARNING - a normal user will not be able to upload to the database, you need to be a superuser or staff - WARNING.
>>> ## APIs
>>> ### salaryoverviewapi
>>> Collects the salary information for a whole league or a single team, does math to identify diferent percentiles to later be displayed on the page.
>>> ### teamsalaryapi
>>> Collects information on single player contracts within the team to create a bar graph showing the difference between starters and reserve players.
>>> ### leaguesalaryapi
>>> Does the same as the last API but on a league level, comparing salaries for starters and reserves across the teams.
>>> ### totalsalaryapi
>>> Same as the previous two APIs but on a global level, comparing the different salaries for starters and reserves across the leagues.
>>> ### salarygoalsapi, salaryassistsapi, salarytackesapi
>>> On a global level, it collects the stats and salaries from the top 100 players in order to plot a scatter graph, on a league level it uses the top 50.
> ### dataloader.py
>> Takes the CSV files from upload_files, and for each file, takes into account the columns necessary to fill the different models. It also takes care of empty values.
> ### models.py
>> Several models for each group of stats are linked through player_ids, which are linked thorugh team_ids. which are linked through league_ids.
>> Some of the stats are not used, but could be part of an expanded project.
## projectscout/scout/static/scout
> ### style.css
>> provides some styling for the pages.
> ### inmarkts.js
>> Uses plotly.js to create the graphics in the main page.
> ### league.js
>> Uses plotly.js to create the graphics in the league page.
> ### team.js
>> Uses plotly.js to create the graphics in the team page.
> ### plotly-2.2.0.min.js
>> Required to build the different graphics used through the page.
## projectscout/scout/templates/scout
> Includes all the templates for the pages themselves.
> ### layout.html
>> Includes all the scripts necessary for the page to run and limits the ability to see the upload page to staff members.
> ### index.html
>> Provides divs for plotly.js to create the main graphs in the intro page.
> ### league.html & team.html
>> Same as above, creates a dropdown menu to be able to select the teams. team.html also displays several team relevant stats.
> ### upload.html
>> Provides an entry point for the different CSVs and JSON files needed to populate the database.
> ### login.html & register.html 
>> Provide screens to login or register.
## projectscout/scout/csv data/
>> Here are the the original and fixed CSVs files to populate the db (courtesy of https://fbref.com/en/), when the original CSVs are corrected with datahandler.py they are formated and sent to the fixed folder, the fixed CSVs can be uploaded to the upload.html

