# motbox

Python code for preparing and presenting [Multiple Object Tracking](http://www.scholarpedia.org/article/Multiple_object_tracking) experiments. You can use it separately or do some parts in R using [motrack package](https://github.com/jirilukavsky/motrack). 

## How to use it

This package can be used either as a controller for psychopy objects (see `Pupeteer` class in `motbox.control`) or as a generator for paths. These generated paths can then be loaded and used for controlled, pre-reandomised administration of tracks.

### Psychopy
Look inside the `examples` folder for an example of [PsychoPy](https://www.psychopy.org/) integration. 

Currently the package is tested and working with PsychoPy 1.9 and Python 2, and PsychoPy 3.2.4 and Python 3.

### Generators
Path generation can be done either by your own scripts using the `Position` class to generate starting positions and `Track` to then `generate_trajectory`, or there are some shorthand functions in the `motbox.generator` file.

### Visualisations
the `motbox.visualisaions` contains function `plot` allowing to plot position data and/or trajectory data and a function `trajectory_video` which makes a video out of a valid `Trajectory` object.

### Command line
Installation of the package comes with some command line options to generate tracks. If you have installed the package with pip, you can do following commands from command line:

`generate-straight-trajectory --help`

## Code revision

Use `pylint motbox/*.py` or `pylint motbox/yourfile.py`

## Unit tests

Use `python -m unittest discover test` at top folder level.

Running a single test is also possible `python -m unittest test.test_track.TestTrack.test_generate_vonmises.` But beware that the test file includes COMPLETE parameter which by defaults skips those functionw which take a long time to finish (video or track generations).