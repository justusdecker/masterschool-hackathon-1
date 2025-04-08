import requests
from bs4 import BeautifulSoup
from ext.wiki_links import LINKS
from typing import Iterable
from random import randint
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
    soup = get_soup("https://de.wikipedia.org/wiki/" + link)
    return soup.text    #Remove HTML text. Returns only text

def get_wiki_links(link: str) -> list[str]:
    found = get_soup("https://de.wikipedia.org/wiki/" + link).find_all("a")
    links = []
    for i in found:
        
        href = str(i.attrs['href'] if "href" in i.attrs else False)
        if not href: continue
        
        if href.startswith("/wiki/") and \
            not href.endswith(".svg") and \
                not "wikipedia" in href.lower() and \
                    not ":" in href and \
                        not "%" in href:
            links.append(href.replace("/wiki/","")) #HREF Link & the text in the current element
    return links

def get_wiki_text_exclude(link: str,words: Iterable[str]):
    text = get_wiki_text(link).split()
    for word in words:
        text.remove(word)
    return " ".join(text)

print(get_wiki_text("Österreich"))
class WikipediaGame:
    def __init__(self):
        self.current_game = 0
        self.wc = 0
        self.current_page = ""
        self.remaining = 3
        self.points = 0
        
    def get_challenge_title(self):
        match self.current_game:
            case 0:
                return f"How many words has the {self.current_page} page?"
    def random_page(self):
        return LINKS[randint(0,len(LINKS)-1)]
    def start_word_count(self):
        self.remaining = 3
        page = self.random_page()
        self.wc = get_wiki_text(page).count(" ") + 1
        self.current_page = page.split("/")[-1]
    def reset_and_drive(self):
        new_path = get_wiki_links(self.current_page)
        title = ""
        while not title:
            title = new_path[randint(0,len(new_path)-1)]
            if len(title) + 29 < 42:
                LINKS.append(title)
            else:
                title = ""
    def end_word_count(self,inp:int) -> bool:
        
        self.remaining -= 1
        if inp == self.wc: return 3
        elif inp < self.wc * 1.1 and inp > self.wc * 0.9: return 2
        elif inp < self.wc * 1.2 and inp > self.wc * 0.8: return 1
        else: return 0
        