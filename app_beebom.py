from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import Column, ForeignKey, Sequence
from sqlalchemy.sql.sqltypes import DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
import requests
from models import Owner, Content

### Db connection
engine = create_engine('mysql+mysqldb://root:@127.0.0.1:3306/techdaily', connect_args={"init_command": "SET SESSION time_zone='+00:00'"}, echo=True)

### Creating session to make db queries
Session = sessionmaker(bind=engine)
session = Session()

### ----- session code for that particular session goes here -----

statement = 'SELECT techdaily_content.url FROM techdaily_content WHERE owner_id = 2 ORDER BY id DESC LIMIT 1'
results = session.execute(statement).scalars().all()
beebom_recent_url_in_db = 'null'
if len(results)>0:
    beebom_recent_url_in_db = results[0]
print('---------Beebom last record : '+beebom_recent_url_in_db)
# statement = select(Content.url).filter_by(owner_id=2)
# results = session.execute(statement).scalars().all()
# for result in results:
#     print(result)
#     print('\n')
# print('list length: '+str(len(results)))

# --------!!!!!------ Populating techdaily_content table -------!!!!!!!!!--------
owner_names = ['Cnet','Beebom', 'Android Authority']
owner_urls = ['https://www.cnet.com', 'https://beebom.com', 'https://www.androidauthority.com']
owner_ids = [1, 2, 3]

content_titles = []
content_urls = []
content_authors = []
content_img_urls = []
content_pub_dates = []

beebom = 1 #choosing beebom
owner_id = owner_ids[beebom] 
html_text = requests.get(owner_urls[beebom]).text
soup = BeautifulSoup(html_text, 'lxml')
titles = soup.find_all('div',class_ = 'td_module_10 td_module_wrap td-animation-stack bee-list')
for title in titles:
    contentTitle = title.find('div', class_ = 'item-details')
    aHref = contentTitle.find('a')
    image = title.find('img')
    if (aHref['href']==beebom_recent_url_in_db):
        print('------------MATCHING RECORD FOUND')
        break
    print(owner_id)                #owner_id
    print(aHref.text)              #content title
    print(aHref['href'])           #content link
    print(image['src']+'\n')       #content image url
    content_titles.append(aHref.text)
    content_urls.append(aHref['href'])
    content_img_urls.append(image['src'])
    # content = Content()
    # content.owner_id = owner_id
    # content.title = aHref.text
    # # content.author = 'John Doe'
    # content.url = aHref['href']
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
    print(Content.__repr__)
    session.add(content)

session.commit()
session.close()
