from ..app import app, db
from flask import render_template, request, flash
from sqlalchemy import distinct
from ..models.data import Maisons, Personnes, Domaine, Genre
from ..models.formulaires import InsertionMaison, InsertionPersonne, UpdateMaisons
from ..utils.transformations import  clean_arg

@app.route("/update/maisons/<string:nom_maisons>", methods=['GET', 'POST'])
def update_maisons(nom_maisons):
    distinct_regions = Maisons.get_distinct_regions()
    form = UpdateMaisons()
    form.idWikidata.choices = [('','')] + [(maisons.idWikidata, maisons.idWikidata) for maisons in Maisons.query.all()]
    form.region.choices = [('','')] + [(region, region) for region in distinct_regions]
    form.type.choices = [('','')] + [(domaine.value, domaine.value) for domaine in Domaine]
    donnees= Maisons.query.filter(Maisons.denomination == nom_maisons).first()

    try:
        if form.validate_on_submit():
            id =  clean_arg(request.form.get("id", None))
            adresse =  clean_arg(request.form.get("adresse", None))
            commune =  clean_arg(request.form.get("commune", None))
            code_postal =  clean_arg(request.form.getlist("code_postal", None))
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

        nouvelle_maison = Maisons(id=id, 
            denomination=nom_maisons,
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
            type = type,
            museeFrance=museeFrance,
            monumentsClasses=monumentsClasses,
            monumentsInscrits=monumentsInscrits,
            nombreSPR=nombreSPR, 
            idWikidata=idWikidata)

        db.session.add(nouvelle_maison)
        db.session.commit()

        flash("La mise à jour de la maison "+ nom_maisons + " s'est correctement déroulée", 'info')
    
    except Exception as e :
        print(e)
        db.session.rollback()

    return render_template("pages/update_maisons.html", 
            sous_titre= "Update maisons", 
            form=form, 
            donnees=donnees)