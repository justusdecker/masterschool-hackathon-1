import pygame as pg
from ext.wikipedia import WikipediaGame
from ext.animation import StarBouncing, MenuAnimation
from ext.ui_elements import ButtonElements,Button
from ext.tileset_font import FONT,FONT_M
from time import perf_counter
from random import randint
pg.mixer.init()
MIXER = pg.mixer.Sound
class App:
    """
    This Class combines all the features and is used to todo both graphical & technical stuff
    More coming soon...
    """
    WIDTH = 1280
    HEIGHT = 720
    WINDOW = pg.display.set_mode((WIDTH,HEIGHT))
    pg.display.set_caption("Project: WIN")
    pg.display.set_icon(pg.image.load("logo.ico"))
    is_running = True
    CLK = pg.Clock()
    
    def __init__(self):
        pg.font.init()
        self.wiki = WikipediaGame()
        self.font = pg.font.Font(pg.font.get_default_font(),40)
        
        #Load textures
        self.star_texture = pg.transform.scale(pg.image.load("bin\\img\\star.png"),(48,48))
        self.nostar_texture = pg.transform.scale(pg.image.load("bin\\img\\nostar.png"),(48,48))
        self.logo = pg.image.load("logo.ico")
        
        #The Animations for the stars & score
        self.start_bounce_animation_star1 = StarBouncing()
        self.start_bounce_animation_star2 = StarBouncing(25)
        self.start_bounce_animation_star3 = StarBouncing(50)
        self.start_bounce_animation_score = StarBouncing(25)
        
        self.menu_to_game_animation = MenuAnimation()
        
        #The x position for the line animations
        self.animation_pos_1 = self.WIDTH
        self.animation_pos_2 = self.WIDTH
        
        #The sleep values for the line animations
        self.ani_wait_1 = randint(0,3)
        self.ani_wait_2 = randint(0,3)
        
        self.menu_btn = Button("PLAY")
        
        self.transition_image = None
        
        self.btns = ButtonElements()
        self.state = "menu"
        self.delta_time = 0
        
    def music_runner(self):
        pg.mixer.music.load("bin\\bgm.mp3")
        pg.mixer.music.play(-1)
        
    def run(self):
        self.btns.set_texts(self.wiki.start_word_count_predefined())    #Set the first challenge before enter the loop!
        
        self.music_runner()
        
        while self.is_running:
            dt = perf_counter()
            
            self.CLK.tick(60)
            match self.state:
                case "menu":
                    self.menu()
                case "game":
                    self.word_guess_predefined()
                    self.draw_stars()
                    self.draw_points()
                case "menu_to_game":
                    self.animate_menu_to_game()
            
            self.delta_time = perf_counter() - dt
            
            if not self.state == "menu_to_game": pg.display.update()
            self.check_events()
            
    def draw_points(self):
        title_font = FONT_M.render_text(str(self.wiki.points))
        self.WINDOW.blit(
            title_font,
            (
                (self.WIDTH//2) - (title_font.get_width()//2),
                (self.HEIGHT*.3) - (title_font.get_height()//2) + (title_font.get_height() * 0.5 * self.start_bounce_animation_score.update()*self.delta_time*50)
                ))
        
    def draw_background(self):
        self.WINDOW.fill(pg.Color("#e85f58"),(0,0,self.WIDTH,self.HEIGHT))
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
            150 + (-star_height * self.start_bounce_animation_star2.update()*self.delta_time*100),
            150 + star_height + (-star_height * self.start_bounce_animation_star1.update()*self.delta_time*100),
            150 + (star_height) + (-star_height * self.start_bounce_animation_star3.update()*self.delta_time*100))
        
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
        
        title_font = FONT.render_text(self.wiki.get_challenge_title())
        self.WINDOW.blit(
            title_font,
            (
                (self.WIDTH//2) - (title_font.get_width()//2),
                (self.HEIGHT//8) - (title_font.get_height()//2)
                ))
    
    def word_guess_predefined(self):
        self.draw_background()
        self.draw_title_bar()
 
        self.btns.draw_all(self.WINDOW,self.font,self.WIDTH//2 , self.HEIGHT//2)
        if any(self.btns.pressed):
            score = self.wiki.end_word_count_predefined(int(self.btns.texts[self.btns.pressed.index(True)]))
            self.btns.reset_press()
            if score:
                MIXER("bin\\yay.wav").play()
                self.wiki.points += score
                self.btns.set_texts(self.wiki.start_word_count_predefined())
                self.wiki.reset_and_drive()
            
            elif not self.wiki.remaining:
                MIXER("bin\\nope.wav").play()
                self.btns.set_texts(self.wiki.start_word_count_predefined())
                self.wiki.reset_and_drive()
            else:
                MIXER("bin\\nope.wav").play()
    
    def animate_menu_to_game(self):
        self.WINDOW.fill(pg.Color("#e58f58"))
        anim = self.menu_to_game_animation.update(self.delta_time)
        pos = self.HEIGHT*anim*-1

        self.WINDOW.blit(self.transition_image,(0,pos))
        pg.display.update()
        print(anim,)
        if anim > 1:
            self.state = "game"
    
    def menu(self):
        self.draw_background()
        self.WINDOW.blit(self.logo,((self.WIDTH//2)-(self.logo.get_width()//2),(self.HEIGHT*.2)-(self.logo.get_width()//2)))
        self.menu_btn.draw_all(self.WINDOW,self.WIDTH//2,self.HEIGHT//2)
        
        surf = self.WINDOW.copy()
        self.transition_image = pg.Surface((self.WIDTH,self.HEIGHT*2))
        self.transition_image.fill(pg.Color("#e85f58"))
        pg.draw.rect(
            self.transition_image,
            pg.Color("#fcfcfc"),
            ((self.WIDTH * .1),(self.HEIGHT//16)+self.HEIGHT,(self.WIDTH*.8),self.HEIGHT//8),
            border_radius=15
            )
        
        title_font = FONT.render_text(self.wiki.get_challenge_title())
        self.transition_image.blit(
            title_font,
            (
                (self.WIDTH//2) - (title_font.get_width()//2),
                (self.HEIGHT//8) - (title_font.get_height()//2)+self.HEIGHT
                ))
        self.transition_image.blit(surf,(0,0))

        if self.menu_btn.pressed:
            MIXER("bin\\yay.wav").play()
            self.btns.blocked = True
            self.state = "menu_to_game"
    def game_to_star_screen(self):
        pass
    def star_screen(self):
        pass
    def star_screen_to_game(self):
        pass
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                self.is_running = False
if __name__ == "__main__":
    APP = App()
    APP.run()