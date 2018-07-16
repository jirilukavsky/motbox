import unittest
import numpy as np
from numpy import testing
from motbox import *

class TestPosition(unittest.TestCase):
    # https://docs.python.org/2/library/unittest.html
    # http://pythontesting.net/framework/unittest/unittest-introduction/

    def setUp(self):
        self.P0 = Position()
        self.P1 = Position((-2, 2, 2, -2), (-2, -2, 2, 2))
        self.P2 = Position((-2, 2, 2, -2, 0), (-2, -2, 2, 2, 0))

    def test_is_min_distance_complied_1(self):
        self.assertTrue(self.P1.is_min_distance_complied(3))

    def test_is_min_distance_complied_2(self):
        self.assertFalse(self.P2.is_min_distance_complied(3))

    def test_random_positions(self):
        """Does it work? And is min distance tested?
        """
        min_distance = 4
        P = Position()
        P.random_positions(8, (-10, 10), (-10, 10), min_distance)
        self.assertTrue(P.is_min_distance_complied(min_distance))
