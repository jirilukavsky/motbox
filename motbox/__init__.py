""" Set of tools for generating trajectories
for Multiple Object Tracking Experiments

"""
__all__ = ["Track", "Position", "Puppeteer"]

from .track import Track, Position
from .control import Puppeteer
