#Imports
import unittest, time, sys, os, pygame, types
from Jayhawk import *
from Pipe import *
from Background import *
from database import *
#from FlappyJayhawk import *

#Required Pygame Initializations
pygame.init()
pygame.display.set_mode((600,500))

def testsuite():
    """
    Loads in all tests and returns a test suite
    """
    testing = unittest.TestSuite()
    testing.addTest(unittest.TestLoader().loadTestsFromTestCase(TestStringMethods))
    testing.addTest(unittest.TestLoader().loadTestsFromTestCase(TestJayhawkDefs))
    testing.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBackgroundDefs))
    return testing

class TestJayhawkDefs(unittest.TestCase):
    """
    Testcase for Jayhawk Class Defintions
    """
    #Required testing variables
    jayimage = pygame.image.load(os.path.join('images', 'jayhawk.png'))
    jayhawk = Jayhawk(1,1,(1,1),jayimage)
    
    #Sets up the test
    def setUp(self):
        """
        Sets up the test
        Prints the short descriptions of the tests
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
    #Asserts True if something is loaded into the image file
    def test_is_image_working(self):
        """test_is_image_working"""
        self.assertNotEqual(TestJayhawkDefs.jayhawk.image,None)

    #Testing if update position definition is working
    #Checks if the image position updates while jumping and while not jumping
    #Asserts if the image position changes
    def test_is_update_position_working(self):
        """test_is_update_position_working"""
        currentPos = TestJayhawkDefs.jayhawk.y
        TestJayhawkDefs.jayhawk.jump()
        TestJayhawkDefs.jayhawk.updatePosition()
        withJumpPos = TestJayhawkDefs.jayhawk.y
        TestJayhawkDefs.jayhawk.updatePosition()
        afterJumpPos = TestJayhawkDefs.jayhawk.y
        
        self.assertNotEqual(currentPos, withJumpPos,"Update Position with jump FAILED")
        self.assertNotEqual(withJumpPos,afterJumpPos,"Update Position without jump FAILED")

    #Testing if gravity definition is working
    #Checks if the Jayhawk's speed changes when jumping without gravity against jumping with gravity, and jumping with gravity and jumping without gravity
    #Asserts if the speed changes
    def test_is_gravity_working(self):
        """test_is_gravity_working"""
        TestJayhawkDefs.jayhawk.jump()
        JumpWithoutGravity = TestJayhawkDefs.jayhawk.reg_speed
        TestJayhawkDefs.jayhawk.gravity()
        JumpWithGravity = TestJayhawkDefs.jayhawk.reg_speed
        TestJayhawkDefs.jayhawk.gravity()
        NoJumpWithGravity = TestJayhawkDefs.jayhawk.reg_speed
        
        self.assertNotEqual(JumpWithoutGravity,JumpWithGravity,"Test Jumping with Gravity FAILED")
        self.assertNotEqual(JumpWithGravity,NoJumpWithGravity,"Test Gravity speed with jumping/without jumping FAILED")

    #Testing if rotate center definition is working
    #Checks if original image is different from the rotated image
    #Asserts that the current image is different from the rotated image     
    def test_is_rot_center_working(self):
        """test_is_rot_center_working"""
        originalImage = TestJayhawkDefs.jayhawk.rect
        rotatedImage = TestJayhawkDefs.jayhawk.rot_center(TestJayhawkDefs.jayimage,3)
        self.assertNotEqual(originalImage,rotatedImage,"Rotated image and current image are not the same FAILED")

    #Testing if jump defintion is working
    #Checks if the jayhawk's counters and jumping boolean's are set to true
    #Asserts True if the jumping conditions pass        
    def test_is_jump_working(self):
        """test_is_jump_working"""
        TestJayhawkDefs.jayhawk.jump()
        self.assertTrue(TestJayhawkDefs.jayhawk.up_counter == 0 and TestJayhawkDefs.jayhawk.isGoingUp and TestJayhawkDefs.jayhawk.isJumping,"Conditions created when jayhawk should be jumping FAILED")

    #Testing if clamp definition is working
    #Checks if the Jayhawk image is loaded in
    #Asserts True if something is loaded into the image file
    def test_is_clamp_working(self):
        """test_is_clamp_working"""
        TestJayhawkDefs.jayhawk.rect.move(-9999,9999)
        TestJayhawkDefs.jayhawk.clamp()
        self.assertTrue(TestJayhawkDefs.jayhawk.rect.x >= 0 and TestJayhawkDefs.jayhawk.rect.y <= 440,"Clamp places jayhawk back into bounds FAILED")

    #Testing if mask definition is working
    #Checks if the type passed back is a type mask
    #Asserts if the mask type is the same as the type passed back from the mask definition     
    def test_is_mask_working(self):
        """test_is_mask_working"""
        self.surface = pygame.Surface((1,1))
        self.assertEqual( type(TestJayhawkDefs.jayhawk.mask), type(pygame.mask.from_surface(self.surface)),"Type mask is returned FAILED")

    #Testing if rect definition is working
    #Checks if the type passed back is a type rect
    #Asserts if the rect type is the same as the type passed back from the rect definition 
    def test_is_rect_working(self):
        """test_is_rect_working"""
        self.assertEqual( type(TestJayhawkDefs.jayhawk.rect), pygame.Rect,"Type rect is returned FAILED")


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
        


class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
		
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

def main():
    """
    Loads the test and exits the pygame screen.
	Keeps the dialog box up for 300 seconds
    """
    unittest.TextTestRunner(verbosity=2).run(testsuite())
    pygame.quit()
    sys.exit(time.sleep(300))
	
"""
Starts application by calling main function
"""
if __name__ == "__main__":
    main()

