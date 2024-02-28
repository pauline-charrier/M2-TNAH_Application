from ..app import app, db
from flask import render_template, request, flash
from sqlalchemy import or_, text, func
from ..models.formulaires import Recherche
from ..models.data import Maisons, Personnes, Domaine, Genre
from ..utils.transformations import nettoyage_string_to_int, clean_arg, normaliser
from unidecode import unidecode


'''
Sur la route recherche, le .paginate ne fonctionne pas, 
le filtre sur le nom du bâtiment ne fonctionne pas non plus
'''

@app.route("/recherche", methods=['GET', 'POST'])
@app.route("/recherche/<int:page_num>", methods=['GET', 'POST'])
def recherche(page_num=1):
    form = Recherche()
    distinct_regions = Maisons.get_distinct_regions()
    distinct_departements = Maisons.get_distinct_departements()
    distinct_dates = Maisons.get_distinct_date_label()
    form.region.choices = [('','')] + [(region, region) for region in distinct_regions]
    form.departement.choices = [('','')] + [(dp, dp) for dp in distinct_departements]
    form.date_label.choices = [('','')] + [(date, date) for date in distinct_dates]
    form.type.choices = [('','')] + [(domaine.value, domaine.value) for domaine in Domaine]
    form.genre.choices = [('','')] + [(genre.value, genre.value) for genre in Genre]

    # initialisation des données de retour dans le cas où il n'y ait pas de requête
    donnees = []

    if form.validate_on_submit():
        # récupération des éventuels arguments de l'URL qui seraient le signe de l'envoi d'un formulaire
        denomination = clean_arg(request.form.get("denomination", None))
        region =  clean_arg(request.form.get("region", None))
        departement = clean_arg(request.form.get("departement", None))
        type =  clean_arg(request.form.get("type", None))
        genre =  clean_arg(request.form.get("genre", None))
        #periode = clean_arg(request.form.getlist("periode", None))
        museeFrance =  clean_arg(request.form.get("museeFrance", None))
        monumentsInscrits =  clean_arg(request.form.get("monumentsInscrits", None))
        monumentsClasses =  clean_arg(request.form.get("monumentsClasses", None))
        date_label = clean_arg(request.form.get("date_label", None))

        # si l'un des champs de recherche a une valeur, alors cela veut dire que le formulaire a été rempli et qu'il faut lancer une recherche 
        # dans les données
        if denomination or region or departement or type or genre or museeFrance or monumentsClasses or monumentsInscrits or date_label :
            # initialisation de la recherche; en fonction de la présence ou nom d'un filtre côté utilisateur, nous effectuerons des filtres SQLAlchemy,
            # ce qui signifie que nous pouvons jouer ici plusieurs filtres d'affilée
            query_results = Maisons.query
#ce filtre ne fonctionne pas
            if denomination:
                denomination = normaliser(denomination)
                subquery_1 = text("""
                    SELECT id
FROM maisons 
WHERE lower(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(denomination, 'Î', 'I'), 'ë', 'e'), 'ê', 'e'), 'è', 'e'), 'é', 'e'), 'Â', 'A'), 'À', 'A'), 'Ô', 'O'), 'È', 'E'), 'É', 'E')) like '%"""+denomination+"""%'
                    """)
                comparaison_ids = [row[0] for row in db.session.execute(subquery_1)]
                query_results = query_results.filter(Maisons.id.in_(comparaison_ids))
                #query_results = query_results.filter(func.lower(Maisons.denomination).ilike("%"+denomination+"%".lower()))

            if region : 
                query_results = query_results.filter(Maisons.region == region)

            if departement:
                query_results = query_results.filter(Maisons.dpmt == departement)

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
            
            if date_label:
                query_results = query_results.filter(Maisons.date_label == date_label)

            donnees = query_results.all()
            #.paginate(page=page_num, per_page=app.config["MAISONS_PER_PAGE"], error_out=True)
            #print(donnees)
            #print(donnees.items)

#le .paginate ne fonctionne pas pourquoi ???????????  

        #pré-remplir le formulaire pour la prochaine recherche
        form.denomination.data = denomination
        form.region.data = region
        form.type.data = type
        form.museeFrance.data = museeFrance
        form.monumentsClasses.data=monumentsClasses
        form.monumentsInscrits.data=monumentsClasses
        form.departement.data = departement
        form.date_label.data = date_label

    return render_template("pages/resultats_recherche (copie).html", 
        sous_titre= "Recherche", 
        donnees=donnees,
        form=form, 
        page=page_num)
            
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
        chaine = normaliser(chaine)
        subquery = text("""
                SELECT a.id
                FROM maisons a
                INNER JOIN personnes b ON b.idWikidata = a.idWikidata AND lower(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(b.nomIllustre, 'Î', 'I'), 'ë', 'e'), 'ê', 'e'), 'è', 'e'), 'é', 'e'), 'Â', 'A'), 'À', 'A'), 'Ô', 'O'), 'È', 'E'), 'É', 'E')) like '%"""+chaine+"""%'
                """)
        personnes_ids = [row[0] for row in db.session.execute(subquery)]#ok fonctionne

        subquery_1 = text("""
                SELECT id
                FROM maisons 
                WHERE lower(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(denomination, 'Î', 'I'), 'ë', 'e'), 'ê', 'e'), 'è', 'e'), 'é', 'e'), 'Â', 'A'), 'À', 'A'), 'Ô', 'O'), 'È', 'E'), 'É', 'E')) like '%"""+normaliser(chaine)+"""%'
                    """)
        denomination_ids = [row[0] for row in db.session.execute(subquery_1)]

        domaines = Domaine.comparer_valeurs(chaine)#ok fonctionne
#implémenter la méthode de grosse bourrine 
        resultats = Maisons.query.\
            filter(
                or_(
                    #func.lower(func.replace(Maisons.denomination, 'É', 'E')).ilike("%"+normaliser(chaine)+"%"),#ok fonctionne
                    Maisons.id.in_(denomination_ids),
                    func.lower(func.replace(func.replace(func.replace(Maisons.region, 'î', 'i'),'Î', 'I'),'é', 'e' )).ilike("%" + normaliser(chaine) + "%"),
                    func.lower(func.replace(Maisons.commune, 'É', 'E')).ilike("%"+normaliser(chaine)+"%"),
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
            

    else:
        resultats = None
        flash("Pas de résultats, effectuer une nouvelle recherche")
        
        
    return render_template("pages/essai_resultats.html", 
            sous_titre= "Recherche | " + chaine, 
            donnees=resultats,
            requete=chaine)


