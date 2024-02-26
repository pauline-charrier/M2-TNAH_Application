from ..app import app, db
from flask import render_template, request, redirect, url_for, flash
from ..models.data import Maisons, Personnes
from ..utils.transformations import  clean_arg


@app.route("/suppression/maisons/<string:nom_maison>", methods=['GET', 'POST'])
def sup_maison(nom_maison):

    try:
        if request.method == 'POST':
            #nom_maison_a_supp = request.form.get(nom_maison)
            maison_a_supp = Maisons.query.filter(Maisons.denomination == nom_maison).first()
            db.session.delete(maison_a_supp)

            if maison_a_supp.idWikidata:
                personne_a_supp = Personnes.query.filter(Personnes.idWikidata == maison_a_supp.idWikidata).first()
                db.session.delete(personne_a_supp)
            
            db.session.commit()
            flash('La maison a été supprimée avec succès.', 'success')

    except Exception as e :
        print(e)
        flash('Une erreur s\'est produite lors de la suppression de la maison.', 'error')

    return redirect(url_for('maisons'))

