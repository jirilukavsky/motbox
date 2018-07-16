""" Set of tools for generating trajectories
for Multiple Object Tracking Experiments

"""
__all__ = ["Track", "Position", "Puppeteer"]

#from . import track
from motbox.track import Track
from motbox.track import Position
#from . import control
from motbox.control import Puppeteer
