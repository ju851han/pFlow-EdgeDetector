import unittest
from polygon import Polygon


class PolygonTestCase(unittest.TestCase):
    """ Test Class for Polygon Class

    """

    def setUp(self):
        """ setUp() is executed BEFORE the test is started

        :return: None
        """
        self.p = Polygon()

    def tearDown(self):
        """ tearDown() is executed AFTER the test has been executed.

        :return: None
        """
        self.p = None

    def test_add_string_point(self):
        """ Tests what happens if the method is passed a string instead of integer

        Hint: There is no overflow for integer numbers in Python 3. That's why no further tests for add_point() is needed.
        :return: None
        """
        self.assertRaises(ValueError, self.p.add_point, 'a', 'b')


if __name__ == '__main__':
    unittest.main()
