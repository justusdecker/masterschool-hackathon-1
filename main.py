"""http://de.wikipedia.org/wiki/Minecraft"""
import pygame as pg
from ext.wikipedia import WikipediaGame
class App:
    WIDTH = 1280
    HEIGHT = 720
    WINDOW = pg.display.set_mode((WIDTH,HEIGHT))
    is_running = True
   
    def __init__(self):
        self.inp = ""
        pg.font.init()
        self.wiki = WikipediaGame()
        self.font = pg.font.Font(pg.font.get_default_font(),40)
    def run(self):
        self.wiki.start_word_count()
        while self.is_running:
            match self.wiki.current_game:
                case 0:
                    self.word_guess()
            
            pg.display.update()
            self.check_events()
    def word_guess(self):
        hw,hh = self.WIDTH//2 , self.HEIGHT//2
        self.WINDOW.fill(pg.Color("#e85f58"),(0,0,self.WIDTH,self.HEIGHT))
        title_font = self.font.render(self.wiki.get_challenge_title(),True,pg.Color("#242424"))
        pg.draw.rect(self.WINDOW,pg.Color("#fcfcfc"),((self.WIDTH * .1),self.HEIGHT//16,(self.WIDTH*.8),self.HEIGHT//8),border_radius=15)
        
        self.WINDOW.blit(title_font,(hw - (title_font.get_width()//2),(self.HEIGHT//8) - (title_font.get_height()//2)))
        
        w_calc = (len(self.inp) if self.inp else 1)*1.1*self.font.get_height()
        pg.draw.rect(self.WINDOW,pg.Color("#fcfcfc"),(hw - (w_calc//2),hh - (self.font.get_height() * 1.1),w_calc,(self.font.get_height() * 1.1)*2),border_radius=15)
        font = self.font.render(self.inp,True,pg.Color("#242424"))
        
        self.WINDOW.blit(font,(hw - (font.get_width()//2),hh - (font.get_height()//2)))
    def more_or_less(self):
        self.WINDOW.fill(pg.Color("#e85f58"),(0,0,self.WIDTH // 2,self.HEIGHT))
        self.WINDOW.fill(pg.Color("#58c8e8"),(self.WIDTH // 2,0,self.WIDTH,self.HEIGHT))
    def check_events(self):
        shift = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    score = self.wiki.end_word_count(int(self.inp))
                    print(score)
                    self.wiki.start_word_count()
                if event.key == pg.K_BACKSPACE:
                    self.inp = self.inp[:-1]
                    continue
                try: char = chr(event.key)
                except ValueError: continue
                if char in "0123456789":
                    self.inp += char
if __name__ == "__main__":
    APP = App()
    APP.run()