from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class InsertionPersonne(FlaskForm):
    idWikidata =  StringField("id_illustre", validators=[]) 
    nomIllustre =  StringField("nom_illustre", validators=[])
    ddn =  StringField("ddn", validators=[])
    ddm =  StringField("ddm", validators=[])
    genre =  SelectField("genre", choices=[], validators=[])
    image =  StringField("image", validators=[])
    article =  StringField("article", validators=[])

class InsertionMaison(FlaskForm):
    id =  StringField("id", validators=[]) 
    denomination =  StringField("denomination", validators=[])
    code_postal =  StringField("code_postal", validators=[])
    adresse =  StringField("adresse", validators=[])
    commune =  StringField("commune", validators=[])
    dpmt =  StringField("dpmt", validators=[])
    region =  SelectField("region", choices=[], validators=[])
    code_INSEE =  StringField("code_INSEE", validators=[])
    pays =  StringField("pays", validators=[])
    date_label =  StringField("date_label", validators=[])
    latitude =  StringField("latitude", validators=[])
    longitude =  StringField("longitude", validators=[])
    museeFrance =  BooleanField("musee_france", validators=[])
    monumentsInscrits =  BooleanField("monuments_inscrits", validators=[])
    monumentsClasses =  BooleanField("monuments_classes", validators=[])
    nombreSPR =  SelectField("Nombre_SPR", choices=[(None, '')] + [(i, str(i)) for i in range(1, 11)])
    type =  SelectField("type", choices=[], validators = [])
    idWikidata =  SelectField("id_wikidata", choices = [], validators=[])


class UpdateMaisons(FlaskForm):
    id =  StringField("id", validators=[DataRequired()]) 
    denomination =  StringField("denomination", validators=[])
    code_postal =  StringField("code_postal", validators=[])
    adresse =  StringField("adresse", validators=[])
    commune =  StringField("commune", validators=[])
    dpmt =  StringField("dpmt", validators=[])
    region =  SelectField("region", choices=[], validators=[])
    code_INSEE =  StringField("code_INSEE", validators=[])
    pays =  StringField("pays", validators=[])
    date_label =  StringField("date_label", validators=[])
    latitude =  StringField("latitude", validators=[])
    longitude =  StringField("longitude", validators=[])
    museeFrance =  BooleanField("musee_france", validators=[])
    monumentsInscrits =  BooleanField("monuments_inscrits", validators=[])
    monumentsClasses =  BooleanField("monuments_classes", validators=[])
    nombreSPR =  SelectField("Nombre_SPR", choices=[(None, '')] + [(i, str(i)) for i in range(1, 11)]) 
    type =  SelectField("type", choices=[], validators = [])
    idWikidata =  SelectField("id_wikidata", choices = [], validators=[])


class Recherche(FlaskForm):
    denomination =  StringField("denomination", validators=[])
    type =  SelectField("type", choices=[], validators = [])
    region = SelectField("region", choices=[], validators=[])
    genre = SelectField("genre", choices=[], validators=[])
    #periode = SelectField("periode", choices=[], validators=[])
    museeFrance =  BooleanField("musee_france", default=False)
    monumentsInscrits =  BooleanField("monuments_inscrits", default=False)
    monumentsClasses =  BooleanField("monuments_classes", default=False)

