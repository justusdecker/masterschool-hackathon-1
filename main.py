"""http://de.wikipedia.org/wiki/Minecraft"""
import pygame as pg
class App:
    WIDTH = 1280
    HEIGHT = 720
    WINDOW = pg.display.set_mode((WIDTH,HEIGHT))
    is_running = True
    def __init__(self):
        pass
    def run(self):
        while self.is_running:
            self.WINDOW.fill(pg.Color("#e85f58"),(0,0,self.WIDTH // 2,self.HEIGHT))
            self.WINDOW.fill(pg.Color("#58c8e8"),(self.WIDTH // 2,0,self.WIDTH,self.HEIGHT))
            
            pg.display.update()
            self.check_events()
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
if __name__ == "__main__":
    APP = App()
    APP.run()