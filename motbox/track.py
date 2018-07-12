"""Coordinates for Multiple Object Tracking

Track object contains time, x- and y-coordinates of variable number of
moving objects.

"""

import numpy as np

class Track:
    """Track object

    - x - numpy 2D-array (dim1 = time, dim2 = objects)
    """
    def __init__(self):
        """The constructor creates an empty object with data set to None
        """
        self.x = None
        self.y = None
        self.time = None
        self.n_objects = 0


    def load_from_csv_v0(self, filename):
        """Initializes object from data file.
        Uses format from RepMot/RevMot studies.
        """
        mat = np.genfromtxt(filename, delimiter='\t')
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

    def save_to_csv_v0(self, filename):
        """Saves object's data to file

        Mimics classic format. The main difference in the use of
        scientific notation and longer precision.
        """
        nrow = len(self.time)
        new_time = self.time.reshape((nrow, 1))
        new_xy = np.zeros((nrow, 2 * self.n_objects))
        new_xy[:, 0::2] = self.x
        new_xy[:, 1::2] = self.y
        mat = np.concatenate((new_time, new_xy), axis=1)
        np.savetxt(filename, mat, delimiter="\t")

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

    def load_from_csv(self, filename):
        """Initializes object from data file.

        Calls classic format. Maybe add format detection in future.
        """
        return self.load_from_csv_v0(filename)

    def save_to_csv(self, filename):
        """Saves object's data to file

        Defaults to classic format.
        """
        return self.save_to_csv_v0(filename)

    def summary(self):
        """Returns text summary
        """
        if (not self.x is None) and (not self.y is None) and (not self.time is None):
            return "Track: {} objects, time {} - {}".format(
                self.n_objects, np.amin(self.time), np.amax(self.time))
        else:
            return "Track: NOT initialized"


if __name__ == "__main__":
    # execute only if run as a script
    T = Track()
    fn_in = "./examples/data/T220.csv"
    fn_out = "./tmp/T220new.csv"
    T.load_from_csv(fn_in)
    #print(T.mat.shape)
    print(T.summary())
    print(T.time[4:10])
    print(T.timestep())
    T.save_to_csv_v0(fn_out)
    print("ok")
    # print(T.x[:5, :])
    # T.time_interpolate(np.array([0, 0.015, 0.03]))
    print(T.summary())
    # print(T.x)
    P = Puppeteer()
    P.track = T
    print(P.position_for_time(0.1))
