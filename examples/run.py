#!/usr/bin/env python
"""
This is an example script for running the i2maps development server.
It should allow the interested developer to quickly check out the projects
inside the i2maps_projects directory inside the examples directory.
To run the server, simply run this script and then go to 
http://localhost:8800 to see i2maps at work.
"""


# A minimal run.py file would be something like:
#
# import i2maps.server
# i2maps.projects_directory = '/home/user/i2maps_projects'
# i2maps.server.run()
# 
# We complicate things a bit for more flexibility and ease of use

import os, sys

# Try to import i2maps. If it is not installed, we assume we are still inside
# the downloaded i2maps directory structure and try to include the path
# to the library.
try:
    import i2maps.server
except:
    i2maps_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.sep + '..' + os.sep)
    sys.path.append(i2maps_dir)
import i2maps.server    # Import again in case we had an exception
print "Using the i2maps libary at %s" % (os.path.dirname(os.path.abspath(i2maps.__file__)),)

# Define the projects directory (you could set this manually to an absolute 
# path, e.g. /home/user/i2maps_directory/ - don't forget the trailing slash)
i2maps.projects_directory = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'i2maps_projects' + os.sep

# Run the development server
i2maps.server.run()


