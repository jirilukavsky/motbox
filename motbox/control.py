"""Controlling PsychoPy objects using Track data

In future we may add other experiment frameworks, e.g., OpenSesame
"""
import copy
import numpy as np

class Puppeteer(object):
    """
    Gets Track data and move PsychoPy stimuli objects accordingly
    """

    def __init__(self):
        """The constructor creates an empty object
        """
        self.objects = []
        self.track = None


    def update_positions_psychopy(self, timevalue):
        """Updates the controlled objects' positions to coordinates based on
        given time point
        """
        (newx, newy) = self.track.position_for_time(timevalue)
        n_track_objects = self.track.n_objects
        n_screen_objects = len(self.objects)
        for index in range(min(n_track_objects, n_screen_objects)):
            self.objects[index].pos = (float(newx[:, index]), float(newy[:, index]))


    def clone_template_psychopy(self, psychopyobject, ntimes):
        """Populates objects array by copies of given PsychoPy object
        """
        self.objects = []
        for index in range(ntimes):
            new_object = copy.copy(psychopyobject)
            new_object.name = "{} copy {}".format(psychopyobject.name, index)
            self.objects.append(new_object)
