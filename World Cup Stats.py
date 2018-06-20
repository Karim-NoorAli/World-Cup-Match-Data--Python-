from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd

################### Paste the url of that particular match from indianexpress.com and get your data ##########
url = 'https://indianexpress.com/section/fifa/schedules-fixtures/portugal-vs-morocco-fifa-2018-21991-scorecard/'

u_client = uReq(url)
page_html = u_client.read()
u_client.close()

page_soup = soup(page_html,"html.parser")

Headings_html = page_soup.findAll("div",{"class":"tops"})
Headings = Headings_html[0].findAll("li")

stats_html = page_soup.findAll("div",{"class":"goal"})

teams_html = page_soup.findAll("div", {"class":"heading"})
teams = []

for team in teams_html:
    teams.append(team.text)

i = 0
H_Team = []
A_Team = []
Event = []

for stat in stats_html:
    stats = stats_html[i].findAll("li")    
    H_Team.append(stats[0].text)
    Event.append(stats[1].text)
    A_Team.append(stats[2].text)
    i+=1
        
H_Team = list(map(int, H_Team))
A_Team = list(map(int, A_Team))

ply_by_ply_html = page_soup.findAll("div", {"class":"ply-by-ply"})

# extracts individual events from play by play
list_items = ply_by_ply_html[0].findAll("li")

PBP_Minute = []
PBP_Event = []
PBP_Team = []
Event_Details = [] 
min = ""

for tag in list_items:
    min = tag.find("span").text
    min = min.replace("'","")
    PBP_Minute.insert(0, min)
    PBP_Event.insert(0, tag.find("h3").text)
    Event_Details.insert(0, tag.find("p").text)
    
    player_team = tag.find("p").text
    if teams[0] in player_team:
       PBP_Team.insert(0, teams[0])
    else:
       PBP_Team.insert(0, teams[1])


writer = pd.ExcelWriter(Headings[0].text + ' VS '+Headings[2].text + '.xlsx', engine='xlsxwriter')

df = pd.DataFrame({Headings[1].text:Event,Headings[0].text:H_Team,Headings[2].text:A_Team})

df.to_excel(writer,sheet_name='Game Stats',columns=[Headings[1].text,Headings[0].text,Headings[2].text],index=False)

df2 = pd.DataFrame({"Minute":PBP_Minute, "Event":PBP_Event, "Team":PBP_Team, "Event Details":Event_Details})

df2.to_excel(writer, sheet_name='Play by Play', columns=["Minute", "Event", "Team", "Event Details"], index=False)

writer.save()

