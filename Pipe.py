import pygame
from random import randint     



class Pipe(pygame.sprite.Sprite):
    """
    x: The bird's X coordinate.
    y: The bird's Y coordinate.
    msec_to_climb: The number of milliseconds left to climb, where a
        complete climb lasts Bird.CLIMB_DURATION milliseconds.
    Constants:
    WIDTH: The width, in pixels, of the bird's image.
    HEIGHT: The height, in pixels, of the bird's image.
    SINK_SPEED: With which speed, in pixels per millisecond, the bird
        descends in one second while not climbing.
    CLIMB_SPEED: With which speed, in pixels per millisecond, the bird
        ascends in one second while climbing, on average.  See also the
        Bird.update docstring.
    CLIMB_DURATION: The number of milliseconds it takes the bird to
        execute a complete climb.
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
        self.y = randint(25, 475 - Pipe.GAP)#475 should be game_window_height and game_window_size should be passed as param

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

    """def test(self, a, b):
        Used together with objRef in FlappyJayhawk.py as a demo
        print a
        self.y = a
        print b"""
    
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
        return pygame.Rect(self.x, self.y - 504, 25, 25)#pipe's img height is 504

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
        return pygame.Rect(self.x, self.y + Pipe.GAP, 25, 25)

