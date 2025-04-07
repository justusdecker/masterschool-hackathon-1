import requests
from bs4 import BeautifulSoup

"""
WFAPI - Wikipedia fetching API
(c) 2025 - Justus Decker
"""

def get_soup(link:str) -> BeautifulSoup:
    """
    Get the Website content with HTML Tags
    """
    return BeautifulSoup(
        requests.get(f"{link}").content, 
        "html.parser"
        )
def get_wiki_text(link: str) -> str:
    soup = get_soup(link)
    return soup.text    #Remove HTML text. Returns only text

def get_wiki_links(link: str) -> list[str,str]:
    soup = get_soup(link)
    found = soup.find_all("a")
    links = []
    for i in found:
        link = i.get("href")
        
        if not link: continue
        if not i.attrs['href']: continue
        
        links.append((str(i.attrs['href']),i.text)) #HREF Link & the text in the current element
        
    return links

print(get_wiki_text("https://de.wikipedia.org/wiki/Minecraft"))