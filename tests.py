#Imports
import unittest, time, sys, os, pygame, types, imp
from Jayhawk import *
from Pipe import *
from Background import *
from PipeManager import *
from PowerUp import *
from PowerUpManager import *
from FlappyJayhawk import *
from database import *

#Required Pygame Initializations
pygame.init()
pygame.display.set_mode((600,500))

def testsuite():
    """
    Loads in all tests and returns a test suite
    """
    testing = unittest.TestSuite()
    testing.addTest(unittest.TestLoader().loadTestsFromTestCase(TestJayhawkDefs))
    testing.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBackgroundDefs))
    testing.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPipeDefs))
    testing.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPipeManagerDefs))
    testing.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPowerUpDefs))
    testing.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDatabaseDefs))
    return testing

class TestDatabaseDefs(unittest.TestCase):
    """
    Testcase for Database Class Defintions
    """
    #Required testing variables
    testdata = database
    sqlavailable = False
    try:
        import mysql.connector
        sqlavailable = True
    except ImportError:
        sqlavailable = False

    #Sets up the test
    def setUp(self):
        """
        Sets up the test
        Prints short descriptions of the tests
        """
        currentTest = self.shortDescription()
        if (currentTest == "test_is_addScore_working"):
            sys.stderr.write("Testing if addScore is allowing sql ... ")
        elif (currentTest == "test_is_printTable_working"):
            sys.stderr.write("Testing if printTable is allowing sql ... ")
        else:
            sys.stderr.write("Unnamed test ... ")
            
    #Tears down the tests
    def tearDown(self):
        """
        Cleans up after the test
        Nothing is required here
        """
        
    @unittest.skipIf(not sqlavailable,"database not available to test")
    def test_is_addScore_working(self):
        """test_is_addScore_working"""
        self.addScoreWorking = False
        try:
            self.conn=TestDatabaseDefs.mysql.connector.connect(user='jyang',password='gumy555',host='mysql.eecs.ku.edu',database='jyang')
            self.mycursor=self.conn.cursor()
            self.add_score = ("INSERT INTO scores_alltime (score, name, timestamp) VALUES (%s, %s, %s)")
            self.currentTime = datetime.datetime.now()
            self.score_data = (1, 'test', self.currentTime)
            self.mycursor.execute(self.add_score, self.score_data)
            self.delete_score = "DELETE FROM scores_alltime WHERE timestamp = '%s'" % self.currentTime
            self.mycursor.execute(self.delete_score)
            self.addScoreWorking = True
        except TestDatabaseDefs.mysql.connector.Error as err:
            print("database() error: {}".format(err))
            self.addScoreWorking = False
            
        self.assertTrue(self.addScoreWorking,"addScore loaded FAILED")
        
    @unittest.skipIf(not sqlavailable,"database not available to test")    
    def test_is_printTable_working(self):
        """test_is_printTable_working"""
        try:
            self.conn=TestDatabaseDefs.mysql.connector.connect(user='jyang',password='gumy555',host='mysql.eecs.ku.edu',database='jyang')
            self.mycursor=self.conn.cursor()
            self.mycursor.execute("SHOW TABLES")            
            print(self.mycursor.fetchall())
            self.printWorking = True
        except TestDatabaseDefs.mysql.connector.Error as err:
            print("database() error: {}".format(err))
            self.printWorking = False
        self.assertTrue(self.printWorking,"print loaded FAILED")


