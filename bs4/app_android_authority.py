from re import T
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column, ForeignKey, Sequence
from sqlalchemy.sql.sqltypes import DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
import requests
from models import Owner, Content
from connection import engine
from datetime import datetime, timedelta

# --------!!!!!------ Populating techdaily_content table -------!!!!!!!!!--------
owner_names = ['Cnet','Beebom', 'Android Authority']
owner_urls = ['https://www.cnet.com', 'https://beebom.com', 'https://www.androidauthority.com']
owner_ids = [1, 2, 3]

content_titles = []
content_urls = []
content_authors = []
content_img_urls = []
content_pub_dates = []

android_authority = 2 #choosing Android Authority
owner_id = owner_ids[android_authority] 
html_text = requests.get(owner_urls[android_authority]+'/news').text
soup = BeautifulSoup(html_text, 'lxml')

areaMains =soup.find_all('a',class_ = 'sc-4kupz5-0 hzhPLs dark')
for areaMain in areaMains:   
    areaMainTitle = areaMain.find("div", {"class": "title-wrapper"}).text
    areaMainAuthor = areaMain.find("div", {"class": "g7i2b7-0 gqLaGq author-wrapper dark"}).text
    print(areaMainTitle)
    print(owner_urls[android_authority]+areaMain['href'])
    print(areaMainAuthor)
    print(areaMain.img['src']+'\n')
    content_titles.append(areaMainTitle)
    content_urls.append(owner_urls[android_authority]+areaMain['href'])
    content_authors.append(areaMainAuthor)
    content_img_urls.append(areaMain.img['src'])
    # content = Content()
    # content.owner_id = owner_id
    # content.title = areaMainTitle
    # content.author = areaMainAuthor
    # content.url = owner_urls[android_authority]+areaMain['href']
    # content.img_url = areaMain.img['src']
    # # content.pub_date = 'June 17, 2021'
    # session.add(content)

print('------------------------------------------') 

titles = soup.find_all('a', class_ = 'hv33vx-0 kcHKDA dark')
for title in titles:
    contentTitle = title.find("div", {"class": "title-wrapper"}).text
    contentAuthor = title.find("div", {"class": "g7i2b7-0 gqLaGq author-wrapper dark"}).text
    image = title.find('img')
    print(contentTitle)
    print(owner_urls[android_authority]+title['href'])
    print(contentAuthor)
    print(image['src']+'\n')
    content_titles.append(contentTitle)
    content_urls.append(owner_urls[android_authority]+title['href'])
    content_authors.append(contentAuthor)
    content_img_urls.append(image['src'])
    # content = Content()
    # content.owner_id = owner_id
    # content.title = contentTitle
    # content.author = contentAuthor
    # content.url = owner_urls[android_authority]+title['href']
    # content.img_url = image['src']
    # # content.pub_date = 'June 17, 2021'
    # session.add(content)

print('------------------------------------------')
 
lists =soup.find_all('a',class_ = 'sc-1aq13fn-0 sc-1aq13fn-12 sc-1aq13fn-19 sc-120h2xs-0 jWWkOG cctOPP kTuQdK iWkver')
print('lists[] length: '+str(len(lists))+'\n')

currentTime = datetime.today()
print('current time: '+currentTime.strftime("%Y-%m-%d %H:%M:%S"))

# flag = True
for list in lists:
    listTitle = list.find("div", {"class": "sc-1aq13fn-0 sc-1aq13fn-18 dbovrV jOqhtl title hover"}).text
    # listHref = list.find("a", {"class": "sc-1aq13fn-0 sc-1aq13fn-12 sc-1aq13fn-19 sc-120h2xs-0 jWWkOG cctOPP kTuQdK iWkver"})
    listHref = list
    listAuthor = list.find("div", {"class": "sc-1aq13fn-35 cwMVEv black"}).text
    listPubDate = list.find("div", {"class": "sc-1aq13fn-0 sc-1aq13fn-16 gPiACj lbeAGp"}).text
    # if(flag):  
    print(listTitle)
    print(owner_urls[android_authority]+listHref['href'])
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

    content_titles.append(listTitle)
    content_urls.append(owner_urls[android_authority]+listHref['href'])
    content_authors.append(listAuthor[3:])
    content_img_urls.append(listHref.img['src'])
    content_pub_dates.append(listPubDate)
    # content = Content()
    # content.owner_id = owner_id
    # content.title = listTitle
    # content.author = listAuthor[3:]
    # content.url = owner_urls[android_authority]+listHref['href']
    # content.img_url = listHref.img['src']
    # # content.pub_date = 'June 17, 2021'
    # session.add(content)
    # flag = not flag
 
print('------------------------------------------')


### Creating session to make db queries
Session = sessionmaker(bind=engine)
session = Session()

### ----- session code for that particular session goes here -----

# for content_author, content_pub_date, content_title, content_url, content_img_url in zip(
#         reversed(content_authors), reversed(content_pub_dates), reversed(content_titles), \
#             reversed(content_urls), reversed(content_img_urls)):
#     content = Content()
#     content.owner_id = owner_id
#     content.title = content_title
#     content.author = content_author
#     content.url = content_url
#     content.img_url = content_img_url
#     content.pub_date = content_pub_date
#     session.add(content)

# session.commit()
session.close()
