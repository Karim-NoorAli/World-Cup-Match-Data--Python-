from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd
import re

########## Paste the url of that particular match from indianexpress.com and get your data ##########

url = 'https://indianexpress.com/section/fifa/schedules-fixtures/russia-vs-saudi-arabia-fifa-2018-21974-scorecard/'

u_client = uReq(url)
page_html = u_client.read()
u_client.close()

page_soup = soup(page_html, "html.parser")

########## Team Name Code ##########
# extracts teams

teams_html = page_soup.findAll("div", {"class":"heading"})
teams = []

# loop to place teams in list
for team in teams_html:
    teams.append(team.text)
xlwb = teams[0] + " vs. " + teams[1] + ".xlsx"

########## Game Summary Code ##########
stats_html = page_soup.findAll("div", {"class":"goal"})

sp = re.compile('^ ')

i = 0
Home = []
Stat = []
Away = []

# loop to place game summary stats in lists

for ul in stats_html:
    stats = stats_html[i].findAll("li")
    Home.append(sp.sub("", stats[0].text))
    Stat.append(sp.sub("", stats[1].text))
    Away.append(sp.sub("", stats[2].text))
    i += 1

Home = list(map(int, Home))
Away = list(map(int, Away))


########## Play by Play Code ##########

# extracts play by play event data
ply_by_ply_html = page_soup.findAll("div", {"class":"ply-by-ply"})

# extracts individual events from play by play
list_items = ply_by_ply_html[0].findAll("li")

PBP_Minute = []
PBP_Event = []
PBP_Team = []

# loop to place live stats in list
for tag in list_items:
    PBP_Minute.insert(0, tag.find("span").text)
    PBP_Event.insert(0, tag.find("h3").text)
    
    player_team = tag.find("p").text
    if teams[0] in player_team:
       PBP_Team.insert(0, teams[0])
    else:
       PBP_Team.insert(0, teams[1])

writer = pd.ExcelWriter(xlwb, engine='xlsxwriter')

fs = pd.DataFrame({"Key Stats":Stat, "Home Team":Home, "Away Team":Away})

fs.to_excel(writer, sheet_name='Game Summary', columns=["Key Stats", "Home Team", "Away Team"], index=False)

ss = pd.DataFrame({"Minute":PBP_Minute, "Event":PBP_Event, "Team":PBP_Team})

ss.to_excel(writer, sheet_name='Play by Play', columns=["Minute", "Event", "Team"], index=False)

writer.save()
writer.close()
