from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import Column, ForeignKey, Sequence
from sqlalchemy.sql.sqltypes import DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import by
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import os, re
import time, datetime
from models import Owner, Content
from connection import engine
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

### Creating session to make db queries
Session = sessionmaker(bind=engine)
session = Session()

freshStart = False
statement = 'SELECT contents_content.url FROM contents_content WHERE owner_id = 3 ORDER BY id DESC LIMIT 10'
results = session.execute(statement).scalars().all()
print("Previous records' results[] length: "+str(len(results)))
most_recent_url = 'null'
if len(results)>0:
    most_recent_url = results[0]
    print('\n---------Android Authority last record : '+most_recent_url+'\n')
else:
    freshStart = True
    print('\nFresh Start!')

# --------!!!!!------ Populating techdaily_content table -------!!!!!!!!!--------
owner_names = ['Cnet','Beebom', 'Android Authority']
owner_urls = ['https://www.cnet.com', 'https://beebom.com', 'https://www.androidauthority.com']
owner_ids = [1, 2, 3]

content_titles = []
content_urls = []
content_authors = []
content_img_urls = []
content_pub_dates = []
contentsRaw = []

#Loading the webpage
android_authority = 2 #choosing 'android authority'
owner_id = owner_ids[android_authority] 
root_url = owner_urls[android_authority]

# Get each content's datetime
def fetchContentPubDate(url):
    tmp_html_text = requests.get(url).text
    tmp_soup = BeautifulSoup(tmp_html_text, 'lxml')
    pub_date = tmp_soup.find("div", {"class": "sc-1aq13fn-0 sc-1aq13fn-16 hVEXKF lbeAGp date"}).text

    timeUnitCount = int(pub_date.split()[0][1:])
    unitOfTime = pub_date.split()[1][0:1]
    d = ''
    if unitOfTime=='h':
        d = currentTime - timedelta(hours=timeUnitCount, minutes=0)
    if unitOfTime=='m':
        d = currentTime - timedelta(hours=0, minutes=timeUnitCount)
    # print(d.strftime("%Y-%m-%d %H:%M:%S")+'\n')

    return d

# ----- ***** ----- Getting all contents with beautifulSoup
currentTime = datetime.today()
html_text = requests.get(root_url+'/news').text
soup = BeautifulSoup(html_text, 'lxml')

areaMains =soup.find_all('a',class_ = 'sc-4kupz5-0 hzhPLs dark')
for areaMain in areaMains:   
    areaMainTitle = areaMain.find("div", {"class": "title-wrapper"}).text
    areaMainAuthor = areaMain.find("div", {"class": "g7i2b7-0 gqLaGq author-wrapper dark"}).text
    areaMainPubDate = fetchContentPubDate(owner_urls[android_authority]+areaMain['href'])
    print(areaMainTitle)
    print(root_url+areaMain['href'])
    print(areaMainAuthor)
    print(areaMain.img['src'])
    print(areaMainPubDate)
    print('\n')

    content = Content()
    content.owner_id = owner_id
    content.title = areaMainTitle
    content.author = areaMainAuthor
    content.url = root_url+areaMain['href']
    content.img_url = areaMain.img['src']
    content.pub_date = areaMainPubDate
    contentsRaw.append(content)
    
print('------------------------------------------') 

titles = soup.find_all('a', class_ = 'hv33vx-0 kcHKDA dark')
for title in titles:
    contentTitle = title.find("div", {"class": "title-wrapper"}).text
    contentAuthor = title.find("div", {"class": "g7i2b7-0 gqLaGq author-wrapper dark"}).text
    image = title.find('img')
    contentPubDate = fetchContentPubDate(owner_urls[android_authority]+title['href'])
    print(contentTitle)
    print(root_url+title['href'])
    print(contentAuthor)
    print(image['src'])
    print(contentPubDate)
    print('\n')

    content = Content()
    content.owner_id = owner_id
    content.title = contentTitle
    content.author = contentAuthor
    content.url = root_url+title['href']
    content.img_url = image['src']
    content.pub_date = contentPubDate
    contentsRaw.append(content)

print('------------------------------------------')
 
lists =soup.find_all('a',class_ = 'sc-1aq13fn-0 sc-1aq13fn-12 sc-1aq13fn-19 sc-120h2xs-0 jWWkOG cctOPP kTuQdK iWkver')
print('lists[] length: '+str(len(lists))+'\n')
for list in lists:
    listTitle = list.find("div", {"class": "sc-1aq13fn-0 sc-1aq13fn-18 dbovrV jOqhtl title hover"}).text
    listHref = list
    listAuthor = list.find("div", {"class": "sc-1aq13fn-35 cwMVEv black"}).text
    listPubDate = list.find("div", {"class": "sc-1aq13fn-0 sc-1aq13fn-16 gPiACj lbeAGp"}).text
    print(listTitle)
    print(root_url+listHref['href'])
    print(listAuthor[3:])
    print(listHref.img['src']) 
    print(listPubDate+'\n')
    
    timeUnitCount = int(listPubDate.split()[0])
    unitOfTime = listPubDate.split()[1][0:1]
    d = ''
    if unitOfTime=='h':
        d = currentTime - timedelta(hours=timeUnitCount, minutes=0)
    if unitOfTime=='m':
        d = currentTime - timedelta(hours=0, minutes=timeUnitCount)
    print(d.strftime("%Y-%m-%d %H:%M:%S")+'\n')

    content = Content()
    content.owner_id = owner_id
    content.title = listTitle
    content.author = listAuthor[3:]
    content.url = root_url+listHref['href']
    content.img_url = listHref.img['src']
    content.pub_date = d
    contentsRaw.append(content)
 
print('------------------------------------------') 

urlFound = False
if freshStart:
    urlFound = True

checkCount = 0
while(urlFound is False and checkCount<=len(contentsRaw)):
    checkCount+=1
    print('\nChecking for most recent url:\n'+most_recent_url)
    print(most_recent_url[32:])
    targetElem = soup.find_all("a", href=re.compile(most_recent_url[32:]))
    if(len(targetElem)>0):
        print("Most recent url found in page, saving contents until that...\n")
        urlFound = True
        break
    else:
        # statement = 'DELETE FROM contents_content WHERE url = :val'
        # session.execute(statement, {'val':most_recent_url})
        # print('Deleted the orphan entry from db')
        # statement = 'SELECT contents_content.url FROM contents_content WHERE owner_id = 3 ORDER BY id DESC LIMIT 1'
        # results = session.execute(statement).scalars().all()
        if len(results)>0:
            most_recent_url = results[checkCount]
        else:
            break

# --------------------------------------------
# -------------------------------------------------
# --------------------------------------------

contents = []

for content in contentsRaw:
    if content.url == most_recent_url:
        break
    contents.append(content)

for content in reversed(contents):
    session.add(content)

print("Total "+str(len(contents))+" new content(s) found\n")

session.commit()
session.close()
