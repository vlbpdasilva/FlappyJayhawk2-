"""
EECS 448 - "Flappy Jayhawk" -- Project 3
@author Victor Berger, Jesse Yang, Jeromy Tsai, and Cammy Vo
prof: John Gibbons
University of Kansas
code freeze: April 8th, 2016 - 11:59 pm
 
Basic controls:
From the menu, press the spacebar to start game. Use the up arrow to control the Jayhawk up.
Hitting one of the moving blocks causes you to lose. Then, the user can press 'c' to restart 
or Escape to close the game.

Sources used:_____________________

Official Pygame documentation: http://www.pygame.org/docs/
Youtube videos available at https://www.youtube.com/playlist?list=PL6gx4Cwl9DGAjkwJocj7vlc_mFU-4wXJq
Pipe image from http://vignette3.wikia.nocookie.net/fantendo/images/0/06/RocketPipes.png/revision/latest?cb=20100430132034
Background obtained from https://peukalo.wordpress.com/tag/super-mario/
Github repository used for help with Pygame implementations: https://github.com/TimoWilken/flappy-bird-pygame
Pygame clock documentation: http://www.geon.wz.cz/pygame/ref/pygame_time.html
Python documentation regarding classes: https://docs.python.org/2/tutorial/classes.html

"""

#Import
import sys, pygame, time, os
from random import randint
from Jayhawk import *
from Pipe import *
from Background import *

#Initialization
pygame.init()

#Screen Initializations
pygame.display.set_caption("Flappy Jayhawk")
size = width, height = (600, 500)
screen = pygame.display.set_mode(size)

#Color Definitions
black = (0,0,0)
white = (255,255,255)
blue = (0, 0, 255)
red = (255, 0, 0)

#Clock Implementation
clock = pygame.time.Clock()
FPS = 60

#Font Definitions and sizes
smallFont = pygame.font.SysFont("comicsansms", 14)
medFont = pygame.font.SysFont("comicsansms", 25)
largeFont = pygame.font.SysFont("comicsansms", 50)

class objRef():
    """Simulating pointers in python can be done explicitly.
    Source: http://stackoverflow.com/a/1145848
    Calling a function of a module from a string with the function's name in Python can be compressed to: result = getattr(foo, 'bar')()
    Source: http://stackoverflow.com/a/3071
    Python using getattr to call function with variable parameters You could try something like: getattr(foo, bar)(*params)
    Source: http://stackoverflow.com/a/11781292"""
    def __init__(self, obj): self.obj = obj
    def get(self):    return self.obj
    def set(self, obj):      self.obj = obj
    def call(self, methodToCall, params):   return getattr(self.obj, methodToCall)(*params)

def load_images():
    """Load all images required by the game and return a dict of them.
    The returned dict has the following keys:
    jayhawk: The image of the Jayhawk bird.
    background: The game's background image.
    pipe: The image of the pipe (a 540px image extending both end-piece and body).
    """

    def load_image(img_file_name):
        """Return the loaded pygame image with the specified file name.
        This function looks for images in the game's images folder
        (./images/).  All images are converted before being returned to
        speed up blitting.
        Arguments:
        img_file_name: The file name (including its extension, e.g.
            '.png') of the required image, without a file path.
        """
        file_name = os.path.join('.', 'images', img_file_name)
        img = pygame.image.load(file_name)
        img.convert()
        return img

    return {'jayhawk': load_image('jayhawk.png'),
            'background': load_image('repeatTest_smw.png'),
            'background2': load_image('background2.png'),
            'background3': load_image('background3.png'),
            'pipe': load_image('pipe.png')
            }

