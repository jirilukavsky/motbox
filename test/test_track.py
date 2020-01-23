"""Unittests for track
"""

import unittest, os, re
import numpy as np
from numpy import testing
from motbox import Track, Position

COMPLETE = True
track_data_path = os.path.join("test", "tracks", "T220.csv")

class TestTrack(unittest.TestCase):
    # https://docs.python.org/2/library/unittest.html
    # http://pythontesting.net/framework/unittest/unittest-introduction/

    def setUp(self):
        T1 = Track()
        T2 = Track()        
        T1.load_from_csv(track_data_path, delim=",")
        T2.load_from_csv(track_data_path, delim=",")
        self.T1 = T1
        self.T2 = T2
        self.diff1 = (1.1, 1.2)
        self.vector_8 = np.array(range(8), dtype=float)
        self.matrix_18 = self.vector_8.reshape((1, 8))
        self.matrix_81 = self.vector_8.reshape((8, 1))
        self.matrix_28 = np.array(range(16)).reshape(2, 8)
        pass

    def tearDown(self):
        # removes generated files so they are not left in .git by accident
        for f in os.listdir("test"):
            if re.search(".*(.csv)", f):
                os.remove(os.path.join("test", f))

    def test_move_x(self):
        oldx = self.T1.x.copy()
        oldy = self.T1.y
        self.T1.move(self.diff1)
        testing.assert_allclose(oldx + self.diff1[0], self.T1.x)

    def test_move_y(self):
        oldx = self.T1.x
        oldy = self.T1.y.copy()
        difference = (1.1, 1.2)
        self.T1.move(self.diff1)
        testing.assert_allclose(oldy + self.diff1[1], self.T1.y)

    def test_move_numpy(self):
        difference_numpy = np.array(self.diff1)
        self.T1.move(self.diff1)
        self.T2.move(difference_numpy)
        testing.assert_allclose(self.T1.x, self.T2.x)

    def test_move_numpy(self):
        difference_numpy = np.array(self.diff1)
        self.T1.move(self.diff1)
        self.T2.move(difference_numpy)
        testing.assert_allclose(self.T1.x, self.T2.x)

    def test_timestep(self):
        step = self.T1.timestep()
        self.assertAlmostEqual(step, 0.01)

    @unittest.skipUnless(COMPLETE, "Time consuming video generation")
    def generate_vonmises(self):
        opts = {"xlim": (-10, 10), "ylim": (-10, 10), "spacing":2.}
        time = np.arange(0, 5, 0.5)
        self.T1.generate_vonmises(Positions().circular_positions(8, 5), speed= 3., kappa = 8, opts = opts, time = time)
        self.assertTrue(True)
