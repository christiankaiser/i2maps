"""
Runs the temperature surface interpolation algorithm.
It is doing it by retrieving the latest temperature measurements from the
database, and then by interpolating the temperature for each hour for a whole
week. All the results will be stored in a spatial array, which is saved in two
files: ireland_temperature.npy and ireland_temperature.json.
The computation takes some while (around 10 minutes depending on your computer), 
and the output files will be around 140 MB.
"""

import datetime, sys, time
from os.path import abspath, dirname

# In the following section we need to setup the Python environment.
# If we have installed i2maps and pico properly somewhere on the Pythonpath,
# we can simply import these two modules. If however we are running them just
# from inside the downloaded i2maps package, we need to add the folder 
# containing i2maps and pico to the Pythonpath. We therefore assume that the
# project directory structure is still intact.

proj_dir = abspath(dirname(abspath(__file__)) +'/../../../') + '/'

# Try to import i2maps. If it is not installed, we assume we are still inside
# the downloaded i2maps directory structure and try to include the path
# to the library.
try:
    import i2maps
except:
    i2maps_dir = abspath(proj_dir +'../../') + '/'
    sys.path.append(i2maps_dir)

import i2maps    # Import again in case we had an exception
i2maps.projects_directory = proj_dir
print "Using the i2maps libary at %s" % (dirname(abspath(i2maps.__file__)),)

# Because we don't want to run the i2maps server, we need to do some more setup.
# We need to define the modules directory, and include it in the Python path if
# necessary.
i2maps.modules_directory = i2maps.projects_directory + 'modules/'
if i2maps.modules_directory not in sys.path: 
    sys.path.insert(0, i2maps.modules_directory)

# Now the i2maps should be imported and its parent directory in the Pythonpath.
# We have also the modules folder in the Pythonpath. We can therefore start
# working normally.

import i2maps.db
import pico

import weather.model as model
import weather.sensors as sensors

db = i2maps.db.Sqlite(i2maps.projects_directory + 'data/weather/temperature.db')


@pico.private
def run_model():
    # Get the information about the sensors
    sens = sensors.sensors()
    # Find the latest measurement time in the database
    max_time = db.query('SELECT MAX(time) FROM measurements').fetchone()[0]
    t = i2maps.datestring_to_datetime(str(max_time))
    # Define the time step, in our case 1 hour
    dt = datetime.timedelta(hours=1)
    # Run the model for each time step for one week
    # This is of course not very efficient, as we should rather first check
    # if we have already computed the time step. But it is enough for 
    # illustration purposes.
    for i in range(0, 24*7):
        m = sensors.measurements(t)
        t -= dt
        data = [[sens[id]['geometry'].x, sens[id]['geometry'].y, sens[id]['elevation'], m[id]['t']] for id in m]
        model.update(data, str(t))
        print '%i of %i hours computed' % (i+1, 24*7)
    


if __name__ == '__main__':
    t0 = time.time()
    run_model()
    print 'Model computed in %f seconds' % (time.time() - t0, )

