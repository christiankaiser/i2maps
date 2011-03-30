# Simple example PostGIS layer for demonstration purposes.
# Load this table into the PostGIS database i2maps, and access the data
# through the postgis_layer.py datasource

CREATE TABLE example_layer (
	id INTEGER PRIMARY KEY,
	the_geom GEOMETRY,
	val VARCHAR(60)
);

INSERT INTO example_layer VALUES (1, ST_GeomFromEWKT('SRID=4326;POINT(-7.4 54.4)'), 'Point 1');
INSERT INTO example_layer VALUES (2, ST_GeomFromEWKT('SRID=4326;POINT(-6.9 54.6)'), 'Point 2');
INSERT INTO example_layer VALUES (3, ST_GeomFromEWKT('SRID=4326;POINT(-6.2 52.1)'), 'Point 3');
INSERT INTO example_layer VALUES (4, ST_GeomFromEWKT('SRID=4326;POINT(-9.1 53.2)'), 'Point 4');
INSERT INTO example_layer VALUES (5, ST_GeomFromEWKT('SRID=4326;POINT(-8.5 53.9)'), 'Point 5');
