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
import os
import time, datetime
from models import Owner, Content
from connection import engine

### Creating session to make db queries
Session = sessionmaker(bind=engine)
session = Session()

freshStart = False
statement = 'SELECT contents_content.url FROM contents_content WHERE owner_id = 2 ORDER BY id DESC LIMIT 20'
results = session.execute(statement).scalars().all()
print("Previous records' results[] length: "+str(len(results)))
most_recent_url = 'null'
if len(results)>0:
    most_recent_url = results[0]
    print('\n---------Beebom last record : '+most_recent_url)
else:
    freshStart = True
    print('\nFresh Start!')


#Setting up options for the driver
option = Options()
option.add_argument("--disable-infobars")
# option.add_argument("start-maximized")
option.add_argument("--headless")
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
print('\nWebpage title: '+driver.title)

try:
    # Navigating to the 'Latest News' column
    newsColumnDivClass = "//div[@class='td-ss-main-content']"
    newsColumnDiv = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, newsColumnDivClass)))
    # print("'Latest News' column found!")
        
    try:
        # Getting all the 'article/content' rows in 'latest news' column
        contentRowDivClass = "//div[@class='td-ss-main-content']//div[@class='td_module_10 td_module_wrap td-animation-stack bee-list']"
        contentRowDivs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, contentRowDivClass)))
        # print("'Content' rows found!")
        print('contents[] length: '+str(len(contentRowDivs)))

        urlFound = False
        if freshStart:
            urlFound = True

        checkCount = 0
        while(urlFound is False and checkCount<=len(contentRowDivs)):
            checkCount+=1
            print('\nChecking for most recent url:\n'+most_recent_url)
            targetElem = driver.find_elements_by_xpath(".//a[contains(@href,'"+most_recent_url+"')]")
            if(len(targetElem)>0):
                print("Most recent url found in page, saving contents until that...\n")
                urlFound = True
                break
            else:
                # statement = 'DELETE FROM contents_content WHERE url = :val'
                # session.execute(statement, {'val':most_recent_url})
                # print('Deleted the orphan entry from db')
                # statement = 'SELECT contents_content.url FROM contents_content WHERE owner_id = 2 ORDER BY id DESC LIMIT 1'
                # results = session.execute(statement).scalars().all()
                if len(results)>0:
                    most_recent_url = results[checkCount]
                else:
                    break

        for contentRowDiv in contentRowDivs:
            if(contentRowDiv.find_element_by_class_name('entry-title').find_element_by_tag_name('a').get_attribute('href')==most_recent_url):
                break

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

print("Total "+str(len(content_urls))+" new content(s) found\n")
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
