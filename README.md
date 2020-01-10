# motbox

Python code for preparing and presenting [Multiple Object Tracking](http://www.scholarpedia.org/article/Multiple_object_tracking) experiments. You can use it separately or do some parts in R using [motrack package](https://github.com/jirilukavsky/motrack). 

## How to use it

Look inside the `examples` folder for an example of [PsychoPy](https://www.psychopy.org/) integration.

Currently the package is tested and working with pscyhopy 1.9 and Python 2.

## Code

Use `pylint motbox/*.py` or `pylint motbox/yourfile.py`

## Unit tests

Use `python -m unittest discover test` at top folder level.

Running a single test is also possible `python -m unittest test.test_track.TestTrack.test_generate_vonmises.` But beware that the test file includes COMPLETE parameter which by defaults skips those functionw which take a long time to finish (video or track generations).