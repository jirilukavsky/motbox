import unittest, os, re
import numpy as np
from numpy import testing
from motbox import Track, Position

from motbox import visualisations as vis

track_data_path = os.path.join("test", "tracks", "T220.csv")

COMPLETE = True

class TestVisualisation(unittest.TestCase):
  def setUp(self):
    T1 = Track()
    T1.load_from_csv(track_data_path)
    self.T1 = T1


  def tearDown(self):
    # removes generated files so they are not left in .git by accident
    for f in os.listdir("test"):
      if re.search(".*(.png)|(.mp4)", f):
        os.remove(os.path.join("test", f))


  def test_plot(self):
    vis.plot(self.T1.x, self.T1.y, os.path.join("test", "test_trajectory.png"))
    self.assertTrue(True)


  @unittest.skipUnless(COMPLETE, "Time consuming video generation")
  def test_make_video(self):
    vis.trajectory_video(self.T1, os.path.join("test", "test_video.mp4"))
    self.assertTrue(True)
