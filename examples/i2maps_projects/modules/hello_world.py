"""
This is an example i2maps Python module that can be called directly from
the Javascript code. In this code, we simply read an existing JSON file
and send it to the Javascript frontend. The JSON file contains simply a few
points to be displayed.
In a real case, you will probably want to connect to a database like PostGIS
or SQLite, or do some computation before sending the geometries (or other
values such as attributes) to the Javascript frontend. This is demonstrated
in another example.
"""

import pico     # We need this in every case
import i2maps
import json
import os


def random_points():
    datafile = 'data' + os.sep + 'hello_world.json'
    f = open(i2maps.projects_directory + os.sep + datafile)
    points = json.load(f)
    f.close()
    return points

