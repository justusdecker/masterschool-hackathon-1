
def ease_sine(x:float) -> float:
    return x**2 if x > 0 else (x*-1)**2
class StarBouncing:
    def __init__(self,start=0):
        self.flip = False
        self.x = 0
        self.frame = start
        self.speed = 0.01
        
    def frame_counter(self,c):
        self.frame += c
    def update(self):
        self.frame_counter([-1,1][self.flip])
        self.x = self.speed * self.frame

        if self.frame > 100 or self.frame < -100: self.flip = not self.flip
            
            
        #print((self.x**2),(self.x-1)**2)
        return ease_sine(self.x)