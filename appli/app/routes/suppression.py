from ..app import app, db
from flask import render_template, request, redirect, url_for, flash
from ..models.data import Maisons, Personnes
from ..utils.transformations import  clean_arg


@app.route("/suppression/maisons/<string:nom_maison>", methods=['GET', 'POST'])
def sup_maison(nom_maison):
    """
    Gère la route "/suppression/maisons/<nom_maison>" pour la suppression d'une maison.

    Parameters
    ----------
    nom_maison : str
        Le nom de la maison à supprimer. Elle est envoyée par l'input du bouton dans le template. 

    Returns
    -------
    redirect
        Redirige vers la page principale du catalogue des maisons après la suppression.
    """

    try:
        if request.method == 'POST':
            # Récupère la maison à supprimer en fonction de l'input
            maison_a_supp = Maisons.query.filter(Maisons.denomination == nom_maison).first()
            db.session.delete(maison_a_supp)
            
            # Supprime la maison puis passe la suppression à la base de donnée. Si la suppression est effective, l'utilisateur reçoit un message
            db.session.commit()
            flash('La maison a été supprimée avec succès.', 'success')

    except Exception as e :
        print(e)
        flash('Une erreur s\'est produite lors de la suppression de la maison.', 'error')

    return redirect(url_for('maisons'))



@app.route("/suppression/personnes/<string:nom_personne>", methods=['GET', 'POST'])
def sup_personne(nom_personne):
    """
    Gère la route "/suppression/personnes/<nom_personne>" pour la suppression d'une personne.

    Parameters
    ----------
    nom_personne : str
        Le nom de la personne à supprimer.

    Returns
    -------
    redirect
        Redirige vers le catalogue de gestion des personnes après la suppression.
    """

    try:
        if request.method == 'POST':
            # Récupère la personne à supprimer en fonction de l'inupt 
            personne_a_supp = Personnes.query.filter(Personnes.nomIllustre == nom_personne).first()
            db.session.delete(personne_a_supp)

            # Supprime la personne et transmission de l'action dans la base de données.
            db.session.commit()
            flash('La personne a été supprimée avec succès.', 'success')

    except Exception as e :
        print(e)
        flash('Une erreur s\'est produite lors de la suppression de la maison.', 'error')

    return redirect(url_for('personnes'))