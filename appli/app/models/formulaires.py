from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField

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
    region =  StringField("region", validators=[])
    code_INSEE =  StringField("code_INSEE", validators=[])
    pays =  StringField("pays", validators=[])
    date_label =  StringField("date_label", validators=[])
    latitude =  StringField("latitude", validators=[])
    longitude =  StringField("longitude", validators=[])
    museeFrance =  BooleanField("musee_france", validators=[])
    monumentsInscrits =  BooleanField("monuments_inscrits", validators=[])
    monumentsClasses =  BooleanField("monuments_classes", validators=[])
    nombreSPR =  StringField("nombre_SPR", validators=[])
    type =  SelectField("type", validators=[])
    idWikidata =  StringField("id_wikidata", validators=[])