class TestPowerUpDefs(unittest.TestCase):
    """
    Testcase for PowerUp Class Defintions
    """
    #Required testing variables
    testpipeimage = pygame.image.load(os.path.join('images', 'pipe.png'))
    testpipemanager = PipeManager(testpipeimage)
    testjayimage = pygame.image.load(os.path.join('images', 'jayhawk.png'))
    testjayhawk = Jayhawk(1,1,(1,1),testjayimage)
    testpipe = Pipe(testpipeimage,300)
    testpowerup = PowerUp((0,0,0), (50,50), 20, 0, testjayimage, 'test')
    
    #Sets up the test
    def setUp(self):
        """
        Sets up the test
        Prints short descriptions of the tests
        """
        currentTest = self.shortDescription()
        if (currentTest == "test_is_loadImports_working"):
            sys.stderr.write("Testing if loadImports is returning a string ... ")
        elif (currentTest == "test_is_scroll_working"):
            sys.stderr.write("Testing if scroll is scrolling to left ... ")
        elif (currentTest == "test_is_circle_color_working"):
            sys.stderr.write("Testing if circle color is returning a color ... ")
        elif (currentTest == "test_is_circle_pos_working"):
            sys.stderr.write("Testing if circle position is returning a tuple of two arguments ... ")
        elif (currentTest == "test_is_circle_radius_working"):
            sys.stderr.write("Testing if circle radius is returning an int ... ")
        elif (currentTest == "test_is_circle_width_working"):
            sys.stderr.write("Testing if circle width is returning an int ... ")        
        elif (currentTest == "test_is_image_working"):
            sys.stderr.write("Testing if something is being passed into image ... ")
        elif (currentTest == "test_is_image_rect_working"):
            sys.stderr.write("Testing if image rect is returning type rect ... ")
        elif (currentTest == "test_is_update_duration_working"):
            sys.stderr.write("Testing if update duration is decreasing the duration time ... ")
        elif (currentTest == "test_is_duration_expired_working"):
            sys.stderr.write("Testing if duration expired is returning proper booleans for duration time ... ")
        else:
            sys.stderr.write("Unnamed test ... ")
            
    #Tears down the tests
    def tearDown(self):
        """
        Cleans up after the test
        Nothing is required here
        """
        
    #Testing if loadImports definition is working
    #Checks if loadImports is loading proper strings
    #Asserts True if loadImports is passing a string
    def test_is_loadImports_working(self):
        """test_is_loadImports_working"""
        self.assertEqual(type(loadImports(".")),str,"loadImports passing back a string FAILED")
        
    #Testing if scroll definition is working
    #Asserts if scroll is scrolling to the left
    def test_is_scroll_working(self):
        """test_is_scroll_working"""
        self.unscrolledPos = TestPowerUpDefs.testpowerup.x
        TestPowerUpDefs.testpowerup.scroll()
        self.assertTrue(TestPowerUpDefs.testpowerup.x < self.unscrolledPos,"Scroll moves powerup to left FAILED")
        
    #Testing if circle_color definition is working
    #Asserts if circle color is returning a color
    def test_is_circle_color_working(self):
        """test_is_circle_color_working"""
        self.assertEqual(type(TestPowerUpDefs.testpowerup.circle_color),tuple,"Circle color is returning type tuple FAILED")
        self.assertTrue(len(TestPowerUpDefs.testpowerup.circle_color) == 3,"Circle color is not returning 3 tuple arguments")
        
    #Testing if circle_pos definition is working
    #Asserts if circle pos is returning a tuple of a valid position
    def test_is_circle_pos_working(self):
        """test_is_circle_pos_working"""
        self.assertEqual(type(TestPowerUpDefs.testpowerup.circle_pos),tuple,"Circle pos is returning type tuple FAILED")
        self.assertTrue(len(TestPowerUpDefs.testpowerup.circle_pos) == 2,"Circle pos is not returning 2 tuple arguments")
        
    #Testing if circle_radius definition is working
    #Asserts if circle radius is returning a int
    def test_is_circle_radius_working(self):
        """test_is_circle_radius_working"""
        self.assertEqual(type(TestPowerUpDefs.testpowerup.circle_radius),int,"Circle radius is returning type int FAILED")
        
    #Testing if circle_width definition is working
    #Asserts if circle width is returning a int
    def test_is_circle_width_working(self):
        """test_is_circle_width_working"""
        self.assertEqual(type(TestPowerUpDefs.testpowerup.circle_width),int,"Circle width is returning type int FAILED")

    #Testing if image definition is working
    #Asserts if image is not returning nothing
    def test_is_image_working(self):
        """test_is_image_working"""
        self.assertNotEqual(type(TestPowerUpDefs.testpowerup.image),None,"image is not returnong nothing FAILED")

    #Testing if image_rect definition is working
    #Asserts if image_rect is returning a rect
    def test_is_image_rect_working(self):
        """test_is_image_rect_working"""
        self.assertEqual(type(TestPowerUpDefs.testpowerup.image_rect),pygame.Rect,"image rect is returning type rect FAILED")

    #Testing if update_duration definition is working
    #Asserts if update_duration is shortening the duration of the powerup
    def test_is_update_duration_working(self):
        """test_is_update_duration_working"""
        self.notUpdatedDuration = TestPowerUpDefs.testpowerup.duration_remaining
        TestPowerUpDefs.testpowerup.update_duration()
        self.assertTrue(TestPowerUpDefs.testpowerup.duration_remaining < self.notUpdatedDuration,"Duration decreases FAILED")
        
    #Testing if duration_expired definition is working
    #Asserts if duration_expired is returning false if duration remains and true if duration expired
    def test_is_duration_expired_working(self):
        """test_is_duration_expired_working"""
        TestPowerUpDefs.testpowerup.duration_remaining = 300
        self.assertEqual(TestPowerUpDefs.testpowerup.duration_expired,False,"Duration expired returning false on duration not expired FAILED")
        TestPowerUpDefs.testpowerup.duration_remaining = 0
        self.assertEqual(TestPowerUpDefs.testpowerup.duration_expired,True,"Duration expired returning true on duration expired FAILED")

        
