import os, pygame
from random import randint

def loadImports(path):
    """Load the powerups in PowerUps folder"""
    files = os.listdir(path)
    imps = []

    for i in range(len(files)):
        name = files[i].split('.')
        if len(name) > 1:
            if name[1] == 'py' and name[0] != '__init__':
               name = name[0]
               imps.append(name)

    file = open(path+'__init__.py','w')

    toWrite = '__all__ = '+str(imps)
    
    file.write(toWrite)
    file.close()
    return (toWrite)

class PowerUp(pygame.sprite.Sprite):
    """This acts as an Abstract Base Class for custom power ups
    Attributes that all PowerUp instances share:
    POWERUP_DURATION: duration of powerup's effects for the Jayhawk
    POWERUPS_LOADED: init string of powerups included in the PowerUps folder
    POWERUPS_LOADED_CLEAN: string of powerups
    """
    POWERUP_DURATION = 5#5seconds

    POWERUPS_LOADED = loadImports('PowerUps/')
    POWERUPS_LOADED_CLEAN = POWERUPS_LOADED.replace('__all__ = [', '').replace('\'', '').replace(',', '').replace(']', '')
    
    def __init__(self, color, pos, radius, width, image, effectname):
        """Params:
        color: color of PowerUp circle
        pos: pos of circle
        radius: radius of circle
        width: width of circe
        image: image of effect
        effectname: effect's name which should be unique
        """
        #--------------when the PowerUp is floating in the air
        #circular aura
        self.color = color
        self.x = pos[0]#x coord for center
        self.y = pos[1]#y coord for center
        self.x = 600
        self.y = randint(0 + radius, 500 - radius)
        self.radius = radius
        self.width = width

        #power up image
        self.scale = ((int)(self.radius * 1.4), (int)(self.radius * 1.4))
        self.PowerUp_image = image
        self.PowerUp_image = self.PowerUp_image.convert_alpha()
        self.PowerUp_image = pygame.transform.scale(self.PowerUp_image, self.scale)
        self.image_x = self.x - self.scale[0] / 2
        self.image_y = self.y - self.scale[1] / 2

        #--------------when the PowerUp has been picked up
        #power up effect name to refer to
        self.effectname = effectname

        #power up duration bar length: represented as a 200px bar that, over POWERUP_DURATION, will reduce to 0px
        self.PowerUp_duration_bar_length = 200
        self.duration_remaining = 300#5 seconds * 60 FPS = 300 frame duration
    
    def scroll(self):
        """make power-ups scroll like the pipes do"""
        self.x -= 1
        self.image_x -= 1
        
        if(self.x <= -600):
            return False
        return True

    @property
    def circle_color(self):
        """return color
        """
        return self.color
    @property
    def circle_pos(self):
        """return pos
        """
        return (self.x, self.y)
    @property
    def circle_radius(self):
        """return radius
        """
        return self.radius
    @property
    def circle_width(self):
        """return width
        """
        return self.width

    @property
    def image(self):
        """return image
        """
        return self.PowerUp_image
    @property
    def image_rect(self):
        """return image rect
        """
        return pygame.Rect(self.image_x, self.image_y, 25, 25)

    def update_duration(self):   
        """decrement duration of powerup's effect
        """
        self.duration_remaining -= 1
        if(self.duration_remaining % 3 == 0 or self.duration_remaining % 3 == 1):
            self.PowerUp_duration_bar_length -= 1

    @property
    def duration_bar_length(self):
        """return duration bar length
        """
        return self.PowerUp_duration_bar_length
    @property
    def duration_expired(self):
        """return True if duration has expired
        """
        return (self.duration_remaining <= 0)

    
    def effect( self ):
        """Some description that tells you it's abstract,
        often listing the methods you're expected to supply.
        The effect that all PowerUps must have
        """
        raise NotImplementedError( "Should have implemented this" )

    def effect_expire(self):
        """Some description that tells you it's abstract,
        often listing the methods you're expected to supply.
        Effect that occurs upon duration_expired
        """
        raise NotImplementedError( "Should have implemented this" )
