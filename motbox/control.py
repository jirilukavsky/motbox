import numpy as np
import copy

class Puppeteer:
    """
    Gets Track data and move PsychoPy stimuli objects accordingly
    """

    def __init__(self):
        """The constructor creates an empty object
        """
        self.objects = []
        self.track = None

    def position_for_time(self, timevalue):
        """Interpolates coordinates for given time point
        """
        n_objects = self.track.n_objects
        newx = np.zeros((1, n_objects))
        newy = np.zeros((1, n_objects))
        for index in range(n_objects):
            newx[:, index] = np.interp(timevalue, self.track.time, self.track.x[:, index])
            newy[:, index] = np.interp(timevalue, self.track.time, self.track.y[:, index])
        return (newx, newy)

    def update_positions_psychopy(self, timevalue):
        """Updates the controlled objects' positions to coordinates based on
        given time point
        """
        (newx, newy) = self.position_for_time(timevalue)
        n_track_objects = self.track.n_objects
        n_screen_objects = len(self.objects)
        for index in range(min(n_track_objects, n_screen_objects)):
            self.objects[index].pos = (float(newx[:,index]), float(newy[:,index]))

    def clone_template_psychopy(self, psychopyobject, ntimes):
        """Populates objects array by copies of given PsychoPy object
        """
        self.objects = []
        for index in range(ntimes):
            new_object = copy.copy(psychopyobject)
            new_object.name = "{} copy {}".format(psychopyobject.name, index)
            self.objects.append(new_object)