class TestPipeManagerDefs(unittest.TestCase):
    """
    Testcase for PipeManager Class Defintions
    """
    #Required testing variables
    testpipeimage = pygame.image.load(os.path.join('images', 'pipe.png'))
    testpipemanager = PipeManager(testpipeimage)
    testjayimage = pygame.image.load(os.path.join('images', 'jayhawk.png'))
    testjayhawk = Jayhawk(1,1,(1,1),testjayimage)
    testpipe = Pipe(testpipeimage,300)
    
    #Sets up the test
    def setUp(self):
        """
        Sets up the test
        Prints short descriptions of the tests
        """
        currentTest = self.shortDescription()
        if (currentTest == "test_is_spawn_management_working"):
            sys.stderr.write("Testing if the pipes are giving back proper values from scrolling ... ")
        elif (currentTest == "test_is_score_working"):
            sys.stderr.write("Testing if something is loading into the score ... ")
        elif (currentTest == "test_is_collision_working"):
            sys.stderr.write("Testing if collisions are working ... ")
        elif (currentTest == "test_is_collision_pipe_num_working"):
            sys.stderr.write("Testing if collisions pipe number is returning the pipe collision and number ... ")
        elif (currentTest == "test_is_pipe_collisions_top_working"):
            sys.stderr.write("Testing if a collision top is working ... ")
        elif (currentTest == "test_is_pipe_collisions_bot_working"):
            sys.stderr.write("Testing if a collision bot is working ... ")        
        elif (currentTest == "test_is_draw_pipes_working"):
            sys.stderr.write("Testing if draw pipes is drawing something and popping off pipes ... ")
        else:
            sys.stderr.write("Unnamed test ... ")
            
    #Tears down the tests
    def tearDown(self):
        """
        Cleans up after the test
        Nothing is required here
        """
        
    #Testing if spawn_management definition is working
    #Checks if the scroll is passing off variables properly
    #Asserts True if something is loaded into the image file
    def test_is_spawn_management_working(self):
        """test_is_spawn_management_working"""
        self.currentList = len(TestPipeManagerDefs.testpipemanager.pipeList)
        TestPipeManagerDefs.testpipemanager.delayBeforeNextPipeIncr = 286
        TestPipeManagerDefs.testpipemanager.spawn_management()
        self.updatedList = len(TestPipeManagerDefs.testpipemanager.pipeList)
        self.assertTrue(self.currentList < self.updatedList,"New pipe added to list FAILED")
        
    #Testing if score definition is working
    #Checks if score is returning proper values based on pipe and bird position
    #Asserts if true no score is added and when score is added
    #May have false negatives depending on if it's the very first pipe in the list
    def test_is_score_working(self):
        """test_is_score_working"""
        TestPipeManagerDefs.testjayhawk.x = 100
        TestPipeManagerDefs.testjayhawk.y = 100
        self.noScore = TestPipeManagerDefs.testpipemanager.score(TestPipeManagerDefs.testjayhawk.rect)
        self.assertNotEqual(self.noScore,True,"True is not returned when no score should be added FAILED")
        TestPipeManagerDefs.testjayhawk.x = 569
        TestPipeManagerDefs.testjayhawk.y = 500
        self.scoreAdd = TestPipeManagerDefs.testpipemanager.score(TestPipeManagerDefs.testjayhawk.rect)
        self.assertEqual(self.scoreAdd,True,"True is returned when score is added FAILED")
        
    #Testing if collision definition is working
    #Checks if collision handling is working
    #Asserts if top and bottom are not or are colliding
    def test_is_collision_working(self):
        """test_is_collision_working"""
        TestPipeManagerDefs.testjayhawk.x = 0
        self.assertEqual(TestPipeManagerDefs.testpipemanager.collision(TestPipeManagerDefs.testjayhawk),None,"No collision returns nothing FAILED")
        TestPipeManagerDefs.testjayhawk.x = 600
        TestPipeManagerDefs.testjayhawk.y = 600
        self.assertTrue(TestPipeManagerDefs.testpipemanager.collision(TestPipeManagerDefs.testjayhawk),"Collision returns true when colliding with bottom FAILED")
        TestPipeManagerDefs.testjayhawk.y = 0
        self.assertTrue(TestPipeManagerDefs.testpipemanager.collision(TestPipeManagerDefs.testjayhawk),"Collision returns true when colliding with top FAILED")

    #Testing if collision_pipe_num definition is working
    #Checks if the bottom Pipe image is loaded in
    #Asserts if something is loaded into the image file
    def test_is_collision_pipe_num_working(self):
        """test_is_collision_pipe_num_working"""
        TestPipeManagerDefs.testjayhawk.x = 0
        self.assertEqual(TestPipeManagerDefs.testpipemanager.collision_pipe_num(TestPipeManagerDefs.testjayhawk),None,"No collision returns nothing FAILED")
        TestPipeManagerDefs.testjayhawk.x = 600
        TestPipeManagerDefs.testjayhawk.y = 600
        self.assertEqual(TestPipeManagerDefs.testpipemanager.collision_pipe_num(TestPipeManagerDefs.testjayhawk),(0,'bot'),"First index returning tuple of collision and collision number for bot FAILED")
        TestPipeManagerDefs.testjayhawk.y = 0
        self.assertEqual(TestPipeManagerDefs.testpipemanager.collision_pipe_num(TestPipeManagerDefs.testjayhawk),(0,'top'),"First index returning tuple of collision and collision number for top FAILED")

    #Testing if pipe_collisions_bot definition is working
    #Checks if returns true when there's a collision
    #Asserts if there's a collision and if there's not a collision   
    def test_is_pipe_collisions_bot_working(self):
        """test_is_pipe_collisions_bot_working"""
        TestPipeManagerDefs.testjayhawk.x = 0
        self.assertEqual(TestPipeManagerDefs.testpipemanager.pipe_collisions_bot(TestPipeManagerDefs.testjayhawk,TestPipeManagerDefs.testpipemanager.pipeList[0].rect_bot),False,"No collision returns false FAILED")
        TestPipeManagerDefs.testjayhawk.x = 600
        TestPipeManagerDefs.testjayhawk.y = 600
        self.assertTrue(TestPipeManagerDefs.testpipemanager.pipe_collisions_bot(TestPipeManagerDefs.testjayhawk,TestPipeManagerDefs.testpipemanager.pipeList[0].rect_bot),"Collision returns true when colliding FAILED")
        
    #Testing if pipe_collisions_top definition is working
    #Checks if returns true when there's a collision
    #Asserts if there's a collision and if there's not a collision  
    def test_is_pipe_collisions_top_working(self):
        """test_is_pipe_collisions_top_working"""
        TestPipeManagerDefs.testjayhawk.x = 0
        self.assertEqual(TestPipeManagerDefs.testpipemanager.pipe_collisions_top(TestPipeManagerDefs.testjayhawk,TestPipeManagerDefs.testpipemanager.pipeList[0].rect_top),False,"No collision returns false FAILED")
        TestPipeManagerDefs.testjayhawk.x = 600
        TestPipeManagerDefs.testjayhawk.y = 0
        self.assertTrue(TestPipeManagerDefs.testpipemanager.pipe_collisions_top(TestPipeManagerDefs.testjayhawk,TestPipeManagerDefs.testpipemanager.pipeList[0].rect_top),"Collision returns true when colliding FAILED")
        
    #Testing if draw_pipes definition is working
    #Checks if there's something on the screen and if the draw_pipes are not popping off scrolled out pipes
    #Asserts if there's on the screen
    def test_is_draw_pipes_working(self):
        """test_is_draw_pipes_working"""
        self.assertEqual(TestPipeManagerDefs.testpipemanager.draw_pipes(1),None)
        self.assertNotEqual(None,TestPipeManagerDefs.testpipemanager.SCREEN.blit,"Pipe manager is loading screen FAILED")
        
        
