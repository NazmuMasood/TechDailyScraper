from re import T
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column, ForeignKey, Sequence
from sqlalchemy.sql.sqltypes import DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
import requests

owner_names = ['Cnet','Beebom', 'Android Authority']
owner_urls = ['https://www.cnet.com', 'https://beebom.com', 'https://www.androidauthority.com']
owner_ids = [1, 2, 3]
content_owner_ids = []
content_titles = []
content_urls = []
content_img_urls = []
content_pub_dates = []

# scraping beebom
beebom = 1
owner_id = owner_ids[beebom] # for beebom its 2
html_text = requests.get(owner_urls[beebom]).text
soup = BeautifulSoup(html_text, 'lxml')
titles = soup.find_all('div',class_ = 'td_module_10 td_module_wrap td-animation-stack bee-list')
for title in titles:
    contentTitle = title.find('div', class_ = 'item-details')
    aHref = contentTitle.find('a')
    image = title.find('img')
    print(owner_id)                #owner_id
    print(aHref.text)              #content title
    print(aHref['href'])           #content link
    print(image['src']+'\n')       #content image url
    content_owner_ids.append(owner_id)
    content_titles.append(aHref.text)
    content_urls.append(aHref['href'])
    content_img_urls.append(image['src'])
    content_pub_dates.append('June 17, 2021')
print('----------------Scraping completed------------')
print('content_titles length: '+str(len(content_titles)))

# scraping cnet
# ......

# scraping android authority
# ......

Base = declarative_base()

### Owner model
class Owner(Base):
    __tablename__ = 'techdaily_owner'
    # id = Column(Integer, Sequence('owner_id_seq'), primary_key=True)
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    url = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())
    # created_at = Column(DateTime(timezone=True), server_default=func.now())
    # updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return "<Owner(id='%d', name='%s', url='%s', created_at='%s', updated_at='%s')>" % ( 
            self.id, self.name, self.url, self.created_at, self.updated_at)

### Content model
class Content(Base):
    __tablename__ = 'techdaily_content'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('techdaily_owner.id', ondelete="CASCADE"))
    url =  Column(String(300), nullable=False, unique=True)
    title = Column(String(200), nullable=False)
    author = Column(String(200), nullable=True)
    pub_date = Column(String(50), nullable=True)
    img_url = Column(String(200), nullable=True)   
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())
    
    def __repr__(self):
        return "<Content(id='%d', owner_id='%d', url='%s', title='%s', author='%s', pub_date='%s', img_url='%s', created_at='%s', updated_at='%s')>" % ( 
            self.id, self.owner_id, self.url, self.title, self.author, self.pub_date, self.img_url, self.created_at, self.updated_at)

### Db connection
engine = create_engine('mysql+mysqldb://root:@127.0.0.1:3306/techdaily', echo=True)
# Base.metadata.create_all(bind=engine)

### Creating session to make db queries
Session = sessionmaker(bind=engine)
session = Session()

### ----- session code for that particular session goes here -----

# --------!!!!!------ Populating techdaily_owner table -------!!!!!!!!!--------
owner_names = ['Cnet','Beebom', 'Android Authority']
owner_urls = ['https://www.cnet.com', 'https://beebom.com', 'https://www.androidauthority.com']
# for owner_name, owner_url in zip(owner_names, owner_urls):
#     owner = Owner()
#     owner.name = owner_name
#     owner.url = owner_url
#     session.add(owner)

# --------!!!!!------ Populating techdaily_content table -------!!!!!!!!!--------
for content_owner_id, content_title, content_url, content_img_url, content_pub_date in zip(
            content_owner_ids, content_titles, content_urls, content_img_urls, content_pub_dates):
    content = Content()
    content.owner_id = content_owner_id
    content.title = content_title
    content.author = 'John Doe'
    content.url = content_url
    content.img_url = content_img_url
    content.pub_date = content_pub_date
    session.add(content)

session.commit()
session.close()

