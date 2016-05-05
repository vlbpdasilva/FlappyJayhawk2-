import pygame
from Jayhawk import *

#import powerups
from PowerUp import *
from PowerUps import * 

class PowerUpManager():

    POWERUPS_LOADED_STR = PowerUp.POWERUPS_LOADED_CLEAN.split(' ')

    SCREEN = pygame.display.set_mode((600,500))

    def __init__(self):
        #powerups included in the PowerUps folder
        #self.powerupLoadedList = []
        #powerups just floating there
        self.powerupList = []
        #powerups that have been picked up
        self.powerupObtainedList = []
        
        for powerupElement in PowerUpManager.POWERUPS_LOADED_STR:
            module = __import__('PowerUps.' + powerupElement, fromlist=['uselessplaceholder'])
            class_ = getattr(module, powerupElement)
            powerup = class_()
            #self.powerupLoadedList.append(powerup)
            #test
            self.powerupObtainedList.append(powerup)
                            
        print PowerUp.POWERUPS_LOADED_CLEAN
        print PowerUp.POWERUPS_LOADED#.split( )[2].split('\'')

    def spawn_management(self):        
        #spawn powerup at random
        if(randint(0, 100) == 1):
            #select a random index out of the POWERUPS_LOADED_STR
            random_select = randint(0, len(self.POWERUPS_LOADED_STR) - 1)
            #instantiate the powerup from the random index of POWERUPS_LOADED_STR;
            module = __import__('PowerUps.' + PowerUpManager.POWERUPS_LOADED_STR[random_select],
                                fromlist=['uselessplaceholder'])
            class_ = getattr(module, PowerUpManager.POWERUPS_LOADED_STR[random_select])
            powerup1 = class_()
            #append the copied powerup of powerupList
            self.powerupList.append(powerup1)

    def obtained_management(self):
        #draw powerup duration bar
        for powerupObtainedElement in self.powerupObtainedList:
            powerupObtainedElement.effect()
            powerupObtainedElement.update_duration()
            pygame.draw.rect(PowerUpManager.SCREEN, powerupObtainedElement.circle_color,
                             (0,475,powerupObtainedElement.duration_bar_length,5), 0)
            if(powerupObtainedElement.duration_expired):
                self.powerupObtainedList.remove(powerupObtainedElement)

    def collision_management(self, powerup):
        """Takes in bottom pipes and the bird and returns true if there is a collision"""
        if (Jayhawk.Y+60 > powerup.y and Jayhawk.Y-25 < powerup.y) and (Jayhawk.X+60 > powerup.x and Jayhawk.X-25 < powerup.x):
            return True
        return False

    def draw_powerups(self):
        #draw powerups that are spawned in the air
        for powerupElement in self.powerupList:
            pygame.draw.circle(PowerUpManager.SCREEN, powerupElement.circle_color, powerupElement.circle_pos,
                               powerupElement.circle_radius, powerupElement.circle_width)
            PowerUpManager.SCREEN.blit(powerupElement.image, powerupElement.image_rect)
            if(self.collision_management(powerupElement)):
               self.powerupList.remove(powerupElement)
            if(powerupElement.scroll() == False):
               self.powerupList.pop(0)
