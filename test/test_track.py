"""Unittests for track
"""

import unittest, os, re
import numpy as np
from numpy import testing
from motbox import Track, Position

COMPLETE = False
track_data_path = os.path.join("test", "tracks", "T220.csv")

class TestTrack(unittest.TestCase):
    # https://docs.python.org/2/library/unittest.html
    # http://pythontesting.net/framework/unittest/unittest-introduction/

    def setUp(self):
        T1 = Track()
        T2 = Track()        
        T1.load_from_csv(track_data_path)
        T2.load_from_csv(track_data_path)
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
            if re.search(".*(.png)|(.mp4)", f):
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
    def test_generate_vonmises(self):
        #, position, speed, kappa, time=None, direction=None):
        self.T1.generate_vonmises(
            Position().circular_positions(8, 5), 5., 40)
        self.T1.plot(os.path.join("test", "test_generated.png"))
        self.T1.make_video(os.path.join("test", "test_generated.mp4"))
        self.assertTrue(True)

    def test_plot(self):
        self.T1.plot(os.path.join("test", "test_trajectory.png"))
        self.assertTrue(True)

    @unittest.skipUnless(COMPLETE, "Time consuming video generation")
    def test_make_video(self):
        self.T1.make_video(os.path.join("test", "test_video.mp4"))
        self.assertTrue(True)
