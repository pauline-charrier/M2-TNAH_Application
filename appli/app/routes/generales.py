from ..app import app, db
from flask import render_template, request
from sqlalchemy import or_
from ..models.data import Maisons, Personnes, Domaine, Genre
from ..models.formulaires import Recherche
from ..utils.transformations import nettoyage_string_to_int, clean_arg
from ..utils.parse import convertir_geojson


@app.route("/", methods=['GET', 'POST'])
@app.route("/maisons", methods=['GET', 'POST'])
@app.route("/maisons/<int:page>", methods=['GET', 'POST'])
def maisons(page=1):
    form=Recherche()
    donnees = Maisons.query.order_by(Maisons.denomination).paginate(page=page, per_page=app.config["MAISONS_PER_PAGE"])

    return render_template("pages/liste.html", 
        sous_titre="Liste des maisons", 
        donnees=donnees,
        form=form)




@app.route("/maisons/<string:nom_maisons>")
def info_maisons(nom_maisons):
    donnees= Maisons.query.filter(Maisons.denomination == nom_maisons).first()
    print(donnees.idWikidata)
    personne = Personnes.query.filter(Personnes.idWikidata == str(donnees.idWikidata)).first()
    print(personne)

    return render_template("pages/info_maisons.html", 
        sous_titre=nom_maisons, 
        donnees=donnees,
        personne=personne)

@app.route("/personnes", methods=['GET', 'POST'])
@app.route("/personnes/<int:page>", methods=['GET', 'POST'])
def personnes(page=1):

    donnees = Personnes.query.order_by(Personnes.nomIllustre).paginate(page=page, per_page=app.config["MAISONS_PER_PAGE"])

    return render_template("pages/liste_personnes.html", 
        sous_titre="Liste des personnes", 
        donnees=donnees)

@app.route("/carte", methods=['GET'])
def carte():
    maisons = Maisons.query.all()
    donnees = []

    for maison in maisons:
        personne = Personnes.query.filter(Personnes.idWikidata == maison.idWikidata).first()
        donnees.append(
            {
                'lat': maison.latitude,
                'lon': maison.longitude,
                'popup': maison.denomination,
                'domaine': maison.type.value if maison.type else None, 
                'museeFrance':maison.museeFrance, 
                'monClasse' : maison.monumentsClasses,
                'monInscrit' : maison.monumentsInscrits,
                'genre': personne.genre.value if personne and maison.type else None,
                'ddn_pers' : personne.ddn if personne else 0
            }
        )
    
    donnees = convertir_geojson(donnees)
    
    return render_template("pages/carte.html",
        sous_titre="Carte",
        donnees = donnees)

#En cours d'adaptation pour les graphiques : corriger les noms des étiquettes
@app.route("/graphiques/graph1", methods=['GET', 'POST'])
def graphiques():
    genres_count = db.session.query(Personnes.genre, db.func.count(Personnes.nomIllustre)).group_by(Personnes.genre).all()
    labels = [result[0].value if result[0] is not None else 'NULL' for result in genres_count]
    counts = [result[1] for result in genres_count]
    return render_template('pages/graphiques.html', labels=labels, counts=counts)

#Graphique concernant les domaines des maisons des illustres : 
@app.route("/graphiques/domaines", methods=['GET', 'POST'])
def graphiques_domaines():
    types_count = db.session.query(Maisons.type, db.func.count(Maisons.id)).group_by(Maisons.type).all()
    labels = [result[0].value if result[0] is not None else 'NULL' for result in types_count]
    counts = [result[1] for result in types_count]
    return render_template('pages/graphiques_domaines.html', labels=labels, counts=counts)