import os
import numpy as np
from motbox import Track, Position


def generate_straight_trajectory(path, filename='track', n=1, speed=1, time=5, frequency=10, xlim=(-10,10), ylim=(-10,10), plot=False, video=False):
	"""Generates straight trajectory at random starting points.
	Saves trajectory as a csv, and then saves a plot and video if wanted

	Parameters
	----------
	filename : str ('track')
		name of the file to be prepended to csv, plot and video files
	n : int
		number of objects to be moved
	speed : float or tuple of floats
		how far will the object move each "tick". Dependent on the length of the time parameter. If touple, it needs to have the same length as
		is the number of positions. Allows separate speeds to be applied to each object. e.g. (speed for first object, speed for second, etc.)
	time : float
		time of the 
	frequency : int
		frequency at which to 
	xlim : tuple of floats (-10, 10)
		limits of the box in which the objects move
	ylim : tuple of floats (-10, 10)
		limits of the box in which the objects move 
	plot : bool (False)
		if the plot of the trajectory should be created
	video : bool (False)
		if the video of the trajectory should be created

	Return
	--------
	Saves .csv file at location 

	See Also
	---------
	This function is basically just a wrapper around motbox.Track.generate_tracjectory
	"""
	filepath = os.path.join(path, filename)
	## generate random start
	position = Position()
	position.random_positions(n, xlim, ylim, 1)

	## generate path
	track = Track()
	track.generate_trajectory(position, speed, {"xlim": xlim, "ylim": ylim, "spacing": 1}, time = np.arange(0, time, 1/frequency))
	track.save_to_csv(f'{filepath}.csv')

	## generate image and video
	if plot: track.plot(f"{filepath}.png", xlim, ylim)
	if video: track.make_video(f"{filepath}.mp4", xlim, ylim)
 