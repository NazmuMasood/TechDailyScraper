from bs4 import BeautifulSoup
import requests

owner = 'Beeboom'

html_text = requests.get('https://beebom.com').text
soup = BeautifulSoup(html_text, 'lxml')

titles = soup.find_all('div',class_ = 'td_module_10 td_module_wrap td-animation-stack bee-list')

for title in titles:
    contentTitle = title.find('div', class_ = 'item-details')
    aHref = contentTitle.find('a')
    image = title.find('img')
    
    print(owner)                   #owner
    print(aHref.text)              #content title
    print(aHref['href'])           #content url
    print(image['src']+'\n')       #content image url


