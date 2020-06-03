# coding: UTF-8
"""
import urllib3
from bs4 import BeautifulSoup

http = urllib3.PoolManager()
# アクセスするURL
url = "http://www.nikkei.com/"

# URLにアクセスする htmlが帰ってくる → <html><head><title>経済、株価、ビジネス、政治のニュース:日経電子版</title></head><body....
#html = urllib3.urlopen(url)
r = http.request('GET', url)
# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(r, "html.parser")

# タイトル要素を取得する → <title>経済、株価、ビジネス、政治のニュース:日経電子版</title>
title_tag = soup.title

# 要素の文字列を取得する → 経済、株価、ビジネス、政治のニュース:日経電子版
title = title_tag.string

# タイトル要素を出力
print(title_tag)

# タイトルを文字列を出力
print(title)


import requests
from bs4 import BeautifulSoup

target_url = "https://style.nikkei.com/article/DGXNMSFK2702M_X20C14A3000000?channel=DF280120166594&style=1"

r = requests.get(target_url)

soup = BeautifulSoup(r.text, 'lxml')

print(soup.find_all("a", attrs={"class": "link", "href": "/link"}))
"""
import sys
import json
import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import codecs

def scraping(url, output_name):
    # Selenium settings
    driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
    # get a HTML response
    driver.get("https://style.nikkei.com/article/DGXNMSFK2702M_X20C14A3000000?channel=DF280120166594&style=1")
    html = driver.page_source.encode('utf-8')  # more sophisticated methods may be available
    # parse the response
    soup = BeautifulSoup(html, "lxml")
    # extract
    ## title
    header = soup.find("head")
    title = header.find("title").text
    ## description
    description = header.find("meta", attrs={"name": "description"})
    description_content = description.attrs['content'].text
    # output
    output = {"title": title, "description": description_content}
    # write the output as a json file
    with codecs.open(output_name, 'w', 'utf-8') as fout:
        json.dump(output, fout, indent=4, sort_keys=True, ensure_ascii=False)

if __name__ == '__main__':
    # arguments
    argvs = sys.argv
    ## check
    if len(argvs) != 2:
        print ("Usage: python scraping.py [url] [output]")
        exit()
    url = argvs[1]
    output_name = argvs[2]

    scraping(url, output_name)

