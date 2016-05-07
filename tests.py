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
    return testing




class TestJayhawkDefs(unittest.TestCase):
    """Testing Jayhawk Defintions"""
    
    #Required testing variables
    jayimage = pygame.image.load(os.path.join('images', 'jayhawk.png'))
    jayhawk = Jayhawk(100,100,(1,1),jayimage)
    def setUp(self):
        """
        Sets up the test
        Prints the short descriptions of the tests
        """
        
        currentTest = self.shortDescription()
        
        if (currentTest == "test_is_image_working"):
            sys.stderr.write("Testing if something is loaded into the Jayhawk image ... ")
        elif (currentTest == ""):
            print "Tests if something is loaded into the image, is not nothing"
        else:
            sys.stderr.write("Unnamed test ... ")
    def tearDown(self):
        """
        Cleans up after the test
        Nothing is required here
        """
        
    #tests if the Jayhawk image is loaded in
    def test_is_image_working(self):
        """test_is_image_working"""
        self.assertNotEqual(TestJayhawkDefs.jayhawk.image,None)
    def test_is_update_position_working(self):
        CurrentPos = TestJayhawkDefs.jayhawk.y
        TestJayhawkDefs.jayhawk.jump()
        WithJumpPos = TestJayhawkDefs.jayhawk.y

        
        TestJayhawkDefs.jayhawk.updatePosition()
        self.assertNotEqual(TestJayhawkDefs.jayhawk.image, TestJayhawkDefs.jayhawk.updatePosition)
    def test_is_gravity_working(self):
        TestJayhawkDefs.jayhawk.jump()
        JumpWithoutGravity = TestJayhawkDefs.jayhawk.reg_speed
        TestJayhawkDefs.jayhawk.gravity()
        JumpWithGravity = TestJayhawkDefs.jayhawk.reg_speed
        TestJayhawkDefs.jayhawk.gravity()
        NoJumpWithGravity = TestJayhawkDefs.jayhawk.reg_speed
        
        self.assertNotEqual(JumpWithoutGravity,JumpWithGravity,"Test Jumping with Gravity Failed")
        self.assertNotEqual(JumpWithGravity,NoJumpWithGravity,"Test Gravity without Jumping Failed")
    def test_is_rot_center_working(self):
        self.assertTrue(True)
    def test_is_jump_working(self):
        TestJayhawkDefs.jayhawk.jump()
        self.assertTrue(TestJayhawkDefs.jayhawk.up_counter == 0 and TestJayhawkDefs.jayhawk.isGoingUp and TestJayhawkDefs.jayhawk.isJumping)
    def test_is_clamp_working(self):
        TestJayhawkDefs.jayhawk.rect.move(-9999,9999)
        TestJayhawkDefs.jayhawk.clamp()
        self.assertTrue(TestJayhawkDefs.jayhawk.rect.x >= 0 and TestJayhawkDefs.jayhawk.rect.y <= 440)
    def test_is_mask_working(self):       
        self.surface = pygame.Surface((1,1))
        self.assertEqual( type(TestJayhawkDefs.jayhawk.mask), type(pygame.mask.from_surface(self.surface)) )
    def test_is_rect_working(self):
        self.assertEqual( type(TestJayhawkDefs.jayhawk.rect), pygame.Rect )


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
    unittest.TextTestRunner(verbosity=2).run(testsuite())
    pygame.quit()
    sys.exit(time.sleep(300))

if __name__ == "__main__":
    main()

