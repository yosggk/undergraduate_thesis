import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

N_PAGES = 52
titles = []
dates = []
abstracts = []
USproxies = {
    "http":"40.117.231.19:3128",
    "https":"40.117.231.19:3128"
}

for i in range(1, N_PAGES+1):
    url = "https://www.ft.com/search?q=blockchain&page=" + str(i) + "&dateTo=2018-12-31&dateFrom=2016-07-16&sort=date&expandRefinements=true"
    res = requests.get(url, proxies=USproxies, auth=('******', '******')) # auth=("hogehoge@gmail.com", "12345678")
    soup = BeautifulSoup(res.text, "lxml")
    for elm in soup.find_all("div", class_="o-teaser__content"):
        titles.append(elm.find("a", class_="js-teaser-heading-link").get_text())
        dates.append(elm.find("time").get_text())
        if elm.find("p", class_="o-teaser__standfirst"):
            abstracts.append(elm.find("p", class_="o-teaser__standfirst").get_text())
        else:
            abstracts.append(" ")
        time.sleep(1)
for i in range(1, N_PAGES+1):
    url = "https://www.ft.com/search?q=blockchain&page=" + str(i) + "&dateTo=2016-07-15&dateFrom=2003-01-01&sort=date&expandRefinements=true"
    res = requests.get(url, proxies=USproxies, auth=('******', '******')) # auth=("hogehoge@gmail.com", "12345678")
    soup = BeautifulSoup(res.text, "lxml")
    for elm in soup.find_all("div", class_="o-teaser__content"):
        titles.append(elm.find("a", class_="js-teaser-heading-link").get_text())
        dates.append(elm.find("time").get_text())
        if elm.find("p", class_="o-teaser__standfirst"):
            abstracts.append(elm.find("p", class_="o-teaser__standfirst").get_text())
        else:
            abstracts.append(" ")
        time.sleep(1)

data = [dates, titles, abstracts]
df = pd.DataFrame(data).T
df.to_csv("ft-data.csv")