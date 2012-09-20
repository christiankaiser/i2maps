pico.get('../media/js/i2maps.js');
pico.load('weather.sensors');
pico.load('weather.model');


var map, infobox, sensors, sensors_layer, surface, 
    surface_layer, cm, timeline, colorbar = null;
var sensors_data = {};
var sensor_measurements = {};
var GOOGLE_MAPS_API_KEY = 'ABQIAAAAnfs7bKE82qgb3Zc2YyS-oBT2yXp_ZAY8_ufC3CFXhHIE1NvwkxSySz_REpPq-4WZA27OwgbtyR3VcA';

pico.main = function() {   
    sensors = weather.sensors;
    model = weather.model;
    
    map = new i2maps.Map('map', {
        baseLayers: [
            'Open Street Map', 'No Base Layer'
        ],
    });
    
    sensors_layer = new i2maps.VectorLayer('Sensors');
    map.addLayer(sensors_layer);
    
    sensors_layer.style_function = function(id, selected) {
        var data = sensor_measurements[id];
        if (!data) return {'display': 'none'};
        return {
            'pointRadius': 15,
            'fillColor': cm(data.t).html(),     // colormap cm will be created later
            'fontSize': '11px',
            'strokeColor': '#000000',
            'strokeWidth': (selected ? 2 : 0.5),
            'label': data.t.toFixed(1),
        }
    };
    
    infobox = new i2maps.InfoBox('info', 'Info');
    sensors_layer.select_function = function(id) {
        // Update the info box:
        infobox.update({
            'Id': id,
            'Value': sensor_measurements[id].t + ' &deg;C',
            'Time': sensor_measurements[id].time,
            'Type': 'Temperature Sensor',
            'Name': sensors_data[id].name,
            'Elevation': sensors_data[id].elevation + ' metres'
        });
        // Update the timeline:
        sensors.timeline(id, function(data){timeline.update(data)});
    };
    
    timeline = new i2maps.Timeline('timeline', {timespan: '1 week'});
    
    sensors.sensors(function(data) {
        sensors_data = data;
        sensors_layer.setGeometries(sensors_data, 'geometry');
        $('#loading').css('visibility', 'hidden');
    });
    
    // Register for the time change event (fired when the user clicks inside
    // the timeline).
    i2maps.events.register("timechange", function(time){
        sensors.measurements(time, function(data){
            sensor_measurements = data;
            sensors_layer.redraw();
        });
    });
    
    
    // Add a raster layer for the temperature surface
    surface_layer = new i2maps.RasterLayer('Temperature Surface');
    map.addLayer(surface_layer);
    
    // Add another time change listener
    i2maps.events.register('timechange', function(time) {
        model.surface(time, function(data) {
            surface = data;
            surface_layer.setGeometry(surface.bbox, surface.shape);
            surface_layer.update();
        })
    });
    
    // Style the temperature surface
    cm = i2maps.colormap.jet(0, 25);    // colormap for temperature between 0 and 25 degrees; enough for Ireland
    surface_layer.draw_function = function(x,y){
        var v = surface.data[y][x];
        return cm(v, [0,0,0,0]);    // Transparent color for out-of-range values.
    };
    
    // When clicking on the raster layer, we want to display the timeline for
    // this location, and update the infobox also.
    surface_layer.select_function = function(x, y, lat, lon) {
        model.timeline(lat, lon, function(data){timeline.update(data)});
        infobox.update({
            'Location': [Math.round(lat), Math.round(lon)],
            'Value': surface.data[y][x].toFixed(1) + ' &deg;C',
            'Type': 'Temperature Prediction',
        });
    };
    
    colorbar = new i2maps.ColorBar('legend', 'Temperature', cm, ' &deg;C');
    surface_layer.hover_function = function(x, y){
        var value = surface.data[y][x];
        if (value > 0) colorbar.update(value);
    }
    
    // Fire a time change event manually in order to load the measurements
    i2maps.events.trigger("timechange", null);
}


