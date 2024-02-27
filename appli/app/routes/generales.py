from ..app import app, db
from flask import render_template, request
from sqlalchemy import or_
from ..models.data import Maisons, Personnes, Domaine, Genre
from ..models.formulaires import Recherche
from ..utils.transformations import nettoyage_string_to_int, clean_arg

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
    donnees = Maisons.query.all()
    return render_template("pages/carte.html",
        sous_titre="Carte",
        donnees = donnees)