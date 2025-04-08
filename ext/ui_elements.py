from pygame import Color,Font,Surface,draw,mouse,SRCALPHA
from ext.tileset_font import FONT
class Button:
    def __init__(self,text:str):
        self.text = text
        self.reset_press()
        self.blocked = False
    def reset_press(self):
        self.pressed = False
    def draw_only(self,surf:Surface,hw,hh):
        fh = FONT.char_array[0].get_height()
        wc = (len(str(self.text)))*1.1*fh
        rendered_font = FONT.render_text(str(self.text))
        w , h = wc,fh * 1.1*2
        tmp = Surface((w,h),SRCALPHA)
        draw.rect(tmp,Color("#fcfcfc"),(0,0,w,h),border_radius=15)
        tmp.blit(rendered_font,((w//2) - (rendered_font.get_width()//2),(h // 2) - (rendered_font.get_height()//2)))
        surf.blit(tmp,(hw - (tmp.get_width()//2),hh - (tmp.get_height()//2)))
    def draw_all(self,surf:Surface,hw:int,hh:int):
        fh = FONT.char_array[0].get_height()


        wc = (len(str(self.text)))*1.1*fh
        rendered_font = FONT.render_text(str(self.text))
        w , h = wc,fh * 1.1*2
        tmp = Surface((w,h),SRCALPHA)
        hover = False
        if not self.blocked:

            hover = self.get_hover((hw - (tmp.get_width()//2),hh - (tmp.get_height()//2),w,h))
            self.pressed = self.get_press(hover)
                
            
            draw.rect(tmp,Color("#fcfcfc") if hover else Color("#cccccc"),(0,0,w,h),border_radius=15)
            tmp.blit(rendered_font,((w//2) - (rendered_font.get_width()//2),(h // 2) - (rendered_font.get_height()//2)))
            surf.blit(tmp,(hw - (tmp.get_width()//2),hh - (tmp.get_height()//2)))
        self.blocked = mouse.get_pressed()[0]
    def set_texts(self,texts:list[str]):
        self.texts = texts
    def get_hover(self,dest:list[int,int,int,int]):
        x,y,w,h = dest
        c,v = mouse.get_pos()
        return c > x and v > y and c < x + w and v < y + h
    def get_press(self,hov:bool) -> bool:
        return hov and mouse.get_pressed()[0]
class ButtonElements:
    def __init__(self):
        self.set_texts("")
        self.reset_press()
        self.blocked = False
    def reset_press(self):
        self.pressed = [False,False,False]
    def draw_all(self,surf:Surface,font:Font,hw:int,hh:int):
        fh = FONT.char_array[0].get_height()
        position = (hh*2)//6

        for idx,text in enumerate(self.texts):
            wc = (len(str(text)))*1.1*fh
            rendered_font = FONT.render_text(str(text))
            w , h = wc,fh * 1.1*2
            tmp = Surface((w,h),SRCALPHA)
            hover = False
            if not self.blocked:
                hover = self.get_hover((hw - (tmp.get_width()//2),(position*(idx+3)) - (tmp.get_height()//2),w,h))
                self.pressed[idx] = self.get_press(hover)
                
            
            draw.rect(tmp,Color("#fcfcfc") if hover else Color("#cccccc"),(0,0,w,h),border_radius=15)
            tmp.blit(rendered_font,((w//2) - (rendered_font.get_width()//2),(h // 2) - (rendered_font.get_height()//2)))
            surf.blit(tmp,(hw - (tmp.get_width()//2),(position*(idx+3)) - (tmp.get_height()//2)))
        self.blocked = mouse.get_pressed()[0]
    def set_texts(self,texts:list[str]):
        self.texts = texts
    def get_hover(self,dest:list[int,int,int,int]):
        x,y,w,h = dest
        c,v = mouse.get_pos()
        return c > x and v > y and c < x + w and v < y + h
    def get_press(self,hov:bool) -> bool:
        return hov and mouse.get_pressed()[0]
            