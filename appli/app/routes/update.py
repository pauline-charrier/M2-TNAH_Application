from ..app import app, db
from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import distinct, text
from ..models.data import Maisons, Personnes, Domaine, Genre
from ..models.formulaires import InsertionMaison, InsertionPersonne, UpdateMaisons, UpdatePersonnes
from ..utils.transformations import clean_arg


@app.route("/update/maisons/<string:nom_maison>", methods=['GET', 'POST'])
def update_maisons(nom_maison):
    distinct_regions = Maisons.get_distinct_regions()
    maison= Maisons.query.filter(Maisons.denomination == nom_maison).first()
    personne = Personnes.query.filter(Personnes.idWikidata == str(maison.idWikidata)).first()
    form = UpdateMaisons() 
    
    # Remplir le formulaire avec les données en base
    form.id.data = maison.id
    form.denomination.data = maison.denomination
    form.code_postal.data = maison.code_postal
    form.adresse.data = maison.adresse
    form.commune.data = maison.commune
    form.dpmt.data = maison.dpmt
    form.region.data = maison.region
    form.code_INSEE.data = maison.code_INSEE
    form.pays.data = maison.pays
    form.date_label.data = maison.date_label
    form.latitude.data = maison.latitude
    form.longitude.data = maison.longitude
    form.museeFrance.data = maison.museeFrance
    form.monumentsInscrits.data = maison.monumentsInscrits
    form.monumentsClasses.data = maison.monumentsClasses
   
    form.nombreSPR.data = maison.nombreSPR 
    form.type.data = maison.type.value if maison.type else ''
    form.nomIllustre.data = personne.nomIllustre if personne else ''


    form.nomIllustre.choices = [('','')] + [(personnes.nomIllustre, personnes.nomIllustre) for personnes in Personnes.query.all()]
    form.region.choices = [('','')] + [(region, region) for region in distinct_regions]
    form.type.choices = [('','')] + [(domaine.value, domaine.value) for domaine in Domaine]

    print("Formulaire est-il valide ?", form.validate_on_submit())
    if not form.validate_on_submit():
       app.logger.error("Erreurs de validation du formulaire : %s", form.errors)

    try:
        if form.validate_on_submit():
            id =  clean_arg(request.form.get("id", None))
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

            # Vérifier si l'objet existe
            if maison:
                print(maison)
                # Mettre à jour les propriétés de l'objet avec les nouvelles valeurs
                maison.id = id
                maison.adresse = adresse
                maison.commune = commune
                maison.code_postal = code_postal
                maison.code_INSEE = code_INSEE
                maison.dpmt = dpmt
                maison.region = region
                maison.pays = pays
                maison.latitude = latitude
                maison.longitude = longitude
                maison.date_label = date_label
                maison.type = Domaine.obtenir_clef(type)
                maison.museeFrance = True if museeFrance == 'y' else False
                maison.monumentsInscrits = True if monumentsInscrits == 'y' else False
                maison.monumentsClasses = True if monumentsClasses == 'y' else False
                maison.nombreSPR = nombreSPR #if nombreSPR else None
                if nomIllustre is not None:
                    print("je détecte quelque chose")
                    pers_a_lier = Personnes.query.filter(Personnes.nomIllustre == nomIllustre).first()
                    maison.idWikidata = pers_a_lier.idWikidata
                else :   
                    print("je ne détecte rien")
                    maison.idWikidata = None

                    

                # Effectuez l'opération de mise à jour
                db.session.commit()
                print("mise à jour effectuée")

                #Rediriger vers la page de la maison avec les données mises à jour
                return redirect(url_for('info_maisons', nom_maisons=nom_maison))
                
            else:
                print("Aucun information sur cette maison.")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        db.session.rollback()

    return render_template("pages/update_maisons.html", 
            sous_titre= "Update maisons", 
            form=form, 
            donnees=maison)


@app.route("/update/personnes/<string:nom_personne>", methods=['GET', 'POST'])
def update_personne(nom_personne):
    personne = Personnes.query.filter(Personnes.nomIllustre == nom_personne).first()
    form = UpdatePersonnes()

    # Remplir le formulaire avec les données en base
    form.nomIllustre.data = personne.nomIllustre
    form.ddn.data = personne.ddn
    form.ddm.data = personne.ddm
    form.image.data = personne.image
    form.article.data = personne.article
    form.genre.data = personne.genre.value if personne.genre else ''

    form.genre.choices = [('','')] + [(genre.value, genre.value) for genre in Genre]

    print("Formulaire est-il valide ?", form.validate_on_submit())
    if not form.validate_on_submit():
       app.logger.error("Erreurs de validation du formulaire : %s", form.errors)

    try:
        if form.validate_on_submit():
            nomIllustre =  clean_arg(request.form.get("nomIllustre", None))
            ddn =  clean_arg(request.form.get("ddn", None))
            ddm =  clean_arg(request.form.get("ddm", None))
            image =  clean_arg(request.form.get("image", None))
            article =  clean_arg(request.form.get("article", None))
            genre =  clean_arg(request.form.get("genre", None))

            # Vérifier si l'objet existe
            if personne:
                print(personne)
                # Mettre à jour les propriétés de l'objet avec les nouvelles valeurs
                personne.nomIllustre = nomIllustre
                personne.ddn = ddn
                personne.ddm = ddm
                personne.image = image
                personne.article = article
                personne.genre = Genre.obtenir_clef(genre)
                
                # Effectuez l'opération de mise à jour
                db.session.commit()
                print("la mise à jour s'est bien déroulée")

                flash("La mise à jour de "+ nomIllustre + " s'est correctement déroulée", 'info')
                
            else:
                print("Aucun information sur cette maison.")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        flash("Une erreur a empêché la mise à jour de "+ nomIllustre, 'danger')
        db.session.rollback()

    return render_template("pages/update_personnes.html", 
            sous_titre= "Update personnes", 
            form=form, 
            donnees=personne)


