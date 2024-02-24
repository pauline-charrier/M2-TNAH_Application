from ..app import app, db
from flask import render_template, request
from sqlalchemy import or_, text
from ..models.formulaires import Recherche
from ..models.data import Maisons, Personnes, Domaine, Genre
from ..utils.transformations import nettoyage_string_to_int, clean_arg



@app.route("/recherche", methods=['GET', 'POST'])
@app.route("/recherche/<int:page>", methods=['GET', 'POST'])
def recherche(page=1):
    form = Recherche()
    #personnes_instance = Personnes()
    #distinct_periode = personnes_instance.get_distinct_siecles()
    distinct_regions = Maisons.get_distinct_regions()
    form.region.choices = [('','')] + [(region, region) for region in distinct_regions]
    form.type.choices = [('','')] + [(domaine.value, domaine.value) for domaine in Domaine]
    form.genre.choices = [('','')] + [(genre.value, genre.value) for genre in Genre]
    #form.periode.choices = [('','')] + [(periode.value, periode.value) for periode in distinct_periode]

    # initialisation des données de retour dans le cas où il n'y ait pas de requête
    donnees = []

    if form.validate_on_submit():
        # récupération des éventuels arguments de l'URL qui seraient le signe de l'envoi d'un formulaire
        denomination = clean_arg(request.form.get("denomination", None))
        region =  clean_arg(request.form.get("region", None))
        type =  clean_arg(request.form.get("type", None))
        genre =  clean_arg(request.form.get("genre", None))
        #periode = clean_arg(request.form.getlist("periode", None))
        museeFrance =  clean_arg(request.form.get("museeFrance", None))
        monumentsInscrits =  clean_arg(request.form.get("monumentsInscrits", None))
        monumentsClasses =  clean_arg(request.form.get("monumentsClasses", None))

        # si l'un des champs de recherche a une valeur, alors cela veut dire que le formulaire a été rempli et qu'il faut lancer une recherche 
        # dans les données
        if region or type or genre or museeFrance or monumentsClasses or monumentsInscrits :
            # initialisation de la recherche; en fonction de la présence ou nom d'un filtre côté utilisateur, nous effectuerons des filtres SQLAlchemy,
            # ce qui signifie que nous pouvons jouer ici plusieurs filtres d'affilée
            query_results = Maisons.query

            #le filtre denomination ne fonctionne pas
            if denomination:
                query_results = query_results.filter(Maisons.denomination.ilike("%"+denomination+"%")) #.lower upper ?

            if region : 
                query_results = query_results.filter(Maisons.region == region)
                print(region)

            if type : 
                query_results = query_results.filter(Maisons.type == Domaine.obtenir_clef(type))

            if museeFrance:
                query_results = query_results.filter(Maisons.museeFrance == True)
            
            if monumentsInscrits:
                query_results = query_results.filter(Maisons.monumentsInscrits == True)

            if monumentsClasses:
                query_results = query_results.filter(Maisons.monumentsClasses == True)
            
            if genre:
                subquery = text("""
                    SELECT a.id
                    FROM maisons a
                    INNER JOIN personnes b ON b.idWikidata = a.idWikidata AND b.genre = :genre
                    """)
                genre_ids = [row[0] for row in db.session.execute(subquery, {'genre': Genre.obtenir_clef(genre)})]

                query_results = query_results.order_by(Maisons.denomination).filter(Maisons.id.in_(genre_ids))

            donnees = query_results.paginate(page=page, per_page=app.config["MAISONS_PER_PAGE"])
            print(donnees)

        form.denomination.data = denomination
        form.region.data = region
        form.type.data = type
        form.museeFrance.data = museeFrance
        form.monumentsClasses.data=monumentsClasses
        form.monumentsInscrits.data=monumentsClasses

    return render_template("pages/resultats_recherche.html", 
        sous_titre= "Recherche", 
        donnees=donnees,
        form=form, 
        page=page)
            
'''

            if periode:
                periode = db.session.execute("""select a.id from maisons a 
                    inner join personnes b on b.idWikidata = a.idWikidata and siecles_vie == '"""+periode+"""'
                    """).fetchall()
                query_results = query_results.filter(Maisons.id.in_([p.id for p in periode] ))
            
            donnees = query_results.order_by(Maisons.name).paginate(page=page, per_page=app.config["PAYS_PER_PAGE"])
'''



@app.route("/recherche_rapide")
@app.route("/recherche_rapide/<int:page>")
def recherche_rapide(page=1):
    chaine =  request.args.get("chaine", None)

    if chaine:
        subquery = text("""
                SELECT a.id
                FROM maisons a
                INNER JOIN personnes b ON b.idWikidata = a.idWikidata AND b.nomIllustre like '%"""+chaine+"""%' or b.ddn like '%"""+chaine+"""%' or b.ddm like '%"""+chaine+"""%'
                """)
        personnes_ids = [row[0] for row in db.session.execute(subquery)]

        domaines = Domaine.comparer_valeurs(chaine)

        resultats = Maisons.query.\
            filter(
                or_(
                    Maisons.denomination.ilike("%"+chaine+"%"),
                    Maisons.region.ilike("%"+chaine+"%"),
                    Maisons.commune.ilike("%"+chaine+"%"),
                    Maisons.id.in_(personnes_ids),
                    Maisons.type == domaines
                )
            ).\
            distinct(Maisons.denomination).\
            order_by(Maisons.denomination).\
            paginate(page=page, per_page=app.config["MAISONS_PER_PAGE"])
    else:
        resultats = None
        
    return render_template("pages/resultats_recherche_full_texte.html", 
            sous_titre= "Recherche | " + chaine, 
            donnees=resultats,
            requete=chaine)

