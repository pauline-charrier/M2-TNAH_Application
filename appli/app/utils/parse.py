import geojson

def convertir_geojson(donnees):
    """
    Convertit une liste de données au format spécifique en GeoJSON.

    Parameters
    ----------
    donnees : list
        Liste de maisons avec des informations géographiques et thématiques.

    Returns
    -------
    str
        GeoJSON représentant les maisons avec leurs informations géographiques et thématiques.

    Notes
    -----
    La fonction filtre les maisons ayant des coordonnées valides (lat, lon non nuls) et un domaine défini.

    Les propriétés de chaque 'feature' incluent le texte à afficher dans une popup, le domaine de génie, les multilabels, le genre et la date de naissance de la personne associée.
    """
    features = []
    for maison in donnees:
         # Vérifie si la maison a des coordonnées valides et un domaine défini.
         if 'lat' in maison and 'lon' in maison and maison['lat'] is not None and maison['lon'] is not None and maison['domaine'] is not None:
            # Crée une feature GeoJSON pour chaque maison.
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
    
    # Crée un objet GeoJSON FeatureCollection à partir des features.
    monJson = geojson.FeatureCollection(features)
    # Retourne le GeoJSON sous forme de chaîne JSON, trié par clés.
    return geojson.dumps(monJson, sort_keys=True)