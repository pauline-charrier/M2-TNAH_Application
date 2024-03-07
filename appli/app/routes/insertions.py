from ..app import app, db
from flask import render_template, request, flash
from sqlalchemy import distinct
from ..models.data import Maisons, Personnes, Domaine, Genre
from ..models.formulaires import InsertionMaison, InsertionPersonne
from ..utils.transformations import  clean_arg

@app.route("/insertions/maisons", methods=['GET', 'POST'])
def insertion_maisons():
    """
    Gère la route "/insertions/maisons" pour l'insertion de nouvelles maisons.

    Returns
    -------
    render_template or redirect
        Si la requête est GET, renvoie le template HTML avec le formulaire pour l'insertion d'une maison.
        Si la requête est POST, effectue l'insertion et redirige vers le formulaire vide pour une nouvelle insertion si besoin. 
    """

    #obtenir la liste des régions pour le champ Select du formulaire. 
    distinct_regions = Maisons.get_distinct_regions()
    #appel à l'instance formulaire
    form = InsertionMaison()
    #charge les choix des menus déroulants du formulaire
    form.nomIllustre.choices = [('','')] + [(personnes.nomIllustre, personnes.nomIllustre) for personnes in Personnes.query.order_by(Personnes.nomIllustre).all()]
    form.region.choices = [('','')] + [(region, region) for region in distinct_regions]
    form.type.choices = [('','')] + [(domaine.value, domaine.value) for domaine in Domaine]

    try:
        if form.validate_on_submit():
            #récupérer les arguments du formulaire ou None
            id =  clean_arg(request.form.get("id", None))
            denomination =  clean_arg(request.form.get("denomination", None))
            adresse =  clean_arg(request.form.get("adresse", None))
            commune =  clean_arg(request.form.get("commune", None))
            code_postal =  clean_arg(request.form.get("code_postal", None))
            code_INSEE =  clean_arg(request.form.get("code_INSEE", None))
            dpmt =  clean_arg(request.form.get("dpmt", None))
            region =  clean_arg(request.form.get("region", None))
            pays =  clean_arg(request.form.get("pays", None))
            latitude =  clean_arg(request.form.get("latitude", None))
            longitude =  clean_arg(request.form.get("longitude", None))
            date_label =  clean_arg(request.form.get("date_label", None))
            type =  clean_arg(request.form.get("type", None))
            museeFrance =  clean_arg(request.form.get("museeFrance", None))
            monumentsInscrits =  clean_arg(request.form.get("monumentsInscrits", None))
            monumentsClasses =  clean_arg(request.form.get("monumentsClasses", None))
            nombreSPR =  clean_arg(request.form.get("nombreSPR", None))
            nomIllustre = clean_arg(request.form.get("nomIllustre", None))

        # Crée une nouvelle instance de la classe Maisons avec les données du formulaire.
        nouvelle_maison = Maisons(id=id, 
            denomination=denomination,
            adresse=adresse,
            commune=commune,
            code_postal=code_postal,
            code_INSEE=code_INSEE,
            dpmt=dpmt,
            region=region,
            pays=pays,
            latitude=latitude,
            longitude=longitude,
            date_label=date_label,
            type = Domaine.obtenir_clef(type), #la valeur doit être la clef de l'énumération déclarée dans le modèle
            museeFrance=True if museeFrance == 'y' else False, #traduction entre l'argument du formulaire et le modèle de classe
            monumentsClasses=True if monumentsClasses == 'y' else False,
            monumentsInscrits=True if monumentsInscrits == 'y' else False,
            nombreSPR=nombreSPR)
        
        # Si un nom d'illustre est fourni, lie la maison à à la personne
        if nomIllustre is not None:
            print("je détecte quelque chose")
            pers_a_lier = Personnes.query.filter(Personnes.nomIllustre == nomIllustre).first()
            nouvelle_maison.idWikidata = pers_a_lier.idWikidata
        else :   
            print("je ne détecte rien")
            nouvelle_maison.idWikidata = None
        
        # Vérifie si la maison existe déjà en base.
        maison_existante = Maisons.query.filter_by(id=id).first()
            
        if maison_existante:
            flash("L'insertion a échoué. Cette maison existe déjà en base.", 'error')
            return render_template("pages/insertion_maisons.html", sous_titre="Insertion maison", form=form)
            #s'il y a déjà une maison avec le même identifiant dans la base, l'insertion ne peut pas être achevée. Retour du formulaire vide avec un message. 
        else:
            db.session.add(nouvelle_maison)
            db.session.commit()
            flash("L'insertion du pays "+ denomination + " s'est correctement déroulée", 'info')
            #s'il n'y a aucune autre maison avec le même identifiant : l'insertion peut être achevée. 
            # ajoute la maison à la base de données
            #la redirection va se faire vers le template avec le formulaire vide
    
    except Exception as e :
        print(e)
        db.session.rollback()

    return render_template("pages/insertion_maisons.html", 
            sous_titre= "Insertion maisons" , 
            form=form)


@app.route("/insertions/personnes", methods=['GET', 'POST'])
def insertion_personnes():
    """
    Gère la route "/insertions/personnes" pour l'insertion de nouvelles personnes.

    Returns
    -------
    render_template
        Un modèle HTML pour la page d'insertion de personnes avec le formulaire et les données à afficher.
    """

    #créer l'instance du formulaire 
    form = InsertionPersonne()

    # Charge les choix du menu déroulant pour le genre à partir de l'énumération Genre.
    form.genre.choices = [('','')] + [(genre.value, genre.value) for genre in Genre]

    try:
        if form.validate_on_submit():
            #récupérer les arguments du formulaire
            idWikidata =  clean_arg(request.form.get("idWikidata", None))
            nomIllustre =  clean_arg(request.form.get("nomIllustre", None))
            ddn =  clean_arg(request.form.get("ddn", None))
            ddm=  clean_arg(request.form.get("ddm", None))
            genre =  clean_arg(request.form.get("genre", None))
            image =  clean_arg(request.form.get("image", None))
            article =  clean_arg(request.form.get("article", None))

            # Crée une nouvelle instance de la classe Personnes avec les données du formulaire.
            nouvelle_personne = Personnes(idWikidata=idWikidata, 
                nomIllustre=nomIllustre,
                ddn=ddn,
                ddm=ddm,
                genre=Genre.obtenir_clef(genre), #la valeur doit être la clef de l'énumération déclarée dans le modèle
                image=image,
                article=article)
            
            # Vérifie si la personne existe déjà en base.
            personne_existante = Personnes.query.filter_by(idWikidata=idWikidata).first()
            
            #si l'identifiant correspond déjà à un enregistrement en base, l'insertion est interrompue. Le formulaire vide est retourné avec un message. 
            if personne_existante:
                flash("L'insertion a échoué. Cette personne existe déjà en base.", 'error')
                return render_template("pages/insertion_personnes.html", sous_titre="Insertion personne", form=form)
            
            else:
                db.session.add(nouvelle_personne)
                db.session.commit()
                #si pas de personne avec le même identifiant en base, ajout de la personne en base. 
                flash("L'insertion du pays "+ nomIllustre + " s'est correctement déroulée", 'info')

    except Exception as e :
        print(f"Une erreur s'est produite : {str(e)}")
        flash("Une erreur a empêché la création de "+ nomIllustre, 'danger')
        db.session.rollback()

    return render_template("pages/insertion_personnes.html", 
            sous_titre= "Insertion personne", 
            form=form)