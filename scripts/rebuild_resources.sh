#!/bin/bash
#
# Run supporting pyrcc files to generate resource files and future
# designer conversions into python code. Run this from the home project
# directory like:
# BlueGraph % ./scripts/rebuild_resources.sh

pyside-rcc \
    bluegraph/assets/bluegraph_resources.qrc \
    -o bluegraph/assets/bluegraph_resources_rc.py

