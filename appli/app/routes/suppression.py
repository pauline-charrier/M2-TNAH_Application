from ..app import app, db
from flask import render_template, request, redirect, url_for, flash
from ..models.data import Maisons, Personnes
from ..utils.transformations import  clean_arg

@app.route("/suppression/pays", methods=['GET', 'POST'])
def sup_maison():

    try:
        if request.method == 'POST':
            nom_maison_a_supp = request.form.get('maison_a_supp')
            maison_a_supp = Maisons.query.filter(denomination=nom_maison_a_supp)
            db.session.delete(maison_a_supp)
            db.session.commit()
            flash('La maison a été supprimée avec succès.', 'success')

    except Exception as e :
        print(e)
    
    return redirect(url_for('maisons'))

