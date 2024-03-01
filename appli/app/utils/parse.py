import geojson

def convertir_geojson(donnees):
    features = []
    for maison in donnees:
         if 'lat' in maison and 'lon' in maison and maison['lat'] is not None and maison['lon'] is not None and maison['domaine'] is not None:
            feature = geojson.Feature(
                geometry=geojson.Point((maison["lon"], maison["lat"])),
                properties={'popup': maison["popup"], 
                            'domaine': maison["domaine"], 
                            'museeFrance' : maison["museeFrance"], 
                            'monClasse' : maison["monClasse"], 
                            'monInscrit' : maison["monInscrit"],
                            'genre' : maison["genre"],
                            'ddn_pers' : maison["ddn_pers"]
                            }
            )
            features.append(feature)

    monJson = geojson.FeatureCollection(features)
    return geojson.dumps(monJson, sort_keys=True)