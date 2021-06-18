from bs4 import BeautifulSoup
import requests
owner = "Cnet"
url = 'https://www.cnet.com'
html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'lxml')
titles = soup.find_all('div',class_ = 'row item')

for title in titles:
    aHref = title.find('a')
    image = title.find('img')
    
    print(owner) 
    print(aHref.text) #content title
    print(url+aHref['href']) #content url
    print(image['src']+'\n') #content img url
    



