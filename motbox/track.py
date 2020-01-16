"""Coordinates for Multiple Object Tracking

Track object contains time, x- and y-coordinates of variable number of
moving objects.

"""

import numpy as np
from scipy.spatial import distance
from scipy.sparse import csgraph
import matplotlib.pyplot as plt


from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage


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


    def plot(self, filename, xlim=(-10, 10), ylim=(-10, 10)):
        """Plots positions into file
        """
        plt.figure()
        plt.plot(self.x, self.y, "o")
        plt.xlabel = "x"
        plt.ylabel = "y"
        plt.xlim(xlim)
        plt.ylim(ylim)
        plt.savefig(filename)


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


    def load_from_csv(self, filename):
        """Initializes object from data file.

        Calls classic format. Maybe add format detection in future.
        """
        return self.load_from_csv_v0(filename)


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


    def plot(self, filename, xlim=(-10, 10), ylim=(-10, 10)):
        """Plots trajectories into a file
        """
        plt.figure()
        plt.plot(self.x, self.y, "k")
        plt.xlabel = "x"
        plt.ylabel = "y"
        plt.xlim(xlim)
        plt.ylim(ylim)
        plt.savefig(filename)

    def make_video(self, filename, xlim=(-10, 10), ylim=(-10, 10), callback=None, axisOff=True):
        WIDTH = 900
        HEIGHT = 600
        DPI = 150
        FPS = 25
        DURATION = np.max(self.time) - np.min(self.time)

        fig, axis = plt.subplots(figsize=(1.0 * WIDTH / DPI, 1.0 * HEIGHT / DPI), dpi=DPI)
        def make_frame(t):
            axis.clear()
            (tx, ty) = self.position_for_time(t + np.min(self.time))
            axis.plot(tx, ty, "ko")
            axis.set_xlim(xlim)
            axis.set_ylim(ylim)
            axis.set_title("Time {:.2f} s".format(t))
            if not callback is None:
                callback(axis)
            if axisOff:
                plt.axis('off')
            return mplfig_to_npimage(fig)
        animation = VideoClip(make_frame, duration=DURATION)
        #animation.write_gif(filename, fps=FPS)
        animation.write_videofile(filename, fps=FPS)
        pass


    def bounce_square(self, position, direction, arena_opts):
        """Checks for boundary bouncing and returns corrected directions
        """
        xlim = arena_opts["xlim"]
        ylim = arena_opts["ylim"]
        too_R = position.x > xlim[1]
        too_L = position.x < xlim[0]
        too_U = position.y < ylim[0]
        too_D = position.y > ylim[1]
        too_horizontal = np.logical_or(too_R, too_L)
        too_vertical = np.logical_or(too_U, too_D)
        corner = np.logical_and(too_horizontal, too_vertical)
        side = np.logical_xor(too_horizontal, too_vertical)
        direction[corner] = np.mod(direction[corner] + np.pi, 2 * np.pi)
        direction[np.logical_and(side, too_horizontal)] = 2 * np.pi - direction[np.logical_and(side, too_horizontal)]
        direction[np.logical_and(side, too_vertical)] = np.mod(np.pi - direction[np.logical_and(side, too_vertical)], 2 * np.pi)
        return direction


    def bounce_objects(self, position, direction, opts):
        """Checks for minimum inter-object spacing
        """
        spacing = opts["spacing"]
        coords = np.zeros((position.n_objects, 2))
        coords[:, 0] = position.x
        coords[:, 1] = position.y
        distances = distance.squareform(distance.pdist(coords)) < spacing
        n_groups, grouping = csgraph.connected_components(distances)
        for group_code in range(n_groups):
            count = np.sum(grouping == group_code)
            if count == 2:
                direction[grouping == group_code] = direction[grouping == group_code][::-1]
            if count > 2:
                direction[grouping == group_code] = np.mod(direction[grouping == group_code] + np.pi, 2 * np.pi)
        return direction


    def generate_vonmises(self, position, speed, kappa, opts,
                          time=None, direction=None):
        """Generates trajectories from starting positions and von Mises sampling
        """
        # opt = {"xlim": (-10, 10), "ylim": (-10, 10), "spacing":2.}
        if not time is None:
            self.time = time
        timestep = self.timestep()
        n = position.n_objects
        if direction is None:
            direction = np.random.uniform(low=0., high=2*np.pi, size=(n,))
        self.x = np.zeros((len(self.time), n))
        self.y = np.zeros((len(self.time), n))
        self.n_objects = n
        step = speed * timestep
        self.x[0, :] = position.x
        self.y[0, :] = position.y
        for frame in range(1, len(self.time)):
            # check boundary
            direction_old = direction.copy()
            direction = self.bounce_square(position, direction, opts)
            # check collisions
            direction_old = direction.copy()
            direction = self.bounce_objects(position, direction, opts)

            position.move((np.sin(direction) * step, np.cos(direction) * step))

            tx = self.x[frame - 1, :] + np.sin(direction) * step
            ty = self.y[frame - 1, :] + np.cos(direction) * step

            # store coordinates
            self.x[frame, :] = tx
            self.y[frame, :] = ty
            # update direction
            direction += np.random.vonmises(mu=0, kappa=kappa, size=direction.shape)
        return self


if __name__ == "__main__":
    # execute only if run as a script
    pass
