import pygame
from random import randint     



class Pipe(pygame.sprite.Sprite):
    """The main obstacle in the game. Pipe will represent a pair of pipes that appear together in tandem top and bottom positions.
    Pipe's exact position is random. Spawning of Pipe will occur at a set interval. Pipe will scroll toward the Jayhawk.
    Upon collision with Pipe, Jayhawk takes massive damage falling and becoming unable to get up thus ending the game.
    Passing Pipe increments score counter.
    
    Attributes that all Pipe instances share:
    GAP: the gap between top and bottom pipes in the pipe pair
    """
    GAP = 200
    
    def __init__(self, image, game_window_width):
        """Initialise a new Pipe instance.
        Arguments:
        image: The Pipe's image. This will be duplicated for both top and
                bottom pipes for the pipe pair.
        game_window_width: The position at which new pipes spawn.
        """
        super(Pipe, self).__init__()
        self.x = game_window_width
        self.reset_x = game_window_width
        self.y_top = randint(25, 475 - Pipe.GAP)#475 should be game_window_height and game_window_size should be passed as param
        self.y_bot = self.y_top

        self.Pipe_image_top = image
        self.Pipe_image_top = self.Pipe_image_top.convert_alpha()
        self.Pipe_image_top = pygame.transform.flip(self.Pipe_image_top, False, True)
        self.Pipe_mask_top = pygame.mask.from_surface(self.Pipe_image_top)
        
        self.Pipe_image_bot = image
        self.Pipe_image_bot = self.Pipe_image_bot.convert_alpha()
        self.Pipe_mask_bot = pygame.mask.from_surface(self.Pipe_image_bot)



    def scroll(self):
        """Update the Pipe's position by changing its x-coord by -1.
        Get whether the pipe has hit the boundary -600 and stopped scrolling (and reset).
        When stopped scrolling, this should be the signal to pop the pipe off the pipeList.
        """
        self.x = self.x - 1
        if(self.x + 600 == 0):
            self.x = self.reset_x
            return False
        return True
    
    @property
    def image_top(self):
        """Get a Surface containing the top pipe's image.
        """
        return self.Pipe_image_top

    @property
    def mask_top(self):
        """Get a bitmask for use in collision detection.
        The bitmask excludes all pixels in self.image with a
        transparency greater than 127."""
        return self.Pipe_mask_top

    @property
    def rect_top(self):
        """Get the top pipe's position, width, and height, as a pygame.Rect.
        """
        return pygame.Rect(self.x, self.y_top - 504, 25, 25)#pipe's img height is 504

    @property
    def image_bot(self):
        """Get a Surface containing the bot pipe's image.
        """
        return self.Pipe_image_bot

    @property
    def mask_bot(self):
        """Get a bitmask for use in collision detection.
        The bitmask excludes all pixels in self.image with a
        transparency greater than 127."""
        return self.Pipe_mask_bot

    @property
    def rect_bot(self):
        """Get the bot pipe's position, width, and height, as a pygame.Rect.
        """
        return pygame.Rect(self.x, self.y_bot + Pipe.GAP, 25, 25)

