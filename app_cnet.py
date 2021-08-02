from re import T
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column, ForeignKey, Sequence
from sqlalchemy.sql.sqltypes import DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
import requests
from models import Content
from connection import engine

### Creating session to make db queries
Session = sessionmaker(bind=engine)
session = Session()

### ----- session code for that particular session goes here -----
statement = 'SELECT contents_content.url FROM contents_content WHERE owner_id = 1 ORDER BY id DESC LIMIT 1'
results = session.execute(statement).scalars().all()
cnet_recent_url_in_db = 'null'
if len(results)>0:
    cnet_recent_url_in_db = results[0]
print('---------Cnet last record : '+cnet_recent_url_in_db)

# --------!!!!!------ Populating techdaily_content table -------!!!!!!!!!--------
owner_names = ['Cnet','Beebom', 'Android Authority']
owner_urls = ['https://www.cnet.com', 'https://beebom.com', 'https://www.androidauthority.com']
owner_ids = [1, 2, 3]

content_titles = []
content_urls = []
content_authors = []
content_img_urls = []
content_pub_dates = []

cnet = 0 #choosing cnet
owner_id = owner_ids[cnet] 
html_text = requests.get(owner_urls[cnet]).text
soup = BeautifulSoup(html_text, 'lxml')
titles = soup.find_all('div',class_ = 'row item')
for title in titles:
    aHref = title.find('a')
    image = title.find('img')
    if ((owner_urls[cnet]+aHref['href'])==cnet_recent_url_in_db):
        print('------------MATCHING RECORD FOUND')
        break
    print(owner_id)                        #owner_id
    print(aHref.text)                      #content title
    print(owner_urls[cnet]+aHref['href'])  #content url
    print(image['src']+'\n')               #content image url
    content_titles.append(aHref.text)
    content_urls.append(owner_urls[cnet]+aHref['href'])
    content_img_urls.append(image['src'])
    # content = Content()
    # content.owner_id = owner_id
    # content.title = aHref.text
    # # content.author = 'John Doe'
    # content.url = owner_urls[cnet]+aHref['href']
    # content.img_url = image['src']
    # # content.pub_date = 'June 17, 2021'
    # session.add(content)

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
