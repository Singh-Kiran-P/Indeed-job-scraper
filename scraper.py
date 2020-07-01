from bs4 import BeautifulSoup
import requests
import pandas as pd

pages=[]
titles=[]
locations=[]
companys=[]
links=[]
dates=[]

page_to_scape=1

search = "student"
location = 3500

for i in range(1,page_to_scape+1):
  url = ("https://be.indeed.com/jobs?q={}&l={}&sort=date&start={}0").format(search,location,i)
  pages.append(url)  


for url in pages:
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    
    for title in soup.find_all('h2'):    
        titles.append(title.getText()[2:-6])
        temp = title.findChild("a" , recursive=False).get('href')
        link = "https://be.indeed.com{}".format(temp)
        links.append(link)
        
    for location in soup.find_all('div',class_='recJobLoc'):    
        locations.append(location.get('data-rc-loc'))   
        
    for date in soup.find_all('span',class_="date"):
        dates.append(date.getText())
        
    for company in soup.find_all('span',{'class':"company"}):
        companys.append(company.text[1:])
                

data = {'Title':titles, 'Locations':locations,'Company':companys, 'Link': links,'Date':dates}
df = pd.DataFrame(data = data)
df.index+=1
df.to_excel('Jobs.xlsx')