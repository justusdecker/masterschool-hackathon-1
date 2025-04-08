from pygame import K_RETURN,K_BACKSPACE,Color,Font,Surface,draw,mouse

class InputElement:
    def __init__(self, ):
        self.input = ""
        self.allowed = "0123456789"
    def draw(self,surf:Surface,font:Font,w:int,h:int): 
        draw_color = Color("#242424") if self.input else Color("#484848")
        width_calculation = (len(self.input) if self.input else 19)*1.1*font.get_height()
        rendered_font = font.render(self.input if self.input else "Enter your choice",True,draw_color)
        draw.rect(surf,Color("#fcfcfc"),(w - (width_calculation//2),h - (font.get_height() * 1.1),width_calculation,(font.get_height() * 1.1)*2),border_radius=15)
        surf.blit(rendered_font,(w - (rendered_font.get_width()//2),h - (rendered_font.get_height()//2)))
        
    def update_text(self,char:str):
        if char == K_BACKSPACE:
            self.input = self.input[:-1]
            return
        try: char = chr(char)
        except ValueError: return
        if char in self.allowed:
            self.input += char
    def get(self) -> str:
        return self.input
class ButtonElement:
    def __init__(self,
                 pos: tuple[int,int],
                 dest: tuple[int,int]):
        self.pos = pos
        self.dest = dest
        self.pressed = False
    def update(self):
        pos = mouse.get_pos()
        