class TestPipeDefs(unittest.TestCase):
    """
    Testcase for Pipe Class Defintions
    """
    #Required testing variables
    testpipeimage = pygame.image.load(os.path.join('images', 'pipe.png'))
    testpipe = Pipe(testpipeimage,1)
    
    #Sets up the test
    def setUp(self):
        """
        Sets up the test
        Prints short descriptions of the tests
        """
        currentTest = self.shortDescription()
        if (currentTest == "test_is_scroll_working"):
            sys.stderr.write("Testing if the pipes are giving back proper values from scrolling ... ")
        elif (currentTest == "test_is_image_top_working"):
            sys.stderr.write("Testing if something is loaded into the top Pipe image ... ")
        elif (currentTest == "test_is_image_bot_working"):
            sys.stderr.write("Testing if something is loaded into the bottom Pipe image ... ")
        elif (currentTest == "test_is_mask_top_working"):
            sys.stderr.write("Testing if a mask object is passed back from top mask definition ... ")
        elif (currentTest == "test_is_mask_bot_working"):
            sys.stderr.write("Testing if a mask object is passed back from bottom mask definition ... ")
        elif (currentTest == "test_is_rect_top_working"):
            sys.stderr.write("Testing if a rect object is passed back from top rect definition ... ")        
        elif (currentTest == "test_is_rect_bot_working"):
            sys.stderr.write("Testing if a rect object is passed back from bottom rect definition ... ")
        else:
            sys.stderr.write("Unnamed test ... ")
            
    #Tears down the tests
    def tearDown(self):
        """
        Cleans up after the test
        Nothing is required here
        """
        
    #Testing if scroll definition is working
    #Checks if the scroll is passing off variables properly
    #Asserts True if something is loaded into the image file
    def test_is_scroll_working(self):
        """test_is_scroll_working"""
        TestPipeDefs.testpipe.x = -599
        self.scrollFalseCondition = TestPipeDefs.testpipe.scroll()
        TestPipeDefs.testpipe.x = -200
        self.scrollTrueCondition = TestPipeDefs.testpipe.scroll()
        self.assertTrue(self.scrollTrueCondition,"Image scrolls FAILED")
        self.assertFalse(self.scrollFalseCondition,"Image wraps back around for scrolling FAILED")
        
    #Testing if image_top definition is working
    #Checks if the top Pipe image is loaded in
    #Asserts if something is loaded into the image file
    def test_is_image_top_working(self):
        """test_is_image_top_working"""
        self.assertNotEqual(TestPipeDefs.testpipe.image_top,None,"Something is passed into top image for Pipes FAILED")
    
    #Testing if image_bot definition is working
    #Checks if the bottom Pipe image is loaded in
    #Asserts if something is loaded into the image file
    def test_is_image_bot_working(self):
        """test_is_image_bot_working"""
        self.assertNotEqual(TestPipeDefs.testpipe.image_bot,None,"Something is passed into bottom image for Pipes FAILED")
        
    #Testing if mask_top definition is working
    #Checks if the type passed back is a type mask
    #Asserts if the mask type is the same as the type passed back from the mask definition     
    def test_is_mask_top_working(self):
        """test_is_mask_top_working"""
        self.surface = pygame.Surface((1,1))
        self.assertEqual( type(TestPipeDefs.testpipe.mask_top), type(pygame.mask.from_surface(self.surface)),"Type mask is returned FAILED")

    #Testing if mask_bot definition is working
    #Checks if the type passed back is a type mask
    #Asserts if the mask type is the same as the type passed back from the mask definition     
    def test_is_mask_bot_working(self):
        """test_is_mask_bot_working"""
        self.surface = pygame.Surface((1,1))
        self.assertEqual( type(TestPipeDefs.testpipe.mask_bot), type(pygame.mask.from_surface(self.surface)),"Type mask is returned FAILED")

    #Testing if rect definition is working
    #Checks if the type passed back is a type rect
    #Asserts if the rect type is the same as the type passed back from the rect definition 
    def test_is_rect_top_working(self):
        """test_is_rect_top_working"""
        self.assertEqual( type(TestPipeDefs.testpipe.rect_top), pygame.Rect,"Type rect is returned FAILED")
    
    #Testing if rect definition is working
    #Checks if the type passed back is a type rect
    #Asserts if the rect type is the same as the type passed back from the rect definition 
    def test_is_rect_bot_working(self):
        """test_is_rect_bot_working"""
        self.assertEqual( type(TestPipeDefs.testpipe.rect_bot), pygame.Rect,"Type rect is returned FAILED")


