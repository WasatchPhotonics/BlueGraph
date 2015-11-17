import os

from setuptools import setup, find_packages

# These will break the travis build. 
#here = os.path.abspath(os.path.dirname(__file__))
#with open(os.path.join(here, "README.txt")) as f:
#    README = f.read()
#with open(os.path.join(here, "CHANGES.txt")) as f:
#    CHANGES = f.read()

README=""
CHANGES=""

requires = [
    "nose",
    "coverage",
    "pyside",
    ]

setup(name="bluegraph",
      version="0.0",
      description="bluegraph",
      long_description=README + "\n\n" + CHANGES,
      classifiers=[],
      author="",
      author_email="",
      url="",
      keywords="",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite="bluegraph",
      install_requires=requires,
      )
