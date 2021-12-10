import unittest
from imageCleaner import ImageCleaner


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def setUp(self):
        """ setUp() is executed BEFORE the test is started

        :return: None
        """
        self.ic = ImageCleaner('../training_images/test/Pentagon.png')

    def tearDown(self):
        """ tearDown() is executed AFTER the test has been executed.

        :return: None
        """
        self.ic = None

    def test_init_with_str(self):
        """ Tests if the expected exception is thrown when a non-existent image path is passed to the method

        :return: None
        """
        self.assertRaises(AttributeError, self.ic.__init__, 'foo')

    def test_init_with_number(self):
        """

        :return:
        """
        self.assertRaises(TypeError, self.ic.__init__, 123)


if __name__ == '__main__':
    unittest.main()