class TestJayhawkDefs(unittest.TestCase):
    """
    Testcase for Jayhawk Class Defintions
    """
    #Required testing variables
    testjayimage = pygame.image.load(os.path.join('images', 'jayhawk.png'))
    testjayhawk = Jayhawk(1,1,(1,1),testjayimage)
    
    #Sets up the test
    def setUp(self):
        """
        Sets up the test
        Prints short descriptions of the tests
        """
        currentTest = self.shortDescription()
        if (currentTest == "test_is_image_working"):
            sys.stderr.write("Testing if something is loaded into the Jayhawk image ... ")
        elif (currentTest == "test_is_update_position_working"):
            sys.stderr.write("Testing if position is getting updated with a jump and without a jump ... ")
        elif (currentTest == "test_is_gravity_working"):
            sys.stderr.write("Testing if gravity is updating the speed of the bird ... ")
        elif (currentTest == "test_is_rot_center_working"):
            sys.stderr.write("Testing if an image with its center rotated is the same as an image without ... ")
        elif (currentTest == "test_is_jump_working"):
            sys.stderr.write("Testing if conditions for jump are passed in ... ")
        elif (currentTest == "test_is_clamp_working"):
            sys.stderr.write("Testing if the jayhawk gets clamped to the actual game's parametered screen ... ")
        elif (currentTest == "test_is_mask_working"):
            sys.stderr.write("Testing if a mask object is passed back from mask definition ... ")
        elif (currentTest == "test_is_rect_working"):
            sys.stderr.write("Testing if a rect object is passed back from rect definition ... ")
        else:
            sys.stderr.write("Unnamed test ... ")
            
    #Tears down the tests
    def tearDown(self):
        """
        Cleans up after the test
        Nothing is required here
        """
        
    #Testing if image definition is working
    #Checks if the Jayhawk image is loaded in
    #Asserts if something is loaded into the image file
    def test_is_image_working(self):
        """test_is_image_working"""
        self.assertNotEqual(TestJayhawkDefs.testjayhawk.image,None)

    #Testing if update position definition is working
    #Checks if the image position updates while jumping and while not jumping
    #Asserts if the image position changes
    def test_is_update_position_working(self):
        """test_is_update_position_working"""
        currentPos = TestJayhawkDefs.testjayhawk.y
        TestJayhawkDefs.testjayhawk.jump()
        TestJayhawkDefs.testjayhawk.updatePosition()
        withJumpPos = TestJayhawkDefs.testjayhawk.y
        TestJayhawkDefs.testjayhawk.updatePosition()
        afterJumpPos = TestJayhawkDefs.testjayhawk.y
        
        self.assertNotEqual(currentPos, withJumpPos,"Update Position with jump FAILED")
        self.assertNotEqual(withJumpPos,afterJumpPos,"Update Position without jump FAILED")

    #Testing if gravity definition is working
    #Checks if the Jayhawk's speed changes when jumping without gravity against jumping with gravity, and jumping with gravity and jumping without gravity
    #Asserts if the speed changes
    def test_is_gravity_working(self):
        """test_is_gravity_working"""
        TestJayhawkDefs.testjayhawk.jump()
        JumpWithoutGravity = TestJayhawkDefs.testjayhawk.reg_speed
        TestJayhawkDefs.testjayhawk.gravity()
        JumpWithGravity = TestJayhawkDefs.testjayhawk.reg_speed
        TestJayhawkDefs.testjayhawk.gravity()
        NoJumpWithGravity = TestJayhawkDefs.testjayhawk.reg_speed
        
        self.assertNotEqual(JumpWithoutGravity,JumpWithGravity,"Test Jumping with Gravity FAILED")
        self.assertNotEqual(JumpWithGravity,NoJumpWithGravity,"Test Gravity speed with jumping/without jumping FAILED")

    #Testing if rotate center definition is working
    #Checks if original image is different from the rotated image
    #Asserts that the current image is different from the rotated image     
    def test_is_rot_center_working(self):
        """test_is_rot_center_working"""
        originalImage = TestJayhawkDefs.testjayhawk.rect
        rotatedImage = TestJayhawkDefs.testjayhawk.rot_center(TestJayhawkDefs.testjayimage,3)
        self.assertNotEqual(originalImage,rotatedImage,"Rotated image and current image are not the same FAILED")

    #Testing if jump defintion is working
    #Checks if the jayhawk's counters and jumping boolean's are set to true
    #Asserts True if the jumping conditions pass        
    def test_is_jump_working(self):
        """test_is_jump_working"""
        TestJayhawkDefs.testjayhawk.jump()
        self.assertTrue(TestJayhawkDefs.testjayhawk.up_counter == 0 and TestJayhawkDefs.testjayhawk.isGoingUp and TestJayhawkDefs.testjayhawk.isJumping,"Conditions created when jayhawk should be jumping FAILED")

    #Testing if clamp definition is working
    #Checks if the Jayhawk image is loaded in
    #Asserts True if something is loaded into the image file
    def test_is_clamp_working(self):
        """test_is_clamp_working"""
        TestJayhawkDefs.testjayhawk.rect.move(-9999,9999)
        TestJayhawkDefs.testjayhawk.clamp()
        self.assertTrue(TestJayhawkDefs.testjayhawk.rect.x >= 0 and TestJayhawkDefs.testjayhawk.rect.y <= 440,"Clamp places jayhawk back into bounds FAILED")

    #Testing if mask definition is working
    #Checks if the type passed back is a type mask
    #Asserts if the mask type is the same as the type passed back from the mask definition     
    def test_is_mask_working(self):
        """test_is_mask_working"""
        self.surface = pygame.Surface((1,1))
        self.assertEqual( type(TestJayhawkDefs.testjayhawk.mask), type(pygame.mask.from_surface(self.surface)),"Type mask is returned FAILED")

    #Testing if rect definition is working
    #Checks if the type passed back is a type rect
    #Asserts if the rect type is the same as the type passed back from the rect definition 
    def test_is_rect_working(self):
        """test_is_rect_working"""
        self.assertEqual( type(TestJayhawkDefs.testjayhawk.rect), pygame.Rect,"Type rect is returned FAILED")


