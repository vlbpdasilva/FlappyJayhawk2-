import pygame,os
import settings
from random import randint
from PowerUp import *
from Jayhawk import *
class grenade_launcher(PowerUp):
    """The most overpowered power up ever. A path of destruction lays in your wake. All pipes touched by grenades are 'destroyed'
    Attributes:
    SCREEN: draw stuff on screen
    GRENADE_LIST: list of grenades that have been launched
    GRENADE_LAUNCHED: detect when grenade is launched during jump so you don't spam grenades
    """
    SCREEN = pygame.display.set_mode((600,500))
    GRENADE_LIST = []
    GRENADE_LAUNCHED = False
    def __init__(self):
        super(grenade_launcher, self).__init__((0,0,0), (0,0), 20, 0,
                                               pygame.image.load(os.path.join('.', 'images', 'jayhawk.png')),
                                               'grenade_launcher')

    def effect(self):
        """Press up to launch a grenade"""
        #pygame.draw.rect(grenade_launcher.SCREEN, (0,255,0),(0,Jayhawk.Y,50,50), 0)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            #print 'boom'
            if(grenade_launcher.GRENADE_LAUNCHED == False):
                grenade_launcher.GRENADE_LIST.append(grenade(Jayhawk.X, Jayhawk.Y + 20))
            grenade_launcher.GRENADE_LAUNCHED = True
            #pygame.draw.rect(grenade_launcher.SCREEN, (0,0,0),(0,Jayhawk.Y,50,50), 0)
        else:
            grenade_launcher.GRENADE_LAUNCHED = False

        self.update_grenade()

    def effect_expire(self):
        """Let grenades respect the laws of existence and allow them to go off the screen before deconstructing them
        """
        self.update_grenade()

    def update_grenade(self):
        """In the grenade_list, update the positions of all grenades and detect collision
        Upon collision, 'destroy' pipes by moving them off the screen
        """
        for grenadeElement in grenade_launcher.GRENADE_LIST:
            grenadeElement.updatePosition()
            grenadeElement_rect = pygame.draw.circle(grenade_launcher.SCREEN, (0,0,0), grenadeElement.pos, 5, 0)
            if(grenadeElement.pos[1] > 500):
                grenade_launcher.GRENADE_LIST.remove(grenadeElement)
            else:    
                collision = settings.pipeManager.collision_pipe_num(grenadeElement_rect)
                if(collision):
                    grenade_launcher.GRENADE_LIST.remove(grenadeElement)
                    if(collision[1] == 'top'):
                        settings.pipeManager.pipeList[collision[0]].y_top = 0
                    else:
                        settings.pipeManager.pipeList[collision[0]].y_bot = 500

class grenade:
    """A circle that represents a grenade"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_speed = randint(10,20)
        self.y_speed = -1 * randint(5,20)
        
    def updatePosition(self):
        """update position of grenade based on its speed"""
        self.gravity()
        self.y += self.y_speed
        self.x += self.x_speed

    def gravity(self):
        """change speed based on gravity accel"""
        self.y_speed += settings.gravity_accel

    @property    
    def pos(self):
        """return pos"""
        return (int(self.x), int(self.y))
