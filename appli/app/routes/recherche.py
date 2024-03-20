from ..app import app, db
from flask import render_template, request
from sqlalchemy import or_, text, func
from ..models.formulaires import Recherche
from ..models.data import Maisons, Personnes, Domaine, Genre
from ..utils.transformations import clean_arg, normaliser
from unidecode import unidecode


'''
pb de pagination !!!!!!
'''

@app.route("/recherche", methods=['GET', 'POST'])
@app.route("/recherche/<int:page_num>", methods=['GET', 'POST'])
def recherche(page_num=1):
    """
    Gère la route "/recherche" pour effectuer une recherche 'par facettes' en fonction de plusieurs filtres.

    Parameters
    ----------
    page : int, optional
        Numéro de la page à afficher, par défaut 1.

    Returns
    -------
    render_template
        Un modèle HTML pour la page de résultats de recherche avec les données à afficher. Les résultats sont les bâtiments pour lesquels la 
        chaîne de caractère entrée ou les filtres sélectionnés sont trouvés dans les attributs des classes Maisons et Personnes. 
    """
    
    # Création du formulaire de recherche
    form = Recherche()

    # Récupération des valeurs distinctes pour les filtres
    distinct_regions = Maisons.get_distinct_regions()
    distinct_departements = Maisons.get_distinct_departements()
    distinct_dates = Maisons.get_distinct_date_label()
    
    # Assignation des valeurs des filtres au formulaire
    form.region.choices = [('','')] + [(region, region) for region in distinct_regions]
    form.departement.choices = [('','')] + [(dp, dp) for dp in distinct_departements]
    form.date_label.choices = [('','')] + [(date, date) for date in distinct_dates]
    form.type.choices = [('','')] + [(domaine.value, domaine.value) for domaine in Domaine]
    form.genre.choices = [('','')] + [(genre.value, genre.value) for genre in Genre]

    #Initialisation des données 
    donnees_init = []  
    donnees = [] 

    # S'il n'y a pas de filtre, la méthode est GET et la fonction affiche le catalogue complet des bâtiments
    if request.method == 'GET' :
        donnees_init = Maisons.query.order_by(Maisons.denomination).paginate(page=page_num, per_page=app.config["MAISONS_PER_PAGE"])
        donnees = [] #vider des données filtrées s'il n'y a pas de requête POST

    # S'il y a un filtre : la méthode est POST et la fonction va filtrer les bâtiments
    # Traitement des données soumises par le formulaire
    elif request.method =='POST':
        donnees_init=[] #vider les données initiales (catalogue complet)

        if form.validate_on_submit():
            # récupération des éventuels données soumises via le formulaire
            denomination = clean_arg(request.form.get("denomination", None))
            region =  clean_arg(request.form.get("region", None))
            departement = clean_arg(request.form.get("departement", None))
            type =  clean_arg(request.form.get("type", None))
            genre =  clean_arg(request.form.get("genre", None))
            museeFrance =  clean_arg(request.form.get("museeFrance", None))
            monumentsInscrits =  clean_arg(request.form.get("monumentsInscrits", None))
            monumentsClasses =  clean_arg(request.form.get("monumentsClasses", None))
            date_label = clean_arg(request.form.get("date_label", None))
            page_num = int(request.form.get('page_num'))

            # Vérification de la présence de valeurs dans les champs de recherche pour lancer la recherche
            if denomination or region or departement or type or genre or museeFrance or monumentsClasses or monumentsInscrits or date_label :
                # initialisation de la recherche; en fonction de la présence ou nom d'un filtre côté utilisateur, nous effectuerons des filtres SQLAlchemy,
                # ce qui signifie que nous pouvons jouer ici plusieurs filtres d'affilée
                query_results = Maisons.query

                # Filtrage des résultats en fonction des critères de recherche
                if denomination:
                    # Filte recherche du nom de la maison
                    denomination = normaliser(denomination)
                    subquery_1 = text("""
                        SELECT id
    FROM maisons 
    WHERE lower(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(denomination, 'Î', 'I'), 'ë', 'e'), 'ê', 'e'), 'è', 'e'), 'é', 'e'), 'Â', 'A'), 'À', 'A'), 'Ô', 'O'), 'È', 'E'), 'É', 'E')) like '%"""+denomination+"""%'
                        """)
                    comparaison_ids = [row[0] for row in db.session.execute(subquery_1)]
                    query_results = query_results.filter(Maisons.id.in_(comparaison_ids))

                if region : 
                    # Filtrage par région
                    query_results = query_results.filter(Maisons.region == region)

                if departement:
                    # Filtrage par département
                    query_results = query_results.filter(Maisons.dpmt == departement)

                if type : 
                    # Filtrage par type ou domaine (littérature, musique etc.)
                    query_results = query_results.filter(Maisons.type == Domaine.obtenir_clef(type))

                # Filtre sur les multilabels
                if museeFrance:
                    query_results = query_results.filter(Maisons.museeFrance == True)
                
                if monumentsInscrits:
                    query_results = query_results.filter(Maisons.monumentsInscrits == True)

                if monumentsClasses:
                    query_results = query_results.filter(Maisons.monumentsClasses == True)
                
                if genre:
                    # Filtrage sur le genre de la personne
                    subquery = text("""
                        SELECT a.id
                        FROM maisons a
                        INNER JOIN personnes b ON b.idWikidata = a.idWikidata AND b.genre = :genre
                        """)
                    genre_ids = [row[0] for row in db.session.execute(subquery, {'genre': Genre.obtenir_clef(genre)})]

                    query_results = query_results.order_by(Maisons.denomination).filter(Maisons.id.in_(genre_ids))
                
                if date_label:
                    # Filtrage par date de labellisation
                    query_results = query_results.filter(Maisons.date_label == date_label)

                #gestion de la pagination dans le route 
                # les boutons de pagination re-soumettent le formulaire
                if 'prev' in request.form:
                    # Si l'action est 'prev' le numéro de page est décrémenté de 1
                    page_num -= 1


                elif 'next' in request.form:
                    # Si l'action est 'next', le numéro de page est incrémenté de 1
                    page_num += 1

                
                elif 'rech' in request.form:
                    # si une nouvelle recherche est lancée, le numéro de page est réaffecté à 1
                    page_num = 1

                #résultats de la recherche
                donnees = query_results.paginate(page=page_num, per_page=app.config["MAISONS_PER_PAGE"], error_out=True)
 
            #pré-remplir le formulaire pour le prochain submit
            form.denomination.data = denomination
            form.region.data = region
            form.type.data = type
            form.museeFrance.data = museeFrance
            form.monumentsClasses.data=monumentsClasses
            form.monumentsInscrits.data=monumentsInscrits
            form.departement.data = departement
            form.date_label.data = date_label
            print("récupération du num de page_num", page_num) 

    # Rendu du modèle HTML avec les données à afficher
    return render_template("pages/resultats_recherche (copie).html", 
        sous_titre= "Recherche", 
        donnees_init=donnees_init,
        donnees=donnees,
        form=form, 
        page=page_num,
        page_num=page_num)




