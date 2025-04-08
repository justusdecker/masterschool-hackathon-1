import pygame as pg
from ext.wikipedia import WikipediaGame
from ext.animation import StarBouncing
from ext.ui_elements import InputElement
from time import perf_counter
from random import randint
pg.mixer.init()
MIXER = pg.mixer.Sound
class App:
    WIDTH = 1280
    HEIGHT = 720
    WINDOW = pg.display.set_mode((WIDTH,HEIGHT))
    pg.display.set_caption("Project: WIN")
    pg.display.set_icon(pg.image.load("logo.ico"))
    is_running = True
    CLK = pg.Clock()
    def __init__(self):
        self.input = InputElement()
        pg.font.init()
        self.wiki = WikipediaGame()
        self.font = pg.font.Font(pg.font.get_default_font(),40)
        self.star_texture = pg.transform.scale(pg.image.load("bin\\img\\star.png"),(48,48))
        self.nostar_texture = pg.transform.scale(pg.image.load("bin\\img\\nostar.png"),(48,48))
        
        self.start_bounce_animation_star1 = StarBouncing()
        self.start_bounce_animation_star2 = StarBouncing(25)
        self.start_bounce_animation_star3 = StarBouncing(50)
        
        self.animation_pos_1 = self.WIDTH
        self.animation_pos_2 = self.WIDTH
        self.ani_wait_1 = randint(0,3)
        self.ani_wait_2 = randint(0,3)
        self.delta_time = 0
        
    def run(self):
        self.wiki.start_word_count()
        pg.mixer.music.load("bin\\bgm.mp3")
        pg.mixer.music.play(-1)
        while self.is_running:
            dt = perf_counter()
            self.CLK.tick(30)
            match self.wiki.current_game:
                case 0:
                    self.word_guess()
            
            self.delta_time = perf_counter() - dt
            self.draw_stars()
            pg.display.update()
            self.check_events()
    def draw_background(self):
        if self.ani_wait_1 > 0:
            self.ani_wait_1 -= self.delta_time
        else:
            pg.draw.line(self.WINDOW,pg.Color("#e58f85"),(self.animation_pos_1,0),(self.animation_pos_1+(self.WIDTH*.4),self.HEIGHT),self.HEIGHT//32)
            self.animation_pos_1 -= self.delta_time * 1800
            if self.animation_pos_1+(self.WIDTH*.4) < 0: 
                self.animation_pos_1 = self.WIDTH
                self.ani_wait_1 = randint(0,4)
            
        if self.ani_wait_2 > 0:
            self.ani_wait_2 -= self.delta_time
        else:
            pg.draw.line(self.WINDOW,pg.Color("#e58f85"),(self.animation_pos_2,0),(self.animation_pos_2+(self.WIDTH*.4),self.HEIGHT),self.HEIGHT//16)
            self.animation_pos_2 -= self.delta_time * 2200
            if self.animation_pos_2+(self.WIDTH*.6) < 0: 
                self.animation_pos_2 = self.WIDTH
                self.ani_wait_2 = randint(0,4)
            
    def draw_stars(self):
        star_height = self.star_texture.get_height() *.5
            
        animations = (
            150 + (-star_height * self.start_bounce_animation_star2.update()),
            150 + star_height + (-star_height * self.start_bounce_animation_star1.update()),
            150 + (star_height) + (-star_height * self.start_bounce_animation_star3.update()))
        
        textures = [self.star_texture if self.wiki.remaining >= i + 1 else self.nostar_texture for i in range(3)]
        
        self.WINDOW.blit(textures[1],((self.WIDTH//2)-(self.star_texture.get_width()//2),animations[0]))
        self.WINDOW.blit(textures[0],((self.WIDTH//2)-((self.star_texture.get_width())*2),animations[1]))
        self.WINDOW.blit(textures[2],((self.WIDTH//2)+((self.star_texture.get_width())),animations[2]))
        
    def draw_input(self) -> None:
        pass
    
    def draw_title_bar(self) -> None:
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
        
        self.WINDOW.blit(
            title_font,
            (
                (self.WIDTH//2) - (title_font.get_width()//2),
                (self.HEIGHT//8) - (title_font.get_height()//2)
                ))
    def word_guess_predefined(self):
        pass
    def word_guess(self): 
        self.WINDOW.fill(pg.Color("#e85f58"),(0,0,self.WIDTH,self.HEIGHT))
        self.draw_background()
        self.draw_title_bar()
        self.input.draw(self.WINDOW,self.font,self.WIDTH//2 , self.HEIGHT//2)
        
    def more_or_less(self):
        self.WINDOW.fill(pg.Color("#e85f58"),(0,0,self.WIDTH // 2,self.HEIGHT))
        self.WINDOW.fill(pg.Color("#58c8e8"),(self.WIDTH // 2,0,self.WIDTH,self.HEIGHT))
        
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                self.is_running = False
            if self.wiki.current_game == 0:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN and self.input.get():
                        score = self.wiki.end_word_count(int(self.input.get()))
                        self.input.input = ""
                        if not self.wiki.remaining:
                            MIXER("bin\\nope.wav").play()
                            self.wiki.start_word_count()
                            self.wiki.reset_and_drive()
                        elif score:
                            MIXER("bin\\yay.wav").play()
                            self.wiki.points += score
                            self.wiki.start_word_count()
                            self.wiki.reset_and_drive()
                        else:
                            
                            MIXER("bin\\nope.wav").play()
                        
                    self.input.update_text(event.key)
if __name__ == "__main__":
    APP = App()
    APP.run()