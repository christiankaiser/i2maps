"""
This is an example i2maps Python module that can be called directly from
the Javascript code. In this example we connect to a SQLite database and
send the geometries and population values to the Javascript front end.
In a real case, you will probably want to do some computation before sending 
the geometries (or other values such as attributes) to the Javascript front end. 
"""

import pico     # We need this in every case
import i2maps, i2maps.db
import json     # For reading GeoJson file
import os

dbfile = '/data/switzerland/switzerland.db'
db = i2maps.db.Sqlite(i2maps.projects_directory + dbfile)

def cantons():
    cantons = db.dict_query("""SELECT abbr, the_geom FROM cantons""")
    return cantons

def cantons_from_geojson():
    """
    Does the same thing as function cantons, except that it reads directly
    from a GeoJson file instead of the SQLite database. GeoJson file is already
    in Google Mercator projection (EPSG:900913)
    We need to return a dictionary where the keys are the abbreviation of the
    cantons, and the values the geometries as GeoJSON dictionary
    """
    fp = open(i2maps.projects_directory + '/data/switzerland/cantons.geojson')
    fc = json.load(fp)
    cantons = {}
    for feat in fc['features']:
        cantons[feat['properties']['Abbr']] = feat['geometry']
    fp.close()
    return cantons

def population_density(year=None):
    if year is None:
        rows = db.query("""SELECT MAX(pop_year) FROM cantons_pop""")
        year = rows.fetchone()[0]
    pop_dens = db.dict_query("""SELECT cantons_pop.abbr, pop_year, 
            pop, pop / area_ha AS pop_dens
        FROM cantons_pop JOIN cantons ON cantons_pop.abbr = cantons.abbr
        WHERE pop_year = ?""", (year,))
    # Note that in a Sqlite query the placeholder for a variable value is ?
    # (it would be %s in Postgres)
    return pop_dens

