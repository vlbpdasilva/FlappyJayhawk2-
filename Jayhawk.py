import pygame
class Jayhawk(pygame.sprite.Sprite):
    """The Jayhawk that the player will be controlling.
    The Jayhawk will ascend or descend and its main objective is to avoid
    colliding with pipes. Ascending will occur when the player hits up/space.
    Descending will occur when the player is not causing the Jayhawk to
    ascend. Colliding with pipes will cause the Jayhawk to lose health.
    At 0 health, the player loses the game.
    
    Attributes that all Jayhawk instances share: 
    isGoingUp:(deprecated) flag to detect if Jayhawk is going up, up_counter is changed as a result
    isJumping: flag to detect if jump has been called to reset Jayhawk's speed back to reg_speed
    up_speed:(deprecated) the speed going up
    down_speed:(deprecated) the speed going down
    reg_speed: Jayhawk's Jumping speed
    gravity_accel: Jayhawk's Speed decreases at this rate
    up_counter:(deprecated) up_speed is changed based on up_counter
    down_counter:(deprecated) down_speed is changed based on down_counter
    X: The bird's X coordinate.
    Y: The bird's Y coordinate.
    """

    #is the Jayhawk moving up (jumping)?
    isGoingUp = False
    isJumping = False
    #Jayhawk speeds going up and down
    up_speed = -22
    down_speed = 2
    reg_speed = 20 / 3
    gravity_accel = 4 / 4
    """
    Counters for up and down movement
    These counters allow for the changing of speed according to length of movement of the Jayhawk
    Generates effect of acceleration
    """
    up_counter = 0
    down_counter = 0
    X = 80
    Y = 200
    
    def __init__(self, x, y, scale, image):
        """Initialise a new Jayhawk instance.
        Arguments:
        x: The Jayhawk's initial X coordinate.
        y: The Jayhawk's initial Y coordinate.
        scale: The Jayhawk's size multiplier.
        image: The Jayhawk's image.
        """
        super(Jayhawk, self).__init__()
        self.x = x
        self.y = y
        Jayhawk.X = self.x
        Jayhawk.Y = self.y
        self.Jayhawk_image = image
        self.Jayhawk_image = self.Jayhawk_image.convert_alpha()
        self.Jayhawk_image = pygame.transform.scale(self.Jayhawk_image, scale)
        self.original = self.Jayhawk_image
        self.Jayhawk_mask = pygame.mask.from_surface(self.Jayhawk_image)

    def updatePosition(self):
        """Update the position of the Jayhawk by calculating all necessary
        position movements affected by gravity function and player-inputted jumps.
        """
        
        """
        The following IF statement controls the entire movement of the Jayhawk while it's going up.
        The counter is used to control speed, giving the user a feeling of acceleration.
        
        The following ELSE statement controls the entire movement of the Jayhawk while it's going Jayhawk.down.
        The counter is used to control speed, giving the user a feeling of acceleration.
        """
        """if(Jayhawk.isGoingUp):
            self.y = self.y + Jayhawk.up_speed/2
            Jayhawk.up_counter += 1
            Jayhawk.down_counter = 0        
            if(Jayhawk.up_counter == 1):
                Jayhawk.up_speed = -16
            elif(Jayhawk.up_counter == 2):
                Jayhawk.up_speed = -12
            elif(Jayhawk.up_counter == 3):
                Jayhawk.up_speed = -10    
            elif(Jayhawk.up_counter == 4):
                Jayhawk.up_speed = -6           
            elif(Jayhawk.up_counter == 5):
                Jayhawk.up_speed = -4         
            elif(Jayhawk.up_counter == 6):
                Jayhawk.up_speed = -2           
            elif(Jayhawk.up_counter > 6):
                Jayhawk.isGoingUp = False
                Jayhawk.up_counter = 0
                Jayhawk.up_speed = -22 
        else:
            self.y = self.y + Jayhawk.down_speed/8            
            Jayhawk.down_counter += 1
            Jayhawk.up_counter = 0            
            if(Jayhawk.down_counter == 1):
                Jayhawk.down_speed = 4            
            elif(Jayhawk.down_counter == 2):
                Jayhawk.down_speed = 6            
            elif(Jayhawk.down_counter == 3):
                Jayhawk.down_speed = 10            
            elif(Jayhawk.down_counter == 4):
                Jayhawk.down_speed = 12            
            elif(Jayhawk.down_counter == 5):
                Jayhawk.down_speed = 16            
            elif(Jayhawk.down_counter > 5):
                Jayhawk.down_speed = 22"""

        self.gravity()
        self.y = self.y + Jayhawk.reg_speed
        Jayhawk.Y = self.y
        #update rotation
        self.Jayhawk_image = self.original
        self.Jayhawk_image = self.rot_center(self.Jayhawk_image, -1 * Jayhawk.reg_speed)

    def gravity(self):
        """apply rate of gravity to change the Jayhawk's speed
        """
        if(Jayhawk.isJumping):
            Jayhawk.reg_speed = -40 / 3
            Jayhawk.isJumping = False
        else:
            Jayhawk.reg_speed = Jayhawk.reg_speed + Jayhawk.gravity_accel

        if(Jayhawk.reg_speed > 20 / 2):
            Jayhawk.reg_speed = 20 / 2

    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size
        Source: http://pygame.org/wiki/RotateCenter?parent= 
        """
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def jump(self):
        """ The Jayhawk jumps up thus moving up.
        listens for UP ARROW key.
        Triggers isGoingUp to be True, sets up_counter to 0 to begin initial jump speed (up_speed to -16).
        """
        Jayhawk.isGoingUp = True
        Jayhawk.up_counter = 0
        Jayhawk.isJumping = True

    def clamp(self):
        """ Clamp the Jayhawk to stay within the screen's boundaries.
        This is done rather than calling clamp_ip() because returning the Jayhawk class's rect does not
        seem to qualify as a proper get_rect() that clamp_ip() looks for.
        """
        if(self.y < 0):
            self.y = 0
        elif(self.y > 440):
            self.y = 440

    def grounded(self):
        """collision detection for bottom of screen
        """
        return(self.rect.bottom  > 462)

    def set_image(self, image, scale):
        """Change the jayhawk's image and scale
        """
        self.Jayhawk_image = image
        self.Jayhawk_image = self.Jayhawk_image.convert_alpha()
        self.Jayhawk_image = pygame.transform.scale(self.Jayhawk_image, scale)
        self.original = self.Jayhawk_image
    
    @property
    def image(self):
        """Get a Surface containing this bird's image.
        """
        return self.Jayhawk_image

    @property
    def mask(self):
        """Get a bitmask for use in collision detection.
        The bitmask excludes all pixels in self.image with a
        transparency greater than 127.
        """
        return self.Jayhawk_mask

    @property
    def rect(self):
        """Get the bird's position, width, and height, as a pygame.Rect.
        """
        return pygame.Rect(self.x, self.y, 25, 25)
