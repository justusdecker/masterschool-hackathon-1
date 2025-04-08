from pygame import mixer
from random import randint
mixer.init()
class MusicWrapper:
    def __init__(self,app):
        self.app = app
    def update(self):
        while self.app.is_running:
            self.change_title()
    def change_title(self):
        if mixer.music.get_busy(): return False
        mixer.music.load(f"bin\\bgm\\bgm{randint(0,2)}.mp3")
        mixer.music.play()
        return True