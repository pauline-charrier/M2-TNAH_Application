from ..app import app, db
from flask import render_template, request, redirect, url_for, flash
from ..models.data import Maisons, Personnes
from ..utils.transformations import  clean_arg

#la route qui supprime l

@app.route("/suppression/maisons/<string:nom_maison>", methods=['GET', 'POST'])
def sup_maison(nom_maison):

    try:
        if request.method == 'POST':
            nom_maison_a_supp = request.form.get('maison_a_supp')
            maison_a_supp = Maisons.query.filter(denomination=nom_maison_a_supp)
            personne_a_supp = Personnes.query.filter(idWikidata=maison_a_supp.idWikidata)
            db.session.delete(maison_a_supp)
            db.session.delete(personne_a_supp)
            db.session.commit()
            flash('La maison a été supprimée avec succès.', 'success')

    except Exception as e :
        print(e)
    
    return redirect(url_for('maisons'))

