# BlueGraph
[![Build Status](https://travis-ci.org/WasatchPhotonics/BlueGraph.svg?branch=master)](https://travis-ci.org/WasatchPhotonics/BlueGraph) [![Coverage Status](https://coveralls.io/repos/WasatchPhotonics/BlueGraph/badge.svg?branch=master&service=github)](https://coveralls.io/github/WasatchPhotonics/BlueGraph?branch=master)
high speed graphing and logging with guiqwt and zmq. SVG blueness in pyqt.

This is a rewrite of the internal "ExtendedTest" interface, and should
look like this:

![BlueGraph Screenshot] (/docs/BlueGraph.gif "BlueGraph screenshot")


Getting Started
---------------

- cd <directory containing this file>

- $VENV/bin/python setup.py develop

- $VENV/bin/nosetests --cover-erase --with-coverage --cover-package=bluegraph

- $VENV/bin/python scripts/bluegraph_demo.py

Development Setup
-----------------

Ideally the fonts could be embedded in the svg file, then addressed
during the text update procedure of the interface creation in python.
The workaround for now is to install the fonts in assets/fonts on your
system, then load the svg files. The text designators are deleted at
runtime, and replaced with QGraphicsTextItems.

Apparently the way nosetests works may be importing all of the existing
tests into one module, then running them. This in turn will create
duplicate log prints, unexpected re-use of qapplication and other issues
associated with the runner. Only define a log handler in the
alphabetically first test procedure. Catch qapplication re-define
runtime errors in the test_views, after it has already been established
in the alphabetically preceeding test_controller.