def start_menu():
    """Create a start menu that gives the users the title of the game and the creators of the game
    Also gives users the directions to start the game and the directions to play the game.
    Users will stay on the start menu until they press the corresponding key to start the game or press x to exit the game.
    """
    intro = True

    images = load_images();
    #Scrolling background declaration
    back = Background(images['background'], images['background'].get_size(), height)
    
    while intro: 
        # Start menu is being shown
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

        screen.fill((255, 231, 181))

        #Draw background
        screen.blit(back.image, back.rect)
        screen.blit(back.image, back.rect2)
        screen.blit(back.image, back.rect3)
        #Make background scroll
        back.scroll()

        message_to_screen("Flappy JayHawks",
                            blue,
                            -100,
                            "large")
        message_to_screen("By: Jeromy Tsai, Cammy Vo, Jesse Yang, Victor Berger",
                            blue,
                            -20,
                            "small")
        message_to_screen("Press SPACE to play!!",
                            red,
                            20,
                            "medium")

        pygame.display.update()
        pygame.time.delay(7)
        
def game_over():
    """
    Creates the game over screen that users will see when they jayhawk touches a pipe, causing the player to lose.
    """

    while 1:
        message_to_screen("Game Over",
                            blue,
                            0,
                            "large")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
                quit()


def text_objects(text, color, size):
    """
    Creates text objects with corresponding sizes. 
    Can expand to a greater range of font size by adding more to this list.
    """
    if size == "small":
        textSurface = smallFont.render(text, True, color)
    elif size == "medium":
        textSurface = medFont.render(text, True, color)
    elif size == "large":
        textSurface = largeFont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0, size="small"):
    """
    Creates the message that is displayed on the screen to users. 
    Will be centered and msg, color, size can be changed
    """
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((width/2),(height/2)+y_displace)
    screen.blit(textSurf,textRect)

def pipe_collisions_top(bird,pipes):
    """Takes in top pipes and the bird and returns true if there is a collision"""
    #---------Notes:--------
    #Screen is (600, 500)
    #Upper right is (600,0)
    #Lower left is (0,500)
    #Lower right is (600 ,500)
    
    if bird.y < (504 + pipes.y) and (bird.x+50 > pipes.x and bird.x-30 < pipes.x):
        return True
    return bird.colliderect(pipes)
	
    
def pipe_collisions_bot(bird,pipes):
    """Takes in bottom pipes and the bird and returns true if there is a collision"""
    if bird.y + 60 > pipes.y and (bird.x+50 > pipes.x and bird.x-30 < pipes.x):
        return True
    return bird.colliderect(pipes)
    
def pipe_passed(bird,pipes):
    """Pass pipe and increment score"""
    if bird.y > pipes.y and (bird.x+30 == pipes.x):
        return True   

def objReftest(c):
    """demo for objRef and calling methods  """
    c.call('test', [0, 'bar'])
        
