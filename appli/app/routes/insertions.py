from ..app import app, db
from flask import render_template, request, flash
from sqlalchemy import distinct
from ..models.data import Maisons, Personnes, Domaine, Genre
from ..models.formulaires import InsertionMaison, InsertionPersonne
from ..utils.transformations import  clean_arg

@app.route("/insertions/maisons", methods=['GET', 'POST'])
def insertion_maisons():
    form = InsertionMaison()
    form.idWikidata.choices = [('','')] + [(maisons.idWikidata, maisons.idWikidata) for maisons in Maisons.query.all()]
    form.region.choices = [('','')] + [(maisons.region, maisons.region) for maisons in db.session.query(Maisons.region).distinct()]
    form.type.choices = [('','')] + [(domaine.value, domaine.value) for domaine in Domaine]

    try:
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

        flash("L'insertion du pays "+ denomination + " s'est correctement déroulée", 'info')
    
    except Exception as e :
        print(e)
        db.session.rollback()

    return render_template("pages/insertion_maisons.html", 
            sous_titre= "Insertion maisons" , 
            form=form)

@app.route("/insertions/personnes", methods=['GET', 'POST'])
def insertion_personnes():
    form = InsertionPersonne()
    form.genre.choices = [('','')] + [(genre.value, genre.value) for genre in Genre]

    try:
        if form.validate_on_submit():
            idWikidata =  clean_arg(request.form.get("id_illustre", None))
            nomIllustre =  clean_arg(request.form.get("nom_illustre", None))
            ddn =  clean_arg(request.form.get("ddn", None))
            ddm=  clean_arg(request.form.get("ddm", None))
            genre =  clean_arg(request.form.getlist("genre", None))
            image =  clean_arg(request.form.get("image", None))
            article =  clean_arg(request.form.get("article", None))

            nouvelle_personne = Personnes(idWikidata=idWikidata, 
                nomIllustre=nomIllustre,
                ddn=ddn,
                ddm=ddm,
                genre=genre,
                image=image,
                article=article)
            
            db.session.add(nouvelle_personne)
            db.session.commit()

            flash("L'insertion du pays "+ nomIllustre + " s'est correctement déroulée", 'info')

    except Exception as e :
        print(e)
        db.session.rollback()

    return render_template("pages/insertion_personnes.html", 
            sous_titre= "Insertion personne", 
            form=form)