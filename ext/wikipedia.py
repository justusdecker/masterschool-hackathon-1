import requests
from bs4 import BeautifulSoup
from ext.wiki_links import LINKS
from typing import Iterable
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

def get_wiki_text_exclude(link: str,words: Iterable[str]):
    text = get_wiki_text(link).split()
    for word in words:
        text.remove(word)
    return " ".join(text)
        

class WikipediaGame:
    def __init__(self):
        self.current_game = 0
        self.wc = 0
        self.current_page = ""
    def get_challenge_title(self):
        match self.current_game:
            case 0:
                return f"How many words has the {self.current_page} page?"
    def start_word_count(self):
        self.wc = get_wiki_text(LINKS[0]).count(" ") + 1
        self.current_page = LINKS[0].split("/")[-1]
    def end_word_count(self,inp:int) -> bool:
        if inp == self.wc: return 3
        elif inp < self.wc * 1.1 and inp > self.wc * 0.9: return 2
        elif inp < self.wc * 1.2 and inp > self.wc * 0.8: return 1
        else: return 0
        