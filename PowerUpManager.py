import pygame
import settings
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

        self.spawnChance = 50

        self.q = []
        
        for index, powerupElement in enumerate(PowerUpManager.POWERUPS_LOADED_STR):
            module = __import__('PowerUps.' + powerupElement, fromlist=['uselessplaceholder'])
            class_ = getattr(module, powerupElement)
            powerup = class_()
            #self.powerupLoadedList.append(powerup)
            #test
            self.powerupObtainedList.append(powerup)
            self.powerupObtainedList[index].duration_remaining = 0  
                        
        print PowerUp.POWERUPS_LOADED_CLEAN
        print PowerUp.POWERUPS_LOADED#.split( )[2].split('\'')

    def spawn_management(self):        
        #spawn powerup at random
        if(settings.pipeManager.delayBeforeNextPipeIncr == 0):
            del self.q[:]
            for powerupElement in PowerUpManager.POWERUPS_LOADED_STR:                
                if(randint(0, 100) < self.spawnChance):
                    #select a random index out of the POWERUPS_LOADED_STR
                    #random_select = randint(0, len(self.POWERUPS_LOADED_STR) - 1)
                    #instantiate the powerup from the random index of POWERUPS_LOADED_STR;
                    module = __import__('PowerUps.' + powerupElement,#PowerUpManager.POWERUPS_LOADED_STR[random_select],
                                        fromlist=['uselessplaceholder'])
                    class_ = getattr(module, powerupElement)#PowerUpManager.POWERUPS_LOADED_STR[random_select])
                    powerup1 = class_()
                    #append the copied powerup of powerupList
                    self.q.append((powerup1,
                                  randint(0, settings.pipeManager.delayBeforeNextPipe)))#self.powerupList.append(powerup1)

        for powerupTupleElement in self.q:
            if(settings.pipeManager.delayBeforeNextPipeIncr == powerupTupleElement[1]):
                self.powerupList.append(powerupTupleElement[0])

    def obtained_management(self):
        """if duration hasnt expired call effect()
        if duration HAS expired call effect_expire()"""
        #draw powerup duration bar
        for index, powerupObtainedElement in enumerate(self.powerupObtainedList):   
            powerupObtainedElement.update_duration()
            if(not powerupObtainedElement.duration_expired):
                powerupObtainedElement.effect()
                pygame.draw.rect(PowerUpManager.SCREEN, powerupObtainedElement.circle_color,
                                 (0,475 - index * 5,powerupObtainedElement.duration_bar_length,5), 0)
            else:
                powerupObtainedElement.effect_expire()

    def collision(self, powerup):
        """Takes in bottom pipes and the bird and returns true if there is a collision"""
        return (Jayhawk.Y+60 > powerup.y and Jayhawk.Y-25 < powerup.y) and (Jayhawk.X+60 > powerup.x and Jayhawk.X-25 < powerup.x)
        

    def draw_powerups(self):
        #draw powerups that are spawned in the air
        for powerupElement in self.powerupList:
            pygame.draw.circle(PowerUpManager.SCREEN, powerupElement.circle_color, powerupElement.circle_pos,
                               powerupElement.circle_radius, powerupElement.circle_width)
            PowerUpManager.SCREEN.blit(powerupElement.image, powerupElement.image_rect)
            if(self.collision(powerupElement)):
               self.re_init_powerup(powerupElement.effectname)#self.powerupObtainedList.append(powerupElement)
               self.powerupList.remove(powerupElement)
            if(powerupElement.scroll() == False):
               self.powerupList.pop(0)

    def re_init_powerup(self, effectname):
        for index, powerupElement in enumerate(self.powerupObtainedList):
            if powerupElement.effectname == effectname:
                break
        module = __import__('PowerUps.' + effectname,
                                fromlist=['uselessplaceholder'])
        class_ = getattr(module, effectname)
        self.powerupObtainedList[index] = class_()
