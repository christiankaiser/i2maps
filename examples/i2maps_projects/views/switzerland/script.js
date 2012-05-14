pico.get('../media/js/i2maps.js');
pico.load('switzerland');

cantons_popdens = {}

pico.main = function() {
    map = new i2maps.Map('map', {
        baseLayers: ["Open Street Map", "No Base Layer"],
    });
    
    // Show only Switzerland
    map.zoomToExtent(new OpenLayers.Bounds(660000, 5750000, 1168000, 6075000));

    // Create a new vector layer for the cantons
    cantons_layer = new i2maps.VectorLayer("Cantons");
    
    // Create a colormap for the population density by providing the class limits
    // The second argument is the default color in case of no data
    pop_colormap = i2maps.colorbrewer.oranges5([0.2,1,2,5,10,52], [255,255,255]);
    
    // Define the style function; the fill color comes from the colormap
	cantons_layer.style_function = function(id, selected) {
	    data = cantons_popdens[id];
	    if (data) {
	        var v = pop_colormap(data.pop_dens);
	        return {
	            'fillColor': v.html(),
	            'stroke': 0,
	            'fillOpacity': 0.7,
	        }
	    } else {
	        return {
	            'fillColor': "#ffffff",
	            'stroke': 0,
	            'fillOpacity': 0,
	        }
	   }
	}
    map.addLayer(cantons_layer);
    
    // Retrieve the geometries from the Python function cantons
    switzerland.cantons(function(data) {
        cantons_layer.setGeometries(data);
    });
    
    // Retrieve the population density from Python
    switzerland.population_density(function(data) {
	    cantons_popdens = data;
	    cantons_layer.redraw();
	});
	
	// Create the legend
	legend = new i2maps.InfoBox('legend', 'Legend');
	legend.update(pop_colormap.legend(1, "[persons / ha]"));
	
}