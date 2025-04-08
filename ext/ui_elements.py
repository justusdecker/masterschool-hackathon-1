from pygame import K_RETURN,K_BACKSPACE,Color,Font,Surface,draw,mouse,SRCALPHA

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
class ButtonElements:
    def __init__(self):
        self.set_texts("")
        self.pressed = [False,False,False]
    def draw_all(self,surf:Surface,font:Font,hw:int,hh:int):
        fh = font.get_height()
        position = (hh*2)//6
        for idx,text in enumerate(self.texts):
            wc = (len(text))*1.1*fh
            rendered_font = font.render(text,True,Color("#242424"))
            w , h = wc,fh * 1.1*2
            tmp = Surface((w,h),SRCALPHA)
            
            hover = self.get_hover((hw - (tmp.get_width()//2),(position*(idx+3)) - (tmp.get_height()//2),w,h))
            self.pressed[idx] = self.get_press(hover)
            draw.rect(tmp,Color("#fcfcfc") if hover else Color("#cccccc"),(0,0,w,h),border_radius=15)
            tmp.blit(rendered_font,((w//2) - (rendered_font.get_width()//2),(h // 2) - (rendered_font.get_height()//2)))
            surf.blit(tmp,(hw - (tmp.get_width()//2),(position*(idx+3)) - (tmp.get_height()//2)))
            
    def set_texts(self,texts:list[str]):
        self.texts = texts
    def get_hover(self,dest:list[int,int,int,int]):
        x,y,w,h = dest
        c,v = mouse.get_pos()
        return c > x and v > y and c < x + w and v < y + h
    def get_press(self,hov:bool) -> bool:
        return hov and mouse.get_pressed()[0]
            