def gameLoop():
    """
    Runs the game loop until users lose by allowing the jayhawk to collide with the pipes.
    When game over the game will show the game over screen and give the users the option to play again.
    """
    gameOver = False
    gameExit = False
    
    images = load_images();

    #Scrolling background declaration
    back = Background(images['background'], images['background'].get_size(), height)

    #Array declaration for moving pipes
    pipe = Pipe(images['pipe'], width)
    pipeList = []
    pipeList.append(pipe)
    #add pipes every 2 seconds
    delayBeforeNextPipe = 286 #(1000 / pygame.time.delay(n)) * 2
    delayBeforeNextPipeIncr = 0;
    
    #Definition of the jayhawk object and its corresponding rect
    jayhawk = Jayhawk(80,200,(60,60),images['jayhawk'])
    
    #Random pipe declaration for testing
    pip = images['pipe']
    pip = pygame.transform.scale(pip, (50, 100))
    piprect = pip.get_rect()
    piprect = piprect.move(5,0)

    #demo for objRef and calling methods    
    piplol = objRef(Pipe(images['pipe'], width))
    piplol.call('test',[42, 'bar'])
    pipeRef = objRef(pipe)#pipe declared above
    objReftest(pipeRef)
    

    #Rect declaration of screen
    screenrect = screen.get_rect()

    #Initial difficulty setting
    difficulty = 1;

    #Screen fill color variable
    fill = (255, 231, 181);

    #initialize score
    score = 0
    
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                pygame.quit()
                quit()
                sys.exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:   
                    # listens for ESCAPE key to close the game
                    gameExit = True
                    pygame.quit()
                    sys.exit
                if event.key == pygame.K_UP: 
                    jayhawk.jump()
                if event.key == pygame.K_1:
                        difficulty = 1;
                        back = Background(images['background'], images['background'].get_size(), height);
                        fill = (255, 231, 181);
                if event.key == pygame.K_2:
                        difficulty = 2;
                        ### background image from http://freetems.net/files/2143_t2.png
                        back = Background(images['background2'], images['background2'].get_size(), height);
                        fill = (17, 131, 255);
                if event.key == pygame.K_3:
                        difficulty = 3;
                        ### background image from https://kanimate.files.wordpress.com/2015/05/3.jpg
                        back = Background(images['background3'], images['background3'].get_size(), height);           

        jayhawk.updatePosition()
                
        #Keeps the Jayhawk in screen for testing
        #jayrect.clamp_ip(screenrect)
        jayhawk.clamp()        

        screen.fill(fill)

        #Draw background
        screen.blit(back.image, back.rect)
        screen.blit(back.image, back.rect2)
        screen.blit(back.image, back.rect3)
        
        #Make background scroll
        back.scroll()
    
        #Generates new pipes by appending them to the end of Pipe array
        delayBeforeNextPipeIncr = delayBeforeNextPipeIncr + 1
        if(delayBeforeNextPipeIncr > delayBeforeNextPipe):
            pipe1 = Pipe(images['pipe'], width)
            pipeList.append(pipe1)
            delayBeforeNextPipeIncr = 0
        #Draw pipe
        for pipeElement in pipeList:
            screen.blit(pipeElement.image_top, pipeElement.rect_top)
            screen.blit(pipeElement.image_bot, pipeElement.rect_bot)
            #make pipe scroll
            if(pipeElement.scroll() == False):
                pipeList.pop(0)
                
        #Draw Jayhawk
        screen.blit(jayhawk.image, jayhawk.rect)

        #Implements collisions
        for pipeElement in pipeList:
            botPipeRect = pipeElement.rect_bot
            topPipeRect = pipeElement.rect_top
            #if (pipe_collisions_top(jayrect,topPipeRect)):
            if (pipe_collisions_top(jayhawk.rect,topPipeRect)):
                gameOver = True
            #if (pipe_collisions_bot(jayrect,botPipeRect)):
            if (pipe_collisions_bot(jayhawk.rect,botPipeRect)):   
                gameOver = True


	#Implements score
        for pipeElement in pipeList:
            if (pipe_passed(jayhawk.rect,pipeElement.rect_top)):
                score = score + 1
        message_to_screen(str(score),
			blue,
			-200,
			"large")    
        while gameOver == True:
                       
            screen.fill(fill)
            #Draw background	
            screen.blit(back.image, back.rect)
            screen.blit(back.image, back.rect2)
            screen.blit(back.image, back.rect3)		           
            #Make background scroll		              
            #back.scroll()	

            #Draw final pipe location
            for pipeElement in pipeList:
                    screen.blit(pipeElement.image_top, pipeElement.rect_top)
                    screen.blit(pipeElement.image_bot, pipeElement.rect_bot)
		
            #Draw Jayhawk
            jayhawk.updatePosition()
            jayhawk.clamp()
            screen.blit(jayhawk.image, jayhawk.rect)
            
                        
            #Draw message
            message_to_screen(str(score),
                            blue,
                            -200,
                            "large")
            message_to_screen("Game Over",
                            blue,
                            -50,
                            "large")		     
            message_to_screen("Press c to play again",	
                            blue,		                            
                            50,		                             
                            "small")	
                          
            pygame.display.update()
            clock.tick(FPS)
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            gameOver = False
                            gameExit = True
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_c:
                                    gameLoop()
                            if event.key == pygame.K_ESCAPE:
                                    gameExit = True
                                    pygame.quit()
                                    sys.exit
                                        
                        
        
        #Updates screen and implements delay
        pygame.display.update()
        pygame.display.flip()
        clock.tick(FPS)

def main():
    """
    The application's entry point. Calls "start_menu" and "gameLoop" functions
    """
    gameExit = False
    start_menu()
    gameLoop()
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
    pygame.quit()
    quit()
    sys.exit
    
    
"""
Starts application by calling main function
"""
if __name__ == '__main__':
    main()
