import pygame,os
import settings
from random import randint
from PowerUp import *
from Jayhawk import *
class grenade_launcher(PowerUp):
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


        
        
    """def load_image(img_file_name):
        Return the loaded pygame image with the specified file name.
        This function looks for images in the game's images folder
        (./images/).  All images are converted before being returned to
        speed up blitting.
        Arguments:
        img_file_name: The file name (including its extension, e.g.
            '.png') of the required image, without a file path.
        
        file_name = os.path.join('.', 'images', img_file_name)
        img = pygame.image.load(file_name)
        img.convert()
        return img"""

class grenade:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_speed = randint(10,20)
        self.y_speed = -1 * randint(5,20)
        
    def updatePosition(self):
        self.gravity()
        self.y += self.y_speed
        self.x += self.x_speed

    def gravity(self):
        self.y_speed += Jayhawk.gravity_accel

    @property    
    def pos(self):
        return (self.x, self.y)