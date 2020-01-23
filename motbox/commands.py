import os
import click
from motbox.generator import generate_straight_trajectory as gst

@click.command()
@click.argument('path', type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.option('-f', '--filename', default='track', type=str)
@click.option('-n', '--n', default=1, type=int)
@click.option('-s', '--speed', default=1, type=float)
@click.option('-fr', '--frequency', default=10, type=int)
@click.option('-x', '--xlim', default=(-10,10), type=(float, float))
@click.option('-y', '--ylim', default=(-10,10), type=(float, float))
@click.option('-t', '--time', default=5, type=float)
@click.option('--plot', default=False, type=bool)
@click.option('--video', default=False, type=bool)
def generate_straight_trajectory(path, filename, n, speed, time, frequency, xlim, ylim, plot, video):
	filepath = os.path.join(path, filename)
	click.echo(f'Saving to {filepath}.csv')
	gst(n=n, speed=speed, time=time, frequency=frequency,
    xlim=xlim, ylim=ylim, save=True, path=path, filename=filename, plot=plot, video=video)
