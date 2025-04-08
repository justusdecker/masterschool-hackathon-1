import requests
from bs4 import BeautifulSoup
from typing import Iterable
from random import randint,shuffle
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
class WikipediaGame:
    def __init__(self):
        self.current_game = 1
        self.wc = 0
        self.current_page = ""
        self.remaining = 3
        self.points = 0
        self.links = {"Minecraft"}
        
    def get_challenge_title(self):
        match self.current_game:
            case 0:
                return f"How many words has the {self.current_page} page?"
            case 1:
                return f"Wordcounter in {self.current_page}"
    def random_page(self):
        return list(self.links)[randint(0,len(self.links)-1)]
    
    def start_word_count_predefined(self):
        self.remaining = 3
        page = self.random_page()
        self.wc = get_wiki_text(page).count(" ") + 1
        self.current_page = page.split("/")[-1]
        ret = [randint(self.wc//2,self.wc * 2) for i in range(2)]
        ret.append(self.wc)
        shuffle(ret)
        return ret
        
    def end_word_count_predefined(self,inp:int) -> bool:
        self.remaining -= 1
        if inp == self.wc: return (self.remaining + 1 if self.remaining else 1)
        else: return 0
    def reset_and_drive(self):
        new_path = get_wiki_links(self.current_page)
        
        for i in range(4096):
            if len(new_path) - 1 < i or len(self.links) >= 4096:
                break
            if len(new_path[i]) + 29 < 42:
                self.links.add(new_path[i])
        