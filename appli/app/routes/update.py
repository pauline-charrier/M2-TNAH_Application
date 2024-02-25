from ..app import app, db
from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import distinct, text
from ..models.data import Maisons, Personnes, Domaine, Genre
from ..models.formulaires import InsertionMaison, InsertionPersonne, UpdateMaisons
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
    form.date_label.data = str(maison.date_label)
    form.latitude.data = str(maison.latitude) 
    form.longitude.data = str(maison.longitude) 
    form.museeFrance.data = maison.museeFrance
    form.monumentsInscrits.data = maison.monumentsInscrits
    form.monumentsClasses.data = maison.monumentsClasses
    form.nombreSPR.data = str(maison.nombreSPR) if maison.nombreSPR is not None else None
    form.type.data = maison.type.value
    form.nomIllustre.data = personne.nomIllustre if personne else None

    #valeur_domaine = Domaine.obtenir_valeur(donnees.type)
    #form.type.data = Domaine.obtenir_valeur(valeur_domaine)
    #ne fonctionne pas
    #form.idWikidata.choices = [('','')] + [(personnes.idWikidata, personnes.idWikidata) for personnes in Personnes.query.all()]
    form.nomIllustre.choices = [('','')] + [(personnes.nomIllustre, personnes.nomIllustre) for personnes in Personnes.query.all()]
    form.region.choices = [('','')] + [(region, region) for region in distinct_regions]
    form.type.choices = [('','')] + [(domaine.value, domaine.value) for domaine in Domaine]

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

            if nomIllustre:
                id_pers = Personnes.query.filter(Personnes.nomIllustre == nomIllustre).first()


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
                maison_a_mettre_a_jour.type = Domaine.obtenir_clef(type)
                maison_a_mettre_a_jour.museeFrance = True if museeFrance == 'y' else False
                maison_a_mettre_a_jour.monumentsInscrits = True if monumentsInscrits == 'y' else False
                maison_a_mettre_a_jour.monumentsClasses = True if monumentsClasses == 'y' else False
                maison_a_mettre_a_jour.nombreSPR = nombreSPR
                if nomIllustre:
                    pers_a_lier = Personnes.query.filter(Personnes.nomIllustre == nomIllustre).first()
                    maison_a_mettre_a_jour.idWikidata = pers_a_lier.idWikidata

                # Effectuez l'opération de mise à jour
                db.session.commit()
                print("mise à jour effectuée")

                #Rediriger vers une page de confirmation ou une autre page appropriée
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