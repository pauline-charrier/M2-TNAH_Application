from ..app import app, db
from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import distinct
from ..models.data import Maisons, Personnes, Domaine, Genre
from ..models.formulaires import InsertionMaison, InsertionPersonne, UpdateMaisons
from ..utils.transformations import clean_arg

@app.route("/update/maisons/<string:nom_maison>", methods=['GET', 'POST'])
def update_maisons(nom_maison):
    distinct_regions = Maisons.get_distinct_regions()
    donnees= Maisons.query.filter(Maisons.denomination == nom_maison).first()
    form = UpdateMaisons(obj=donnees)
    form.idWikidata.choices = [('','')] + [(personnes.idWikidata, personnes.idWikidata) for personnes in Personnes.query.all()]
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
            museeFrance =  clean_arg(request.form.get("musee_france", None))
            monumentsInscrits =  clean_arg(request.form.get("monuments_inscrits", None))
            monumentsClasses =  clean_arg(request.form.get("monuments_classes", None))
            nombreSPR =  clean_arg(request.form.get("nombre_SPR", None))
            idWikidata = clean_arg(request.form.get("id_wikidata", None))


        # Récupérer l'objet Maison à mettre à jour
            maison_a_mettre_a_jour = Maisons.query.filter(Maisons.denomination == nom_maison).first()

            # Vérifier si l'objet existe
            if maison_a_mettre_a_jour:
                # Mettre à jour les propriétés de l'objet avec les nouvelles valeurs
                maison_a_mettre_a_jour.id = id
                maison_a_mettre_a_jour.adresse = adresse
                maison_a_mettre_a_jour.commune = commune
                maison_a_mettre_a_jour.code_postal = code_postal
                maison_a_mettre_a_jour.code_INSEE = code_INSEE
                maison_a_mettre_a_jour.dpmt = dpmt
                maison_a_mettre_a_jour.region = region
                maison_a_mettre_a_jour.pays = pays
                maison_a_mettre_a_jour.latitude = latitude
                maison_a_mettre_a_jour.longitude = longitude
                maison_a_mettre_a_jour.date_label = date_label
                maison_a_mettre_a_jour.type = Domaine[type]
                maison_a_mettre_a_jour.museeFrance = museeFrance
                maison_a_mettre_a_jour.monumentsInscrits = monumentsInscrits
                maison_a_mettre_a_jour.monumentsClasses = monumentsClasses
                maison_a_mettre_a_jour.nombreSPR = nombreSPR
                maison_a_mettre_a_jour.idWikidata = idWikidata

                # Effectuez l'opération de mise à jour
                db.session.commit()
                print("insertion faite")

                # Rediriger vers une page de confirmation ou une autre page appropriée
                #return redirect(url_for('info_maisons', nom_maisons=nom_maison))
            else:
                print("Aucun information sur cette maison.")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        db.session.rollback()

    return render_template("pages/update_maisons.html", 
            sous_titre= "Update maisons", 
            form=form, 
            donnees=donnees)