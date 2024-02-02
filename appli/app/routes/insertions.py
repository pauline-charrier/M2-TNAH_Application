from ..app import app, db
from flask import render_template, request
from ..models.data import Maisons, Personnes
from ..models.formulaires import InsertionMaison
from ..utils.transformations import  clean_arg

@app.route("/insertions/maisons", methods=['GET', 'POST'])
def insertion_maisons():
    form = InsertionMaison() 

    if form.validate_on_submit():
        id =  clean_arg(request.form.get("id", None))
        denomination =  clean_arg(request.form.get("denomination", None))
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
            type = type,
            museeFrance=museeFrance,
            monumentsClasses=monumentsClasses,
            monumentsInscrits=monumentsInscrits,
            nombreSPR=nombreSPR, 
            idWikidata=idWikidata)

        db.session.add(nouvelle_maison)
        db.session.commit()
    
    return render_template("pages/insertion_maisons.html", 
            sous_titre= "Insertion maisons" , 
            form=form)