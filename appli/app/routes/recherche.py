from ..app import app, db
from flask import render_template, request, flash
from sqlalchemy import or_, text, func
from ..models.formulaires import Recherche
from ..models.data import Maisons, Personnes, Domaine, Genre
from ..utils.transformations import nettoyage_string_to_int, clean_arg, normaliser, supprimer_accents

'''
Sur la route recherche, le .paginate ne fonctionne pas, 
le filtre sur le nom du bâtiment ne fonctionne pas non plus
'''

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
#ce filtre ne fonctionne pas
            if denomination:
                query_results = query_results.filter(func.lower(Maisons.denomination).ilike("%"+denomination+"%".lower()))

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

            donnees = query_results.all()
            #paginate(page=page, per_page=app.config["MAISONS_PER_PAGE"])
            print(donnees)

#le .paginate ne fonctionne pas 

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
essai avorté sur une recherche en fonction de la période
            if periode:
                periode = db.session.execute("""select a.id from maisons a 
                    inner join personnes b on b.idWikidata = a.idWikidata and siecles_vie == '"""+periode+"""'
                    """).fetchall()
                query_results = query_results.filter(Maisons.id.in_([p.id for p in periode] ))
            
            donnees = query_results.order_by(Maisons.name).paginate(page=page, per_page=app.config["PAYS_PER_PAGE"])
'''

'''
Problème avec la route de la barre de recherche : elle envoie des faux positifs -_-' Waruuuuum !!
20 maisons, toujours les mêmes 
[<Maisons MI189>, <Maisons MI154>, <Maisons MI236>, <Maisons MI047>, <Maisons MI029>, 
<Maisons MI158>, <Maisons MI010>, <Maisons MI237>, <Maisons MI239>, <Maisons MI240>, 
<Maisons MI241>, <Maisons MI243>, <Maisons MI244>, <Maisons MI102>, <Maisons MI246>, 
<Maisons MI247>, <Maisons MI066>, <Maisons MI249>, <Maisons MI093>, <Maisons MI250>, <Maisons MI251>]
'''

@app.route("/recherche_rapide")
@app.route("/recherche_rapide/<int:page>")
def recherche_rapide(page=1):
    chaine =  request.args.get("chaine", None)

    if chaine:
        chaine = supprimer_accents(chaine)
        subquery = text("""
                SELECT a.id
                FROM maisons a
                INNER JOIN personnes b ON b.idWikidata = a.idWikidata AND b.nomIllustre like '%"""+chaine+"""%' or b.ddn like '%"""+chaine+"""%' or b.ddm like '%"""+chaine+"""%'
                """)
        personnes_ids = [row[0] for row in db.session.execute(subquery)]#ok fonctionne

        domaines = Domaine.comparer_valeurs(chaine)#ok fonctionne

        resultats = Maisons.query.\
            filter(
                or_(
                    normaliser(Maisons.denomination).ilike("%"+chaine.lower()+"%"),#ok fonctionne
                    normaliser(Maisons.region).ilike("%"+chaine.lower()+"%"),#ok fonctionne
                    normaliser(Maisons.commune).ilike("%"+chaine.lower()+"%"),#ok fonctionne sauf pb avec les accents (par exemple on trouve chamb mais pas chambéry)
                    Maisons.id.in_(personnes_ids),#ok fonctionn
                    Maisons.type == domaines#ok fonctionne
                )
            ).\
            distinct(Maisons.denomination).\
            order_by(Maisons.denomination).all()
        #.\
            #paginate(page=page, per_page=app.config["MAISONS_PER_PAGE"])
        #pareil : le .paginate ne fonctionen pas. On passe de /recherche/1 à maisons/2
        
        if resultats:
            print(resultats)
            print(personnes_ids)
            print(domaines)
        else:
            print("il n'y a pas de résultats")
            flash("Pas de résultats, effectuer une nouvelle recherche")

    else:
        resultats = None
        
        
    return render_template("pages/essai_resultats.html", 
            sous_titre= "Recherche | " + chaine, 
            donnees=resultats,
            requete=chaine)