@app.route("/recherche_rapide")
@app.route("/recherche_rapide/<int:page>")
def recherche_rapide(page=1):
    """
    Gère la route "/recherche_rapide" pour effectuer une recherche type 'plein text' à partir de la barre de recherche du header.

    Parameters
    ----------
    page : int, optional
        Numéro de la page à afficher, par défaut 1.

    Returns
    -------
    render_template
        Un modèle HTML pour la page de résultats de recherche avec les données paginées à afficher. Les résultats sont les bâtiments pour lesquels la 
        chaîne de caractère entrée est trouvée dans les attributs de la classe Maisons. 
    """

    # Récupère la chaîne de recherche depuis le formulaire de requête (barre de recherche)
    chaine = request.args.get("chaine", None)
    # Initialisation de la variable resultats
    resultats = None

    if chaine:
        #si une chaîne de caractère est entrée par l'utilisateur, on va chercher dans les valeurs de différents attributs ; 
        #normalisation à l'aide d'une fonction définie dans les utilitaires

        #recherche de l'id des personnes dont le nom correspond à la chaîne de caractère
        #comme SQLite ne dispose pas de la fonction unaccent() (disponible dans PostgreSQL par exemple),nous avons procédé de manière très artisanale en imbiquant des 'replace' les uns dans les autres.
        #de cette manière, les accents les plus courant en français seront supprimés, y compris sur les majuscules. 
        #cette étape est décisive car la fonction lower() de SQLite ne fonctionne pas sur les majuscules accentuées. 
        subquery = text("""
            SELECT a.id
            FROM maisons a
            INNER JOIN personnes b ON b.idWikidata = a.idWikidata AND lower(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(b.nomIllustre, 'Î', 'I'), 'ë', 'e'), 'ê', 'e'), 'è', 'e'), 'é', 'e'), 'Â', 'A'), 'À', 'A'), 'Ô', 'O'), 'È', 'E'), 'É', 'E')) like '%""" + chaine + """%'
            """)
        personnes_ids = [row[0] for row in db.session.execute(subquery)]

        #recherche l'id des maisons dont le nom correspond à la chaîne de caractère
        subquery_1 = text("""
            SELECT id
            FROM maisons 
            WHERE lower(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(denomination, 'Î', 'I'), 'ë', 'e'), 'ê', 'e'), 'è', 'e'), 'é', 'e'), 'Â', 'A'), 'À', 'A'), 'Ô', 'O'), 'È', 'E'), 'É', 'E')) like '%""" + normaliser(chaine) + """%'
            """)
        denomination_ids = [row[0] for row in db.session.execute(subquery_1)]

        #une méthode de classe définie dans le modèle de donnée compare la chaîne de caractère recherchée aux valeurs de l'énumération des domaines. 
        domaines = Domaine.comparer_valeurs(chaine)

        #si un ou des domaines correspondent à la chaîne de caractère : 
        if domaines:
            resultats = Maisons.query.\
                filter(
                    or_(
                        Maisons.id.in_(denomination_ids),
                        func.lower(func.replace(func.replace(func.replace(Maisons.region, 'î', 'i'),'Î', 'I'),'é', 'e' )).ilike("%" + normaliser(chaine) + "%"),
                        func.lower(func.replace(Maisons.commune, 'É', 'E')).ilike("%"+normaliser(chaine)+"%"),
                        Maisons.id.in_(personnes_ids),
                        Maisons.type == domaines
                    )
                ).\
                distinct(Maisons.denomination).\
                order_by(Maisons.denomination).\
                paginate(page=page, per_page=app.config["MAISONS_PER_PAGE"])

        #pour supprimer des résultats les maisons dont le domaine thématique est None, et qui sinon ressortirait automatiquement. 
        else:
            resultats = Maisons.query.\
                filter(
                    or_(
                        Maisons.id.in_(denomination_ids),
                        func.lower(func.replace(func.replace(func.replace(Maisons.region, 'î', 'i'),'Î', 'I'),'é', 'e' )).ilike("%" + normaliser(chaine) + "%"),
                        func.lower(func.replace(Maisons.commune, 'É', 'E')).ilike("%"+normaliser(chaine)+"%"),
                        Maisons.id.in_(personnes_ids),
                    )
                ).\
                distinct(Maisons.denomination).\
                order_by(Maisons.denomination).\
                paginate(page=page, per_page=app.config["MAISONS_PER_PAGE"])

        if not resultats.items:
            return render_template("pages/resultats_recherche_full_texte.html",
                                   sous_titre="Recherche | " + chaine,
                                   no_results=True,
                                   requete=chaine)

    return render_template("pages/resultats_recherche_full_texte.html",
                           sous_titre="Recherche | " + chaine,
                           donnees=resultats,
                           requete=chaine)


