import numpy as np
import timeit

class Track:
    def __init__(self):
        self.x = None
        self.y = None
        self.time = None
        self.n_objects = 0
        pass

    def load_from_csv_v0(self, filename):
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
        nrow = len(self.time)
        at   = self.time.reshape((nrow, 1))
        axy  = np.zeros((nrow, 2 * self.n_objects))
        axy[:, 0::2] = self.x
        axy[:, 1::2] = self.y
        mat = np.concatenate((at, axy), axis = 1)
        np.savetxt(filename, mat, delimiter="\t")

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def scale(self, f):
        self.x *= f
        self.y *= f

    def timestep(self):
        return np.mean(np.diff(self.time))

    def time_interpolate(self, newtime):
        n = len(newtime)
        nx = np.zeros((n, self.n_objects))
        ny = np.zeros((n, self.n_objects))
        for o in range(self.n_objects):
            nx[:, o] = np.interp(newtime, self.time, self.x[:, o])
            ny[:, o] = np.interp(newtime, self.time, self.y[:, o])
        self.x = nx
        self.y = ny
        self.time = newtime

    def load_from_csv(self, filename):
        return self.load_from_csv_v0(filename)

    def save_to_csv(self, filename):
        return self.save_to_csv_v0(filename)

    def summary(self):
        if (not self.x is None) and (not self.y is None) and (not self.time is None):
            return "Track: {} objects, time {} - {}".format(self.n_objects, np.amin(self.time), np.amax(self.time))
        else:
            return "Track: NOT initialized"

if __name__ == "__main__":
    # execute only if run as a script
    T = Track()
    fn = "../examples/data/T220.csv"
    fno = "../tmp/T220new.csv"
    T.load_from_csv(fn)
    #print(T.mat.shape)
    print(T.summary())
    print(T.time[4:10])
    print(T.timestep())
    T.save_to_csv_v0(fno)
    print("ok")
    print(T.x[:5,:])
    T.time_interpolate(np.array([0, 0.015, 0.03]))
    print(T.summary())
    print(T.x)
    pass
