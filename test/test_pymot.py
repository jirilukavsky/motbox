import unittest
import pymot

class TestTrack(unittest.TestCase):
    # https://docs.python.org/2/library/unittest.html
    # http://pythontesting.net/framework/unittest/unittest-introduction/

    def setUp(self):
        pass

    def test_numbers_3_4(self):
        self.assertEqual(3 * 4, 12)

if __name__ == '__main__':
    unittest.main()
