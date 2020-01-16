"""Coordinates for Multiple Object Tracking

Track object contains time, x- and y-coordinates of variable number of
moving objects.

"""

import numpy as np
from scipy.spatial import distance

class Position(object):
    """Represents position of n objects or one timeslice of Track
    """

    def __init__(self, x=None, y=None):
        """Constructor
        """
        self.x = np.array(x, dtype=float)
        self.y = np.array(y, dtype=float)
        if x is None:
            self.n_objects = 0
        else:
            self.n_objects = len(x)

    def is_min_distance_complied(self, min_distance):
        """Checks if objects' distances are smaller than specified value
        """
        coords = np.zeros((self.n_objects, 2))
        coords[:, 0] = self.x
        coords[:, 1] = self.y
        dist = distance.pdist(coords)
        return np.all(dist > min_distance)

    def random_positions(self, n, xlim, ylim, min_distance):
        """Populates square ares (xlim x ylim) with n objects.
        Checks minimum inter-object distance
        """
        while True:
            self.n_objects = n
            self.x = np.random.uniform(low=xlim[0], high=xlim[1], size=(n, ))
            self.y = np.random.uniform(low=ylim[0], high=ylim[1], size=(n, ))
            if self.is_min_distance_complied(min_distance):
                break
        return self

    def circular_positions(self, n, radius, center=(0, 0)):
        """Put n objects on a circle with given center and diameter
        """
        n_range = np.arange(n)
        self.x = center[0] + radius * np.sin(n_range * 2 * np.pi / n)
        self.y = center[1] + radius * np.cos(n_range * 2 * np.pi / n)
        self.n_objects = n
        return self

    def move(self, difference):
        """Shifts all x,y by constant.

        Expects array or tuple
        """
        self.x += difference[0]
        self.y += difference[1]

    def scale(self, factor):
        """Multiplies all x,y by constant

        """
        self.x *= factor
        self.y *= factor

    def jitter_positions(self, amount, method="normal"):
        """Adds uniform or normal jitter to existing positions
        """
        if method in ["normal"]:
            jitter = np.random.normal(scale=amount, size=(2, self.n_objects))
        if method in ["uniform"]:
            jitter = np.random.uniform(low=-amount, high=amount, size=(2, self.n_objects))
        self.move((jitter[0, :], jitter[1, :]))

class Track(object):
    """Track object

    - x - numpy 2D-array (dim1 = time, dim2 = objects)
    - y - numpy 2D-array (dim1 = time, dim2 = objects)
    - time - numpy 1D-array
    """
    def __init__(self):
        """The constructor creates an empty object with data set to None
        """
        self.x = None
        self.y = None
        self.time = None
        self.n_objects = 0


    def load_from_csv(self, filename, delimiter='\t'):
        """Initializes object from data file.
        Uses format from RepMot/RevMot studies.
        """
        mat = np.genfromtxt(filename, delimiter=delimiter)
        # first column

        ncol = mat.shape[1]
        if ncol % 2 == 1:
            self.time = mat[:, 0]
            self.x = mat[:, 1::2]
            self.y = mat[:, 2::2]
            self.n_objects = self.x.shape[1]
        else:
            # even number of columns not expected
            # error
            pass
        pass

    def move(self, difference):
        """Shifts all x,y by constant.

        Expects array or tuple
        """
        self.x += difference[0]
        self.y += difference[1]

    def scale(self, factor):
        """Multiplies all x,y by constant

        """
        self.x *= factor
        self.y *= factor

    def timestep(self):
        """Estimates size of time steps in timeline
        """
        return np.mean(np.diff(self.time))

    def time_interpolate(self, newtime):
        """Interpolates data according to new timeline

        Does not check the validity of new time
        (ascending order, being within time limits)
        """
        nrow_new = len(newtime)
        newx = np.zeros((nrow_new, self.n_objects))
        newy = np.zeros((nrow_new, self.n_objects))
        for index in range(self.n_objects):
            newx[:, index] = np.interp(newtime, self.time, self.x[:, index])
            newy[:, index] = np.interp(newtime, self.time, self.y[:, index])
        self.x = newx
        self.y = newy
        self.time = newtime

    def position_for_time(self, timevalue):
        """Interpolates coordinates for given time point
        """
        n_objects = self.n_objects
        newx = np.zeros((1, n_objects))
        newy = np.zeros((1, n_objects))
        for index in range(n_objects):
            newx[:, index] = np.interp(timevalue, self.time, self.x[:, index])
            newy[:, index] = np.interp(timevalue, self.time, self.y[:, index])
        return (newx, newy)


    def summary(self):
        """Returns text summary
        """
        if (not self.x is None) and (not self.y is None) and (not self.time is None):
            report = "Track: {} objects, time {} - {}".format(
                self.n_objects, np.amin(self.time), np.amax(self.time))
        else:
            report = "Track: NOT initialized"
        return report

if __name__ == "__main__":
    # execute only if run as a script
    pass
