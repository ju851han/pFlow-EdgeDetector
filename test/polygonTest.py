import unittest
from polygon import Polygon


class PolygonTestCase(unittest.TestCase):

    def setUp(self):
        self.p = Polygon()

    def tearDown(self):
        self.p = None

    def test_add_point(self):
        self.assertRaises(ValueError, self.p.add_point, 'a', 'b')


if __name__ == '__main__':
    unittest.main()
