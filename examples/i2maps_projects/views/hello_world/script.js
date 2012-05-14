pico.get('../media/js/i2maps.js');
pico.load('hello_world');

var map, poi_layer;     // Global variables.

pico.main = function() {
    map = new i2maps.Map('map', {
        baseLayers: ["Open Street Map", "No Base Layer"],
    });
    map.zoomToExtent(new OpenLayers.Bounds(-15000000, -5000000, 18000000, 8500000));
    poi_layer = new i2maps.VectorLayer("POIs");
    map.addLayer(poi_layer);
    
    hello_world.random_points(function(data) {
        poi_layer.setGeometries(data);
    });
}
