from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column, ForeignKey, Sequence
from sqlalchemy.sql.sqltypes import DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
from models import Owner, Content
from connection import engine

### Db connection
# engine = create_engine('mysql+mysqldb://root:@127.0.0.1:3306/techdaily', connect_args={"init_command": "SET SESSION time_zone='+00:00'"}, echo=True)
# engine = create_engine('postgresql+psycopg2://postgres:@127.0.0.1:5432/techdaily', connect_args={"options": "-c timezone=utc"})
# Base.metadata.create_all(bind=engine)

### Creating session to make db queries
Session = sessionmaker(bind=engine)
session = Session()

### ----- session code for that particular session goes here -----

# --------!!!!!------ Populating techdaily_owner table -------!!!!!!!!!--------
owner_names = ['Cnet','Beebom', 'Android Authority']
owner_urls = ['https://www.cnet.com', 'https://beebom.com', 'https://www.androidauthority.com']
for owner_name, owner_url in zip(owner_names, owner_urls):
    owner = Owner()
    owner.name = owner_name
    owner.url = owner_url
    session.add(owner)

# --------!!!!!------ Populating techdaily_content table -------!!!!!!!!!--------
# owner_ids = [1, 2, 3]
# beebom = 1 #choosing beebom
# owner_id = owner_ids[beebom] 
# html_text = requests.get(owner_urls[beebom]).text
# soup = BeautifulSoup(html_text, 'lxml')
# titles = soup.find_all('div',class_ = 'td_module_10 td_module_wrap td-animation-stack bee-list')
# for title in titles:
#     contentTitle = title.find('div', class_ = 'item-details')
#     aHref = contentTitle.find('a')
#     image = title.find('img')
#     print(owner_id)                #owner_id
#     print(aHref.text)              #content title
#     print(aHref['href'])           #content link
#     print(image['src']+'\n')       #content image url
#     content = Content()
#     content.owner_id = owner_id
#     content.title = aHref.text
#     content.author = 'John Doe'
#     content.url = aHref['href']
#     content.img_url = image['src']
#     content.pub_date = 'June 17, 2021'
#     session.add(content)

session.commit()
session.close()
