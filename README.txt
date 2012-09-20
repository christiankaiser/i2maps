A framework for building dynamic spatial data driven web applications

#Features

An integrated server & client framework

Server side (Python):
* Python database API with convenience functions
* Spatio-Temporally referenced Numpy arrays for raster data
* Automatic conversion of data formats (Geometries, Dates/Times, Numbers):
  * Python to/from Javascript
  * Python to/from database (Postgres, Sqlite)
* Spatial regression modeling method
* Standalone Python development server
* Easily extendable with custom Python modules

Client side (Javascript):
* OpenLayers based map control
* High level classes for creating data driven vector and raster layers
* Timeline control
* Event system
* Simple mechanism for calling Python functions from Javascript


#How to try it out?

Several examples are inside the example folder. There is also an example script to run the i2maps server. Just cd into the examples folder, and run the server by typing 'python run.py'. This will launch the i2maps server on port 8800, and you will be able to navigate in your browser to http://localhost:8800.

Currently, 3 examples are inside the examples folder:
* hello_world: go to http://localhost:8800/hello_world/ to see it. It is a minimalistic i2maps example featuring 'random' points on a world map
* switzerland: shows a thematic map of population density for the 26 Swiss cantons. Navigate to http://localhost:8800/switzerland/ to see it.
* weather: an interactive weather application featuring temperature sensors and an interpolated temperature raster for a whole week for Ireland. You will need to compute the interpolation for each time step first by running first the Python script in i2maps_projects/modules/weather/model/run.py This will create approximately 140 MB of data, and takes roughly 10 minutes to calculate. After, navigate to http://localhost:8800/weather to see the live application.


#Documentation

Just start the i2maps server, go to http://localhost:8800 and follow the links to the documentation. Alternatively, the HTML files can be found in i2maps/docs.
