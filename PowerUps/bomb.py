import pygame,os
import settings
from PowerUp import *
class bomb(PowerUp):

    SCREEN = pygame.display.set_mode((600,500))
    EXPLOSION_COLORS = [(200,0,0), (255,0,0), (200,200,0), (255,255,0)]
    
    def __init__(self):
        super(bomb, self).__init__((255,0,0), (0,0), 20, 0,
                                               pygame.image.load(os.path.join('.', 'images', 'jayhawk.png')),
                                               'bomb')
        self.waiting = False
        self.explode = False
        self.explosionPos = (0,0)
        self.explosionList = []
        
    def effect(self):
        """bomb is waiting for fuse to go off"""
        self.waiting = True
    
    def effect_expire(self):
        """blow up causing the jayhawk to jump up"""
        if(self.waiting):
            self.explode = True
            self.explosionPos = (settings.jayhawk.x, settings.jayhawk.y)
            settings.jayhawk.jump()
            self.waiting = False
        if(self.explode):
            if(len(self.explosionList) > 30):
                del self.explosionList[:]
                self.explode = False
            else:
                index = 0
                for index, explodingbitElement in enumerate(self.explosionList):
                    explodingbitElement.updatePosition()
                    pygame.draw.circle(bomb.SCREEN, explodingbitElement.color,
                                       explodingbitElement.pos,explodingbitElement.radius)
                self.explosionList.append(exploding_bit(self.explosionPos, index))

class exploding_bit():
    """Code derived from https://www.youtube.com/watch?v=ukKDZkebRow"""
    def __init__(self, pos, magnitude):
        self.x = pos[0] + randint(-1*magnitude, magnitude)
        self.y = pos[1] + randint(-1*magnitude, magnitude)
        self.color = bomb.EXPLOSION_COLORS[randint(0,3)]
        self.radius = randint(1,10)
        
    def updatePosition(self):
        self.x -= 1

    @property
    def pos(self):
        return (int(self.x),int(self.y))
