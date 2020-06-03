import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
N = 60
BT = 2
titles = []
dates = []
abstracts = []
USproxies = {
    "http":"40.117.231.19:3128",
    "https":"40.117.231.19:3128"
}

for i in range(1, N+1):
    url = 'https://www.wsj.com/search/term.html?KEYWORDS=blockchain&min-date=2013/01/01&max-date=2018/12/31&isAdvanced=true&daysback=90d&andor=AND&sort=date-desc&source=wsjarticle,wsjblogs,wsjvideo,interactivemedia,sitesearch,wsjpro&ns=prod/accounts-wsj&page=' + str(i)
    res = requests.get(url, proxies=USproxies)
    soup = BeautifulSoup(res.text, "lxml")
    for elm in soup.find_all("div", class_="item-container"):
        titles.append(elm.find("h3", class_="headline").get_text())
        dates.append(elm.find("time").get_text())
        for elm2 in elm.find_all("div", class_="summary-container"):
            abstracts.append(elm2.find("p").get_text()) 

data = [titles, dates, abstracts]
with open('data.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(data)