import pygame,os
import settings
from Jayhawk import *
from PowerUp import *
class flea(PowerUp):
    
    def __init__(self):
        super(flea, self).__init__((255,255,0), (0,0), 20, 0,
                                               pygame.image.load(os.path.join('.', 'images', 'jayhawk.png')),
                                               'flea')
        
        self.sizeScale = settings.jayhawk.image.get_width()
        
    def effect(self):
        """shrinks the jayhawk down to flea size"""
        Jayhawk.gravity_accel = 0.5
        self.sizeScale -= 5
        if(self.sizeScale < 10):
            self.sizeScale = 10
        else:
            settings.jayhawk.set_image(pygame.image.load(os.path.join('.', 'images', 'jayhawk.png')), (self.sizeScale, self.sizeScale))            

    def effect_expire(self):
        """restores the jayhawk's size"""
        Jayhawk.gravity_accel = settings.gravity_accel
        self.sizeScale += 5
        if(self.sizeScale > 60):
            self.sizeScale = 60
        else:
            settings.jayhawk.set_image(pygame.image.load(os.path.join('.', 'images', 'jayhawk.png')), (self.sizeScale, self.sizeScale))           
