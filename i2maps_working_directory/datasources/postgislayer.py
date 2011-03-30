import i2maps.datasources
import i2maps.settings as settings

class Postgislayer(i2maps.datasources.Custom):
    def __init__(self):
        self.ds = i2maps.datasources.new({
            "type": "postgres",
            "database": "i2maps",
            "user": "postgres",
            "password": "",
            "host": "localhost"
        })
    
    def layer(self, options={}):
        print options
        return self.ds.feature_query("""SELECT st_transform(the_geom, 900913) AS geometry, val 
            FROM example_layer""")
    

