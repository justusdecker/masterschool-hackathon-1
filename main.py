import pygame as pg
from ext.wikipedia import WikipediaGame
from ext.animation import StarBouncing
from time import perf_counter
pg.mixer.init()
MIXER = pg.mixer.music
class App:
    WIDTH = 1280
    HEIGHT = 720
    WINDOW = pg.display.set_mode((WIDTH,HEIGHT))
    is_running = True
    CLK = pg.Clock()
    def __init__(self):
        self.inp = ""
        pg.font.init()
        self.wiki = WikipediaGame()
        self.font = pg.font.Font(pg.font.get_default_font(),40)
        self.star_texture = pg.transform.scale(pg.image.load("bin\\img\\star.png"),(48,48))
        self.nostar_texture = pg.transform.scale(pg.image.load("bin\\img\\nostar.png"),(48,48))
        
        self.start_bounce_animation_star1 = StarBouncing()
        self.start_bounce_animation_star2 = StarBouncing(25)
        self.start_bounce_animation_star3 = StarBouncing(50)
        self.delta_time = 0
        
    def run(self):
        self.wiki.start_word_count()
        while self.is_running:
            dt = perf_counter()
            self.CLK.tick(30)
            match self.wiki.current_game:
                case 0:
                    self.word_guess()
            self.delta_time = perf_counter() - dt
            self.WINDOW.blit(self.star_texture if self.wiki.remaining >= 2 else self.nostar_texture,((self.WIDTH//2)-(self.star_texture.get_width()//2),150+(-self.star_texture.get_height()*.5*self.start_bounce_animation_star2.update())))
            self.WINDOW.blit(self.star_texture if self.wiki.remaining >= 1 else self.nostar_texture,((self.WIDTH//2)-((self.star_texture.get_width())*2),150+(self.star_texture.get_height()*.5)+(-self.star_texture.get_height()*.5*self.start_bounce_animation_star1.update())))
            self.WINDOW.blit(self.star_texture if self.wiki.remaining >= 3 else self.nostar_texture,((self.WIDTH//2)+((self.star_texture.get_width())),150+(self.star_texture.get_height()*.5)+(-self.star_texture.get_height()*.5*self.start_bounce_animation_star3.update())))
            
            pg.display.update()
            self.check_events()
    def draw_input(self) -> None:
        pass
    def draw_title_bar(self,title:str) -> None:
        pg.draw.rect(
            self.WINDOW,
            pg.Color("#fcfcfc"),
            ((self.WIDTH * .1),self.HEIGHT//16,(self.WIDTH*.8),self.HEIGHT//8),
            border_radius=15
            )
        title_font = self.font.render(
            self.wiki.get_challenge_title(),
            True,
            pg.Color("#242424")
            )
        self.WINDOW.blit(title_font,((self.WIDTH//2) - (title_font.get_width()//2),(self.HEIGHT//8) - (title_font.get_height()//2)))
    def word_guess(self):
        hw,hh = self.WIDTH//2 , self.HEIGHT//2
        if self.inp:
            input_draw = self.inp
            draw_color = pg.Color("#242424")
        else:
            input_draw = "Enter your choice"
            draw_color = pg.Color("#484848")
            
        self.WINDOW.fill(
            pg.Color("#e85f58"),
            (0,0,self.WIDTH,self.HEIGHT)
            )
        
        self.draw_title_bar(input_draw)
        
        w_calc = (len(input_draw) if input_draw else 1)*1.1*self.font.get_height()
        
        pg.draw.rect(self.WINDOW,pg.Color("#fcfcfc"),(hw - (w_calc//2),hh - (self.font.get_height() * 1.1),w_calc,(self.font.get_height() * 1.1)*2),border_radius=15)
        
        font = self.font.render(input_draw,True,draw_color)
        
        self.WINDOW.blit(font,(hw - (font.get_width()//2),hh - (font.get_height()//2)))
    def more_or_less(self):
        self.WINDOW.fill(pg.Color("#e85f58"),(0,0,self.WIDTH // 2,self.HEIGHT))
        self.WINDOW.fill(pg.Color("#58c8e8"),(self.WIDTH // 2,0,self.WIDTH,self.HEIGHT))
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN and self.inp:
                    score = self.wiki.end_word_count(int(self.inp))
                    print(score)
                    if not self.wiki.remaining:
                        MIXER.load("bin\\nope.wav")
                        MIXER.play()
                        self.inp = ""
                        self.wiki.start_word_count()
                    elif score:
                        MIXER.load("bin\\yay.wav")
                        MIXER.play()
                        self.wiki.points += score
                        self.inp = ""
                        self.wiki.start_word_count()
                    else:
                        MIXER.load("bin\\nope.wav")
                        MIXER.play()
                    
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