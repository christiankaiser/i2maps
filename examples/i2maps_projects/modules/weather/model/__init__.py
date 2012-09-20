import i2maps
import i2maps.algorithms.krls
import i2maps.algorithms.kernel
import i2maps.raster_cube
import i2maps.spatial_array
import pico

import numpy as np

path = __path__[0] + '/'
filename = path + 'ireland_temperature'

@pico.private 
def update(measurements, time):
    """
    Computes a raster surface from the sensors for a given time step.
    It uses an interpolation method based on kernel regression, where the
    digital elevation model is also taken into account.
    """
    measurements = np.array(measurements)
    data = measurements[:,0:3] # array of [lat, lon, elevation]
    targets = measurements[:,3] # array of corresponding temperature values
    
    # Setup the KRLS (Kernel Recursive Least Squares method)
    params = dict(adopt_thresh=0.01, dico_max_size=100)
    kernel = i2maps.algorithms.kernel.Gaussian(np.array([70000, 70000, 155.5])) 
    model = i2maps.algorithms.krls.KRLS(kernel, params)
    
    # Train the model (sample by sample)
    for i in range(0, len(data)):
        model.update(np.array(data[i, :]), np.array(targets[i]))
    
    # Do the full grid prediction for this timestep now and save it
    dem = i2maps.spatial_array.load(path + 'dem')
    dem_points = dem.items()
    output = model.query(dem_points).tolist()
    predicted = np.array(output).reshape(dem.shape)
    predicted[dem == dem.nodata] = dem.nodata
    
    # Open the raster cube
    try:
        raster_cube = i2maps.raster_cube.load(filename)
    except Exception, e:
        print(e)
        print("Creating new RasterCube")
        #shape = (height, width, num_timesteps)
        shape = (372, 282, 24*7)
        #envelope = [[min_y, max_y], [min_x, max_x], [min_t, max_t]]
        envelope = [[7436000.0, 6692000.0], [-1168000.0, -604000.0], [0, 0]] 
        raster_cube = i2maps.raster_cube.RasterCube(filename=filename, shape=shape, envelope=envelope)
    
    # Save the prediction surface into the raster cube at time t
    raster_cube.insert(predicted, time)
    
# Retrieve a surface (geo-referenced 2d array) from the Raster Cube
def surface(time=None):
    raster_cube = i2maps.raster_cube.load(filename)        
    surface = raster_cube.surface(time)
    return surface

# Retrieve a timeline for a given lat, lon
def timeline(geo_x, geo_y):
    raster_cube = i2maps.raster_cube.load(filename)
    return raster_cube.timeline(geo_x, geo_y)


