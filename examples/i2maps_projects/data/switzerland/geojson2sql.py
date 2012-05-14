#!/usr/bin/env python
"""
Reads the cantons.geojson file and outputs the SQL code needed to
fill the SQLite database.
"""

import json
import os, sys
import shapely.geometry, shapely.wkb


def db_structure():
    print """DROP TABLE IF EXISTS cantons;"""
    print """CREATE TABLE cantons (
        geocode INT PRIMARY KEY,
        name VARCHAR(50),
        abbr VARCHAR(2),
        the_geom GEOMETRY,
        area_ha DOUBLE
    );"""
    print """CREATE UNIQUE INDEX cantons_abbr ON cantons (abbr);"""

def convert(path):
    f = open(path)
    fc = json.load(f)
    f.close()
    feats = fc['features']
    for f in feats:
        geom = shapely.geometry.asShape(f['geometry'])
        print """INSERT INTO cantons (geocode, name, abbr, the_geom, area_ha) VALUES (%i, '%s', '%s', '%s', '%f');""" % (
            f['properties']['Geocode'], f['properties']['Name'], 
            f['properties']['Abbr'], shapely.wkb.dumps(geom).encode('hex'), 
            f['properties']['Area_ha']
        )

if __name__=='__main__':
    if len(sys.argv) < 2:
        print("Usage: python geojson2sql.py geojson_file")
        sys.exit(0)
    path = sys.argv[1]
    if os.path.exists(path) is False:
        raise Exception("FILE ERROR. '%s' does not exist." % path)
    db_structure()
    convert(path)