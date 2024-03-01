import geojson

def convertir_geojson(donnees):
    features = []
    for maison in donnees:
         if 'lat' in maison and 'lon' in maison and maison['lat'] is not None and maison['lon'] is not None:
            feature = geojson.Feature(
                geometry=geojson.Point((maison["lon"], maison["lat"])),
                properties={'popup': maison["popup"]}
            )
            features.append(feature)

    monJson = geojson.FeatureCollection(features)
    return geojson.dumps(monJson, sort_keys=True)