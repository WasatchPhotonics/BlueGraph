# BlueGraph
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

