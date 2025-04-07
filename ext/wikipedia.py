import requests
from bs4 import BeautifulSoup
def get_wiki(search):
    print("result:\n")
    req = requests.get(f"https://de.wikipedia.org/wiki/{search}")
    BeautifulSoup().find()
    soup = BeautifulSoup(req.content, "html.parser")
    
    found = soup.find_all("div", class_="mw-content-ltr")
    found = soup.find_all("a")
    links = {}
    for i in found:
        link,text = i.get("href"),i.get("contents")
        if not link: continue
        
        if not i.attrs['href']: continue
        links[str(i.attrs['href'])] = i.text
    print(links)
    

get_wiki("Minecraft")