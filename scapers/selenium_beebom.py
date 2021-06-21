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

#Loading the webpage
root_url = "https://beebom.com"
driver.get(root_url+"/category/news")
print('Webpage title: '+driver.title)

#   news column div         - <div class=td-ss-main-content>
#       content row div     -   <div class=td_module_10 td_module_wrap td-animation-stack bee-list >
# 
#       image div           -     <div class=td-module-thumb >
#       image a             -        <a class=td-image-wrap href="{contentLink}">
#       image img           -             <img class=entry-thumb src="{imageLink}" alt="{imageAltText}">
# 
#       title,author,date   -     <div class=item-details >
#       title h3            -       <h3 class=entry-title td-module-title >
#       title a             -           <a href="contentLink" title="{title}"> {title} </a>
#       short review div    -       <div class=td-excerpt review-excerpt > {review} </div>
#       author, date div    -       <div class=td-module-meta-info >
#       author span         -           <span class=td-post-author-name >
#       author a            -               <a href={authorLink} > {author} </a>
#       date span           -           <span class=td-post-date >
#       date time           -               <time class=entry-date updated td-module-date datetime="{some datetime ago}">

most_recent_url = "https://beebom.com/battlegrounds-mobile-india-sending-data-to-chinese-servers/" 

try:
    # Navigating to the story 'Settings' button on the Create Facebook Stories page 
    newsColumnDivClass = "//div[@class='td-ss-main-content']"
    newsColumnDiv = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, newsColumnDivClass)))
    print("'Latest News' column found!")
        
    try:
        # Navigating to the story 'Settings' button on the Create Facebook Stories page 
        contentRowDivClass = "//div[@class='td-ss-main-content']//div[@class='td_module_10 td_module_wrap td-animation-stack bee-list']"
        contentRowDivs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, contentRowDivClass)))
        print("'Content' rows found!")
        print('contents[] length: '+str(len(contentRowDivs)))

        for contentRowDiv in contentRowDivs:
            # image url
            imageImg = contentRowDiv.find_element_by_class_name('entry-thumb')
            print(imageImg.get_attribute('src'))

            # title
            titleH3 = contentRowDiv.find_element_by_class_name('entry-title')
            titleA = titleH3.find_element_by_tag_name('a')
            print(titleA.text)

            # url
            print(titleA.get_attribute('href'))

            # author
            authorSpan = contentRowDiv.find_element_by_class_name('td-post-author-name')
            authorA = authorSpan.find_element_by_tag_name('a')
            print(authorA.text)

            # pub_date
            pub_dateSpan = contentRowDiv.find_element_by_class_name('td-post-date')
            pub_dateTime = pub_dateSpan.find_element_by_tag_name('time')
            print(pub_dateTime.get_attribute('datetime')+'\n')


    except TimeoutException:
        print("No 'contentRow' present on 'news' page")

except TimeoutException:
    print("No 'newsColumnDiv' present on 'news' page")

# driver.quit()






# try:
#     # Navigating to the story 'Settings' button on the Create Facebook Stories page 
#     newsColumnDivClass = "//div[@class='td_module_10 td_module_wrap td-animation-stack bee-list']"
#     newsColumnDiv = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, newsColumnDivClass)))
#     print("newsColumnDiv found!")
        
# except TimeoutException:
#     print("No 'newsColumnDiv' present on 'news' page")