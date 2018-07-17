import numpy as np
from matplotlib import collections as mc
import motbox

if __name__ == "__main__":
    # execute only if run as a script
    n = 5
    #P1 = Position()
    timescale = np.arange(0., 2.5, 0.13)
    radius = 2.5
    opts = {"xlim": (-10, 10), "ylim": (-10, 10), "spacing":2.}
    offset = 3.
    arena_width = 20.
    def anotate(ax):
        ax.annotate(  "1", xy=(-arena_width-2*offset,  0.),
        horizontalalignment='center', verticalalignment='center', color="blue")
        ax.annotate(  "2", xy=(                   0.,  0.),
        horizontalalignment='center', verticalalignment='center', color="blue")
        ax.annotate(  "4", xy=(+arena_width+2*offset,  0.),
        horizontalalignment='center', verticalalignment='center', color="blue")
        ax.annotate(  "8", xy=(-arena_width-2*offset,  -arena_width-2*offset),
        horizontalalignment='center', verticalalignment='center', color="blue")
        ax.annotate( "64", xy=(                   0.,  -arena_width-2*offset),
        horizontalalignment='center', verticalalignment='center', color="blue")
        ax.annotate("128", xy=(+arena_width+2*offset,  -arena_width-2*offset),
        horizontalalignment='center', verticalalignment='center', color="blue")
        sx = +1.5*arena_width+3*offset - 5
        sy =  0.5*arena_width+1*offset - 0
        tick = 0.5
        step = 5
        lines = [[(sx, sy), (sx + step, sy)],
                 [(sx, sy), (sx, sy + tick)],
                 [(sx + step, sy), (sx + step, sy + tick)],
                 [(sx + 2 * step, sy), (sx + 2 * step, sy + tick)],
                 [(sx + step, sy), (sx + 2 * step, sy)]
                 ]
        lc = mc.LineCollection(lines, colors="black", linewidths=1)
        ax.add_collection(lc)
        ax.annotate('5"', xy=(sx + step,  sy + 1),
        horizontalalignment='center', verticalalignment='bottom', color="black")
        ax.annotate('10"', xy=(sx + 2 * step,  sy + 1),
        horizontalalignment='center', verticalalignment='bottom', color="black")

    T1 = motbox.Track().generate_vonmises(
        motbox.Position().circular_positions(n, radius),
        5.,
        1,
        opts=opts,
        time = timescale,
        direction = np.arange(n, dtype=float) / n * (2 * np.pi))
    T2 = motbox.Track().generate_vonmises(
        motbox.Position().circular_positions(n, radius),
        5.,
        2,
        opts=opts,
        time = timescale,
        direction = np.arange(n, dtype=float) / n * (2 * np.pi))
    T3 = motbox.Track().generate_vonmises(
        motbox.Position().circular_positions(n, radius),
        5.,
        4,
        opts=opts,
        time = timescale,
        direction = np.arange(n, dtype=float) / n * (2 * np.pi))
    T4 = motbox.Track().generate_vonmises(
        motbox.Position().circular_positions(n, radius),
        5.,
        8,
        opts=opts,
        time = timescale,
        direction = np.arange(n, dtype=float) / n * (2 * np.pi))
    T5 = motbox.Track().generate_vonmises(
        motbox.Position().circular_positions(n, radius),
        5.,
        64,
        opts=opts,
        time = timescale,
        direction = np.arange(n, dtype=float) / n * (2 * np.pi))
    T6 = motbox.Track().generate_vonmises(
        motbox.Position().circular_positions(n, radius),
        5.,
        128,
        opts=opts,
        time = timescale,
        direction = np.arange(n, dtype=float) / n * (2 * np.pi))
    T1.move((-arena_width-2*offset,  0.))
    T2.move((  0.,  0.))
    T3.move(( arena_width+2*offset,  0.))
    T4.move((-arena_width-2*offset, -arena_width-2*offset))
    T5.move((  0., -arena_width-2*offset))
    T6.move(( arena_width+2*offset, -arena_width-2*offset))
    TT = motbox.Track()
    TT.time = T1.time
    TT.n_objects = 6 * T1.n_objects
    TT.x = np.concatenate((T1.x, T2.x, T3.x, T4.x, T5.x, T6.x), axis=1)
    TT.y = np.concatenate((T1.y, T2.y, T3.y, T4.y, T5.y, T6.y), axis=1)
    print(TT.summary())
    xlim = (-1.5*arena_width-3*offset - 5, 1.5*arena_width+3*offset + 5)
    ylim = (-1.5*arena_width-3*offset, 0.5*arena_width+1*offset + 5)
    TT.plot("demo_kappa.png", xlim = xlim, ylim = ylim)
    TT.make_video("demo_kappa.mp4", xlim = xlim, ylim = ylim, callback=anotate)
    pass
