from pygame import Surface,image,transform,SRCALPHA
from string import digits,ascii_lowercase

class Font:
    surface : Surface = image.load("bin\\tilesets\\char_set.png")
    chars : str = digits + ascii_lowercase + "!?*\\/().:-+,"

    def __init__(self, 
                 char_size: int = 512,
                 draw_size: int = 30
                 ) -> None:
        self.size : int = draw_size
        self.char_array = []
        for char in range(len(self.chars)):
            surf = Surface((char_size,char_size),SRCALPHA)
            surf.blit(self.surface,(-char*char_size,0))
            surf = transform.scale(surf,(self.size,self.size))
            self.char_array.append(surf)

    def render_text(self,text:str) -> Surface:
        surf = Surface((self.size*len(text),self.size),SRCALPHA)
        for index,char in enumerate(text):
            if char.isspace(): continue
            if char in "{[": char = "("
            if char in "]}": char = ")"
            char = char.lower()
            if char not in self.chars: char = "*"
            surf.blit(self.char_array[self.chars.index(char)],(index*self.size,0))
        return surf
FONT = Font()
FONT_M = Font(draw_size=60)