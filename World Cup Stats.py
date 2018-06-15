from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import numpy as np
import pandas as pd

################### Paste the url of that particular match from indianexpress.com and get your data ##########
url = 'https://indianexpress.com/section/fifa/schedules-fixtures/russia-vs-saudi-arabia-fifa-2018-21974-scorecard/'

u_client = uReq(url)
page_html = u_client.read()
u_client.close()

page_soup = soup(page_html,"html.parser")

Headings_html = page_soup.findAll("div",{"class":"tops"})
Headings = Headings_html[0].findAll("li")

Headings[1]

stats_html = page_soup.findAll("div",{"class":"goal"})

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


df = pd.DataFrame({Headings[1].text:Event,Headings[0].text:H_Team,Headings[2].text:A_Team})

df.to_excel(Headings[0].text + ' VS '+Headings[2].text + '.xlsx',columns=[Headings[1].text,Headings[0].text,Headings[2].text],index=False)

