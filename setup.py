"""Setup file for the motbox
"""

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="motbox",
    version="0.1.0",
    author="Jiri Lukavsky",
    author_email="lukavsky@praha.psu.cas.cz",
    description="Package for moving object track generation and control from psychopy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jirilukavsky/motbox",
    packages=setuptools.find_packages(),
    install_requires=[
      'numpy>=1.16',
      'moviepy',
      'matplotlib',
      'scipy',
      'click'
    ],
    entry_points={
      'console_scripts': [
        'generate-straight-trajectory = motbox.commands:generate_straight_trajectory',
      ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
