from re import T
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column, ForeignKey, Sequence
from sqlalchemy.sql.sqltypes import DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
import requests

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

# --------!!!!!------ Populating techdaily_content table -------!!!!!!!!!--------
owner_names = ['Cnet','Beebom', 'Android Authority']
owner_urls = ['https://www.cnet.com', 'https://beebom.com', 'https://www.androidauthority.com']
owner_ids = [1, 2, 3]
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
    content = Content()
    content.owner_id = owner_id
    content.title = contentTitle
    content.author = contentAuthor
    content.url = owner_urls[android_authority]+title['href']
    content.img_url = image['src']
    # content.pub_date = 'June 17, 2021'
    session.add(content)

print('------------------------------------------')

areaMains =soup.find_all('a',class_ = 'sc-4kupz5-0 hzhPLs dark')
for areaMain in areaMains:   
    areaMainTitle = areaMain.find("div", {"class": "title-wrapper"}).text
    areaMainAuthor = areaMain.find("div", {"class": "g7i2b7-0 gqLaGq author-wrapper dark"}).text
    print(areaMainTitle)
    print(owner_urls[android_authority]+areaMain['href'])
    print(areaMainAuthor)
    print(areaMain.img['src']+'\n')
    content = Content()
    content.owner_id = owner_id
    content.title = areaMainTitle
    content.author = areaMainAuthor
    content.url = owner_urls[android_authority]+areaMain['href']
    content.img_url = areaMain.img['src']
    # content.pub_date = 'June 17, 2021'
    session.add(content)

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
        content = Content()
        content.owner_id = owner_id
        content.title = listTitle
        content.author = listAuthor[3:]
        content.url = owner_urls[android_authority]+listHref['href']
        content.img_url = listHref.img['src']
        # content.pub_date = 'June 17, 2021'
        session.add(content)
    flag = not flag
 
print('------------------------------------------')

session.commit()
session.close()
