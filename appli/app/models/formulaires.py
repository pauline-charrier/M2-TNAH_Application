from flask_wtf import FlaskForm
from wtforms.validators import NumberRange, optional, DataRequired
from wtforms import StringField, SelectField, BooleanField, IntegerField, FloatField, HiddenField
from wtforms.widgets import HiddenInput


class InsertionPersonne(FlaskForm):
    idWikidata =  StringField("id_illustre", validators=[DataRequired()]) 
    nomIllustre =  StringField("nom_illustre", validators=[DataRequired()])
    ddn =  StringField("ddn", validators=[optional()])
    ddm =  StringField("ddm", validators=[optional()])
    genre =  SelectField("genre", choices=[], validators=[optional()])
    image =  StringField("image", validators=[optional()])
    article =  StringField("article", validators=[optional()])

class InsertionMaison(FlaskForm):
    id =  StringField("id", validators=[DataRequired()]) 
    denomination =  StringField("denomination", validators=[DataRequired()])
    code_postal =  StringField("code_postal", validators=[optional()])
    adresse =  StringField("adresse", validators=[optional()])
    commune =  StringField("commune", validators=[optional()])
    dpmt =  StringField("dpmt", validators=[optional()])
    region =  SelectField("region", choices=[], validators=[optional()])
    code_INSEE =  StringField("code_INSEE", validators=[optional()])
    pays =  StringField("pays", validators=[optional()])
    date_label =  StringField("date_label", validators=[optional()])
    latitude = FloatField("Latitude", validators=[optional(), NumberRange(min=-90, max=90)])
    longitude = FloatField("Longitude", validators=[optional(), NumberRange(min=-180, max=180)])
    museeFrance =  BooleanField("musee_france", validators=[optional()])
    monumentsInscrits =  BooleanField("monuments_inscrits", validators=[optional()])
    monumentsClasses =  BooleanField("monuments_classes", validators=[optional()])
    nombreSPR =  SelectField("Nombre_SPR", choices=[('', '')] + [(i, i) for i in range(0, 11)], validators = [optional()])
    type =  SelectField("type", choices=[], validators = [optional()])
    nomIllustre =  SelectField("nomIllustre", choices = [], validators=[optional()])


class UpdateMaisons(FlaskForm):
    denomination =  StringField("denomination", validators=[DataRequired()])
    code_postal =  StringField("code_postal", validators=[optional()])
    adresse =  StringField("adresse", validators=[optional()])
    commune =  StringField("commune", validators=[optional()])
    dpmt =  StringField("dpmt", validators=[optional()])
    region =  SelectField("region", choices=[], validators=[optional()])
    code_INSEE =  StringField("code_INSEE", validators=[optional()])
    pays =  StringField("pays", validators=[optional()])
    date_label =  StringField("date_label", validators=[optional()])
    latitude = FloatField("Latitude", validators=[optional(), NumberRange(min=-90, max=90)])
    longitude = FloatField("Longitude", validators=[optional(), NumberRange(min=-180, max=180)])
    museeFrance =  BooleanField("musee_france", validators=[optional()])
    monumentsInscrits =  BooleanField("monuments_inscrits", validators=[optional()])
    monumentsClasses =  BooleanField("monuments_classes", validators=[optional()])
    nombreSPR = IntegerField("Nombre_SPR", validators=[optional()])
    type =  SelectField("type", choices=[], validators = [optional()])
    nomIllustre = SelectField("nomIllustre", choices = [optional()], validators=[optional()])


class Recherche(FlaskForm):
    page_num = HiddenField(widget=HiddenInput, default=1)
    denomination =  StringField("denomination", validators=[])
    type =  SelectField("type", choices=[], validators = [])
    region = SelectField("region", choices=[], validators=[])
    departement = SelectField("departement", choices=[])
    genre = SelectField("genre", choices=[], validators=[])
    museeFrance =  BooleanField("musee_france", default=False)
    monumentsInscrits =  BooleanField("monuments_inscrits", default=False)
    monumentsClasses =  BooleanField("monuments_classes", default=False)
    date_label = SelectField("date_label", choices=[], validators=[])

class UpdatePersonnes(FlaskForm):
    nomIllustre =  StringField("nomIllustre", validators=[DataRequired()])
    genre =  SelectField("genre", choices=[], validators = [optional()])
    ddn = StringField("ddn", validators = [optional()])
    ddm = StringField("ddm", validators = [optional()])
    image = StringField("image", validators = [optional()])
    article = StringField("article", validators = [optional()])
    
