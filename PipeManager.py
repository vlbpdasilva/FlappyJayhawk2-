import pygame
#from Jayhawk import *

#import powerups
from Pipe import *

class PipeManager():

    SCREEN = pygame.display.set_mode((600,500))

    def __init__(self, image):
        self.image = image
        #Array declaration for moving pipes
        pipe = Pipe(self.image, 600)
        self.pipeList = []
        self.pipeList.append(pipe)
        #add pipes every 2 seconds
        self.delayBeforeNextPipe = 286 #(1000 / pygame.time.delay(n)) * 2
        self.delayBeforeNextPipeIncr = 0;

        self.scrollSpeed = 1
        self.spawnTime = 286

    def spawn_management(self):             
        #Spawns new pipes by appending them to the end of Pipe array
        self.delayBeforeNextPipeIncr = self.delayBeforeNextPipeIncr + 1
        if(self.delayBeforeNextPipeIncr > self.delayBeforeNextPipe):
            pipe1 = Pipe(self.image, 600)
            self.pipeList.append(pipe1)
            self.delayBeforeNextPipeIncr = 0

    def score(self, bird):
        """Pass pipe and increment score"""
        for pipeElement in self.pipeList:
            if bird.y > pipeElement.rect_top.y and (bird.x+30 == pipeElement.rect_top.x):
                return True
        
    def collision(self, bird):
        #Implements collisions
        for pipeElement in self.pipeList:
            botPipeRect = pipeElement.rect_bot
            topPipeRect = pipeElement.rect_top
            #if (pipe_collisions_top(jayrect,topPipeRect)):
            if (self.pipe_collisions_top(bird, topPipeRect)):
                return True#gameOver = True
            #if (pipe_collisions_bot(jayrect,botPipeRect)):
            if (self.pipe_collisions_bot(bird, botPipeRect)):   
                return True#gameOver = True
                
    def pipe_collisions_top(self,bird,pipes):
        """Takes in top pipes and the Jayhawk and returns true if there is a collision"""
        #---------Notes:--------
        #Screen is (600, 500)
        #Upper right is (600,0)
        #Lower left is (0,500)
        #Lower right is (600 ,500)
        
        if bird.y < (504 + pipes.y) and (bird.x+50 > pipes.x and bird.x-30 < pipes.x):
            return True
        #return Jayhawk.colliderect(pipes)
	
    
    def pipe_collisions_bot(self,bird,pipes):
        """Takes in bottom pipes and the Jayhawk and returns true if there is a collision"""
        if bird.y + 60 > pipes.y and (bird.x+50 > pipes.x and bird.x-30 < pipes.x):
            return True
        #return Jayhawk.colliderect(pipes)


    def draw_pipes(self, scroll):
        #Draw pipe
        for pipeElement in self.pipeList:
            PipeManager.SCREEN.blit(pipeElement.image_top, pipeElement.rect_top)
            PipeManager.SCREEN.blit(pipeElement.image_bot, pipeElement.rect_bot)
            #make pipe scroll
            if(scroll == 1):
                if(pipeElement.scroll() == False):
                    self.pipeList.pop(0)
