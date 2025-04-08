from pygame import mixer
from random import randint
mixer.init()

def change_title():
    if mixer.music.get_busy(): return False
    mixer.music.load(f"bin\\bgm\\bgm{randint(0,2)}.mp3")
    mixer.music.play()
    return True