class TestBackgroundDefs(unittest.TestCase):
    """
    Testcase for Background Class Defintions
    """
    #Required testing variables
    backimage1 = pygame.image.load(os.path.join('images','repeatTest_smw.png'))
    backimage2 = pygame.image.load(os.path.join('images','background2.png'))
    backimage3 = pygame.image.load(os.path.join('images','background3.png'))
    back1 = Background(backimage1,backimage1.get_size(),1)
    back2 = Background(backimage2,backimage2.get_size(),1)
    back3 = Background(backimage3,backimage3.get_size(),1)
    
    #Sets up tests
    def setUp(self):
        """
        Sets up the test
        Prints the short descriptions of the tests
        """
        currentTest = self.shortDescription()
        if (currentTest == "test_is_scroll_working"):
            sys.stderr.write("Testing if the image's position changes based on the scroll definition ... ")
        elif (currentTest == "test_is_image_working"):
            sys.stderr.write("Testing if something get loaded into the Background image for each iteration ... ")
        elif (currentTest == "test_is_rect_working"):
            sys.stderr.write("Testing if there's a rect obtained based on the first image ... ")
        elif (currentTest == "test_is_rect2_working"):
            sys.stderr.write("Testing if there's a rect obtained based on second rect image ... ")
        elif (currentTest == "test_is_rect3_working"):
            sys.stderr.write("Testing if there's a rect obtained based on third rect image ... ")
        else:
            sys.stderr.write("Unnamed test ... ")
            
    #Tears down tests    
    def tearDown(self):
        """
        Cleans up after the test
        Nothing is required here
        """
        
    #Tests if scroll definition is working
    #Takes in current positions of all 3 backgrounds, scrolls, then checks the new position against the old position
    #Asserts true if the new position scrolled to the left
    def test_is_scroll_working(self):
        """test_is_scroll_working"""        
        currentPosition1 = TestBackgroundDefs.back1.x
        currentPosition2 = TestBackgroundDefs.back2.x
        currentPosition3 = TestBackgroundDefs.back3.x
        TestBackgroundDefs.back1.scroll()
        TestBackgroundDefs.back2.scroll()
        TestBackgroundDefs.back3.scroll()
        self.assertTrue(currentPosition1 > TestBackgroundDefs.back1.x)
        self.assertTrue(currentPosition2 > TestBackgroundDefs.back2.x)
        self.assertTrue(currentPosition3 > TestBackgroundDefs.back3.x)
        
    #Tests if image definition is working
    #Checks if there's something inside the image return
    #Asserts true if there's something inside
    def test_is_image_working(self):
        """test_is_image_working"""        
        self.assertNotEqual(TestBackgroundDefs.back1.image,None,"First image has something loaded in FAILED")
        self.assertNotEqual(TestBackgroundDefs.back2.image,None,"Second image has something loaded in FAILED")
        self.assertNotEqual(TestBackgroundDefs.back3.image,None,"Third image has something loaded in FAILED")
        
    #Tests if rect defintion for first case is working
    #Checks if the type class passed back is a rect
    #Asserts true if the type class passed back is a rect
    def test_is_rect_working(self):
        """test_is_rect_working"""      
        self.assertEqual(type(TestBackgroundDefs.back1.rect), pygame.Rect,"First image has type rect with rect defintion loaded in FAILED")

    #Tests if rect defintion for second case is working
    #Checks if the type class passed back is a rect
    #Asserts true if the type class passed back is a rect    
    def test_is_rect2_working(self):
        """test_is_rect2_working""" 
        self.assertEqual(type(TestBackgroundDefs.back2.rect), pygame.Rect,"Second image has type rect with rect defintion loaded in FAILED" )
        
    #Tests if rect defintion for third case is working
    #Checks if the type class passed back is a rect
    #Asserts true if the type class passed back is a rect
    def test_is_rect3_working(self):
        """test_is_rect3_working"""       
        self.assertEqual(type(TestBackgroundDefs.back3.rect), pygame.Rect,"Third image has type rect with rect defintion loaded in FAILED" )
        

def main():
    """
    Loads the test and exits the pygame screen.
	Keeps the dialog box up for 500 seconds
    """
    unittest.TextTestRunner(verbosity=2).run(testsuite())
    pygame.quit()
    sys.exit(time.sleep(500))
	
"""
Starts application by calling main function
"""
if __name__ == "__main__":
    main()

