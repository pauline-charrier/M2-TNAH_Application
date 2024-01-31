from ..app import app, db
from flask import render_template, request
from sqlalchemy import or_
from ..models.formulaires import Recherche
from ..utils.transformations import nettoyage_string_to_int, clean_arg


@app.route("/recherche_rapide")
@app.route("/recherche_rapide/<int:page>")
def recherche_rapide(page=1):
    chaine =  request.args.get("chaine", None)

    if chaine:
        resources = db.session.execute("""select a.id from country a 
            inner join country_resources b on b.id = a.id 
            inner join resources c on c.name = b.resource and (c.name like '%"""+chaine+"""%' or  c.id like '%"""+chaine+"""%')
            """).fetchall()
        
        maps = db.session.execute("""select a.id from country a 
            inner join country_map b on b.id = a.id 
            inner join map  c on c.name = b.map_ref and (c.name like '%"""+chaine+"""%' or  c.id like '%"""+chaine+"""%')
            """).fetchall()

        resultats = Country.query.\
            filter(
                or_(
                    Country.name.ilike("%"+chaine+"%"),
                    Country.type.ilike("%"+chaine+"%"),
                    Country.Introduction.ilike("%"+chaine+"%"),
                    Country.id.in_([r.id for r in resources] + [m.id for m in maps])
                )
            ).\
            distinct(Country.name).\
            order_by(Country.name).\
            paginate(page=page, per_page=app.config["PAYS_PER_PAGE"])
    else:
        resultats = None
        
    return render_template("pages/resultats_recherche_pays.html", 
            sous_titre= "Recherche | " + chaine, 
            donnees=resultats,
            requete=chaine)

@app.route("/recherche", methods=['GET', 'POST'])
@app.route("/recherche/<int:page>", methods=['GET', 'POST'])
def recherche(page=1):
    form = Recherche() 

    # initialisation des données de retour dans le cas où il n'y ait pas de requête
    donnees = []

    if form.validate_on_submit():
        # récupération des éventuels arguments de l'URL qui seraient le signe de l'envoi d'un formulaire
        nom_pays =  clean_arg(request.form.get("nom_pays", None))
        ressource =  clean_arg(request.form.get("ressources", None))
        continent =  clean_arg(request.form.get("continents", None))

        # si l'un des champs de recherche a une valeur, alors cela veut dire que le formulaire a été rempli et qu'il faut lancer une recherche 
        # dans les données
        if nom_pays  or continent or ressource:
            # initialisation de la recherche; en fonction de la présence ou nom d'un filtre côté utilisateur, nous effectuerons des filtres SQLAlchemy,
            # ce qui signifie que nous pouvons jouer ici plusieurs filtres d'affilée
            query_results = Country.query

            if nom_pays:
                query_results = query_results.filter(Country.name.ilike("%"+nom_pays.lower()+"%"))
            
            if ressource:
                resource = db.session.execute("""select a.id from country a 
                    inner join country_resources b on b.id = a.id and b.resource  == '"""+ressource+"""'
                    """).fetchall()
                query_results = query_results.filter(Country.id.in_([r.id for r in resource] ))
            
            if continent:
                map = db.session.execute("""select a.id from country a 
                    inner join country_map b on b.id = a.id and map_ref == '"""+continent+"""'
                    """).fetchall()
                query_results = query_results.filter(Country.id.in_([m.id for m in map] ))
            
            donnees = query_results.order_by(Country.name).paginate(page=page, per_page=app.config["PAYS_PER_PAGE"])

            # renvoi des filtres de recherche pour préremplissage du formulaire
            form.nom_pays.data = nom_pays
            form.continents.data = continent
            form.ressources.data = ressource

    return render_template("pages/resultats_recherche.html", 
            sous_titre= "Recherche" , 
            donnees=donnees,
            form=form)
