import matplotlib.pyplot as plt
import numpy as np
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage


def plot(x, y, filename, xlim=(-10, 10), ylim=(-10, 10)):
    """Plots trajectories into a file. Uses matplotlib

    Parameters
    -----------
    x : array of float
        x coordinates
    y : array of float
        y coordinates
    filename: str
        filename for the plot o be saved into
    xlim: touple of float
        x plot limits
    ylim : touple of float

    Returns
    -------
    Saves a png file of name filename into the working directory
    """
    plt.figure()
    plt.plot(x, y, "k")
    plt.xlabel = "x"
    plt.ylabel = "y"
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.savefig(filename)


def trajectory_video(trajectory, filename, xlim=(-10, 10), ylim=(-10, 10), callback=None, axisOff=True):
    """Create video of the track and saves it in working directory

    Parameters
    ---------
    filename : string
        name of the file to be saved into
    xlim : touple(2) of float
        xlimits of the fideo
    ylim : touple(2) of float
        ylimits of the video
    callback:
        what to
    axisOff : bool

    Returns
    --------
    saved mp4 video at fiven filepath
    """
    WIDTH = 900
    HEIGHT = 600
    DPI = 150
    FPS = 25
    DURATION = np.max(trajectory.time) - np.min(trajectory.time)

    fig, axis = plt.subplots(figsize=(1.0 * WIDTH / DPI, 1.0 * HEIGHT / DPI), dpi=DPI)

    def make_frame(t):
        axis.clear()
        (tx, ty) = trajectory.position_for_time(t + np.min(trajectory.time))
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
