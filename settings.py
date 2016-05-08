# settings.py

def init():
    #window properties
    global size
    global width
    global height
    global FPS
    size = width, height = (600, 500)
    FPS = 60


    #sound properties
    global sound_toggle
    sound_toggle = True

    #gameplay properties
    global gravity_accel

    #game's global objects
    global jayhawk
    global pipeManager
