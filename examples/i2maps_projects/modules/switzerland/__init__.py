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
import i2maps, i2maps.db
import os

dbfile = 'data' + os.sep + 'switzerland/switzerland.db'
db = i2maps.db.Sqlite(i2maps.projects_directory + os.sep +  dbfile)

def cantons():
    cantons = db.dict_query("""SELECT abbr, the_geom FROM cantons""")
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

