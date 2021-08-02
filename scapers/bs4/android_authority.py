from bs4 import BeautifulSoup
import requests

owner = 'Android Authority'

url = 'https://www.androidauthority.com'
html_text = requests.get(url+'/news').text
soup = BeautifulSoup(html_text, 'lxml')

titles = soup.find_all('a',class_ = 'hv33vx-0 kcHKDA dark')
for title in titles:
    contentTitle = title.find("div", {"class": "title-wrapper"}).text
    contentAuthor = title.find("div", {"class": "g7i2b7-0 gqLaGq author-wrapper dark"}).text
    image = title.find('img')
    print(contentTitle)         #content title
    print(url+title['href'])    #content url
    print(contentAuthor)        #content author
    print(image['src']+'\n')    #content image url

print('------------------------------------------')

areaMains =soup.find_all('a',class_ = 'sc-4kupz5-0 hzhPLs dark')
for areaMain in areaMains:   
    areaMainTitle = areaMain.find("div", {"class": "title-wrapper"}).text
    areaMainAuthor = areaMain.find("div", {"class": "g7i2b7-0 gqLaGq author-wrapper dark"}).text
    print(areaMainTitle)
    print(url+areaMain['href'])
    print(areaMainAuthor)
    print(areaMain.img['src']+'\n')

print('------------------------------------------') 
 
lists =soup.find_all('div',class_ = 'sc-1aq13fn-0 jWWkOG')
flag = True
for list in lists:
    listTitle = list.find("div", {"class": "sc-1aq13fn-0 sc-1aq13fn-18 dbovrV jOqhtl title hover"}).text
    listHref = list.find("a", {"class": "sc-1aq13fn-0 sc-1aq13fn-12 sc-1aq13fn-19 sc-120h2xs-0 jWWkOG cctOPP kTuQdK iWkver"})
    listAuthor = list.find("div", {"class": "sc-1aq13fn-36 fivJsg black"}).text
    if(flag):  
        print(listTitle)
        print(url+listHref['href'])
        print(listAuthor[3:])
        print(listHref.img['src'+'\n']) 
    flag = not flag
 
print('------------------------------------------')


