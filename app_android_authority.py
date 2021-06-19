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

### Db connection
engine = create_engine('mysql+mysqldb://root:@127.0.0.1:3306/techdaily', connect_args={"init_command": "SET SESSION time_zone='+00:00'"}, echo=True)
# Base.metadata.create_all(bind=engine)

### Creating session to make db queries
Session = sessionmaker(bind=engine)
session = Session()

### ----- session code for that particular session goes here -----

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
 
lists =soup.find_all('div',class_ = 'sc-1aq13fn-0 jWWkOG')
flag = True
for list in lists:
    listTitle = list.find("div", {"class": "sc-1aq13fn-0 sc-1aq13fn-18 dbovrV jOqhtl title hover"}).text
    listHref = list.find("a", {"class": "sc-1aq13fn-0 sc-1aq13fn-12 sc-1aq13fn-19 sc-120h2xs-0 jWWkOG cctOPP kTuQdK iWkver"})
    listAuthor = list.find("div", {"class": "sc-1aq13fn-36 fivJsg black"}).text
    if(flag):  
        print(listTitle)
        print(owner_urls[android_authority]+listHref['href'])
        print(listAuthor[3:])
        print(listHref.img['src']+'\n') 
        content_titles.append(listTitle)
        content_urls.append(owner_urls[android_authority]+listHref['href'])
        content_authors.append(listAuthor[3:])
        content_img_urls.append(listHref.img['src'])
        # content = Content()
        # content.owner_id = owner_id
        # content.title = listTitle
        # content.author = listAuthor[3:]
        # content.url = owner_urls[android_authority]+listHref['href']
        # content.img_url = listHref.img['src']
        # # content.pub_date = 'June 17, 2021'
        # session.add(content)
    flag = not flag
 
print('------------------------------------------')

for content_title, content_url, content_img_url in zip(
        reversed(content_titles), reversed(content_urls), reversed(content_img_urls)):
    content = Content()
    content.owner_id = owner_id
    content.title = content_title
    # content.author = 'John Doe'
    content.url = content_url
    content.img_url = content_img_url
    # content.pub_date = content_pub_date
    session.add(content)

session.commit()
session.close()
