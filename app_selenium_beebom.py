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
import os
import time


### Db connection
engine = create_engine('mysql+mysqldb://root:@127.0.0.1:3306/techdaily', connect_args={"init_command": "SET SESSION time_zone='+00:00'"}, echo=True)
### Creating session to make db queries
Session = sessionmaker(bind=engine)
session = Session()

statement = 'SELECT techdaily_content.url FROM techdaily_content WHERE owner_id = 2 ORDER BY id DESC LIMIT 1'
results = session.execute(statement).scalars().all()
beebom_recent_url_in_db = 'null'
if len(results)>0:
    beebom_recent_url_in_db = results[0]
print('---------Beebom last record : '+beebom_recent_url_in_db)


#Setting up options for the driver
option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
option.add_experimental_option('excludeSwitches', ['enable-logging'])

# Pass the argument 1 to allow and 2 to block on the "Allow Notifications" pop-up
option.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2 
})

#Creating the driver
driver = webdriver.Chrome(options=option, executable_path='./drivers/chromedriver.exe')

# --------!!!!!------ Populating techdaily_content table -------!!!!!!!!!--------
owner_names = ['Cnet','Beebom', 'Android Authority']
owner_urls = ['https://www.cnet.com', 'https://beebom.com', 'https://www.androidauthority.com']
owner_ids = [1, 2, 3]

content_titles = []
content_urls = []
content_authors = []
content_img_urls = []
content_pub_dates = []

#Loading the webpage
beebom = 1 #choosing beebom
owner_id = owner_ids[beebom] 
root_url = owner_urls[beebom]
driver.get(root_url+"/category/news")
print('Webpage title: '+driver.title)

try:
    # Navigating to the story 'Settings' button on the Create Facebook Stories page 
    newsColumnDivClass = "//div[@class='td-ss-main-content']"
    newsColumnDiv = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, newsColumnDivClass)))
    # print("'Latest News' column found!")
        
    try:
        # Navigating to the story 'Settings' button on the Create Facebook Stories page 
        contentRowDivClass = "//div[@class='td-ss-main-content']//div[@class='td_module_10 td_module_wrap td-animation-stack bee-list']"
        contentRowDivs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, contentRowDivClass)))
        # print("'Content' rows found!")
        print('contents[] length: '+str(len(contentRowDivs)))
        
        for contentRowDiv in contentRowDivs:
            # image url
            imageImg = contentRowDiv.find_element_by_class_name('entry-thumb')
            print(imageImg.get_attribute('src'))
            content_img_urls.append(imageImg.get_attribute('src'))

            # title
            titleH3 = contentRowDiv.find_element_by_class_name('entry-title')
            titleA = titleH3.find_element_by_tag_name('a')
            print(titleA.text)
            content_titles.append(titleA.text)

            # url
            print(titleA.get_attribute('href'))
            content_urls.append(titleA.get_attribute('href'))

            # author
            authorSpan = contentRowDiv.find_element_by_class_name('td-post-author-name')
            authorA = authorSpan.find_element_by_tag_name('a')
            print(authorA.text)
            content_authors.append(authorA.text)

            # pub_date
            pub_dateSpan = contentRowDiv.find_element_by_class_name('td-post-date')
            pub_dateTime = pub_dateSpan.find_element_by_tag_name('time')
            print(pub_dateTime.get_attribute('datetime')+'\n')
            content_pub_dates.append(pub_dateTime.get_attribute('datetime'))


    except TimeoutException:
        print("No 'contentRow' present on 'news' page")

except TimeoutException:
    print("No 'newsColumnDiv' present on 'news' page")

driver.quit()

# --------------------------------------------
# -------------------------------------------------
# --------------------------------------------

for content_author, content_pub_date, content_title, content_url, content_img_url in zip(
        reversed(content_authors), reversed(content_pub_dates), reversed(content_titles), reversed(content_urls), reversed(content_img_urls)):
    content = Content()
    content.owner_id = owner_id
    content.title = content_title
    content.author = content_author
    content.url = content_url
    content.img_url = content_img_url
    content.pub_date = content_pub_date
    # print(Content.__repr__)
    session.add(content)

session.commit()
session.close()
