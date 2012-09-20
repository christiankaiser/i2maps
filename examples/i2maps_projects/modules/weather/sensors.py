import i2maps
import i2maps.db
import pico
from datetime import timedelta

db = i2maps.db.Sqlite(i2maps.projects_directory + 'data/weather/temperature.db')

def sensors():
    """
    Returns the ID, name, elevation and point geometry of all sensors.
    """
    sensors = db.dict_query('SELECT id, geometry, name, elevation FROM sensors')
    # Sensors are in WGS84 (EPSG:4326) in the database.
    # We need to transform the coordinates to Google Mercator (EPSG:900913),
    # which is the SRS of the OpenLayers map
    for c in sensors:
        sensors[c]['geometry'].set_srid(4326)
        sensors[c]['geometry'].transform(900913)
    return sensors

def measurements(time=None, time_window=30):
    """
    Returns all available measurements at a given time (None means latest
    measurements), plus/minus a time window (30 minutes by default).
    """
    if time is None:    # Query the database to get time of latest measurement
        time = db.query('SELECT MAX(time) FROM measurements').fetchone()[0]
    from_time = time - timedelta(minutes=time_window)
    to_time = time + timedelta(minutes=time_window)
    measurements = db.dict_query('''SELECT sensor_id, time, 
        AVG(temperature) AS t FROM measurements WHERE time > ? AND time < ?
        GROUP BY sensor_id''', [from_time, to_time])
    return measurements

def timeline(sensor_id):
    """
    Returns all measurements for one particular sensor.
    """
    timeline = db.dict_query('''SELECT time, temperature FROM measurements
        WHERE sensor_id = ? ORDER BY time''', [sensor_id])
    return timeline



