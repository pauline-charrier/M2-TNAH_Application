from ..app import app, db
from ..utils.transformations import normaliser
from enum import Enum
from flask import url_for

class Domaine(Enum):
    """
    Une énumération représentant différents types de domaines.

    Members
    -------
    TYPE1 : Domaine
        Premier type de domaine - 'Littérature et idées'
    TYPE2 : Domaine
        Deuxième type de domaine - 'Sciences et industrie'
    TYPE3 : Domaine
        Troisième type de domaine - 'Arts et architecture'
    TYPE4 : Domaine
        Quatrième type de domaine - 'Histoire et politique'
    TYPE5 : Domaine
        Cinquième type de domaine - 'Musique, théâtre et cinéma'
    """

    TYPE1 = 'Littérature et idées'
    TYPE2 = 'Sciences et industrie'
    TYPE3 = 'Arts et architecture'
    TYPE4 = 'Histoire et politique'
    TYPE5 = 'Musique, théâtre et cinéma'

    @classmethod
    def obtenir_clef(cls, value):

        """
        méthode pout obtenir la clé associée à une valeur donnée dans l'énumération Domaine.

        Parameters
        ----------
        value : str, required
            La valeur dont on veut obtenir la clé.

        Returns
        -------
        str
            Le nom de la clé associée à la valeur, ou None si la valeur n'est pas trouvée.
        """

        for member in cls:
            if member.value == value:
                return member.name

    @classmethod
    def comparer_valeurs(cls, value):

        """
        Compare une valeur donnée avec les valeurs normalisées de l'énumération Domaine.

        Parameters
        ----------
        value : str, required
            La valeur à comparer.

        Returns
        -------
        str
            Le nom de la clé associée à la première valeur correspondante normalisée, ou None si aucune correspondance n'est trouvée.
        """

        for member in cls:
            if normaliser(value) in normaliser(member.value):
                return member.name

class Genre(Enum):

    """
    Une énumération représentant différents genres.

    Members
    -------
    TYPE1 : Genre
        Premier genre - 'masculin'
    TYPE2 : Genre
        Deuxième genre - 'féminin'
    TYPE3 : Genre
        Troisième genre - 'couples/familles'
    """

    TYPE1 = 'masculin'
    TYPE2 = 'féminin'
    TYPE3 = 'couples/familles'

    @classmethod
    def obtenir_clef(cls, value):

        """
        méthode pout obtenir la clé associée à une valeur donnée dans l'énumération Genre.

        Parameters
        ----------
        value : str, required
            La valeur dont on veut obtenir la clé.

        Returns
        -------
        str
            Le nom de la clé associée à la valeur, ou None si la valeur n'est pas trouvée.
        """

        for member in cls:
            if member.value == value:
                return member.name

class Maisons(db.Model):

    """
    Classe représentant les bâtiments. 

    Attributes
    ----------
    id : sqlalchemy.sql.schema.Column
        Identifiant Mérimé du bâtiment labellisé. C'est la clé primaire. Cet attribut est une Column SQLALchemy.
    denomination : sqlalchemy.sql.schema.Column
        Nom du bâtiment
    code_postal : sqlalchemy.sql.schema.Column
    dpmt : sqlalchemy.sql.schema.Column
    region : sqlalchemy.sql.schema.Column
    adresse : sqlalchemy.sql.schema.Column
    commune : sqlalchemy.sql.schema.Column
    code_INSEE : sqlalchemy.sql.schema.Column
    pays : sqlalchemy.sql.schema.Column
        Localisation administrative du bâtiment
    date_label : sqlalchemy.sql.schema.Column
        date de labellisation
    latitude : sqlalchemy.sql.schema.Column
    longitude : sqlalchemy.sql.schema.Column
        Coordonnées géographiques du bâtiment
    museeFrance : sqlalchemy.sql.schema.Column
    momunmentInscrit : sqlalchemy.sql.schema.Column
    momunantClasse: sqlalchemy.sql.schema.Column
        Autres labels du bâtiment
    type : sqlalchemy.sql.schema.Column
        Adresse mail de l'utilisateur
    mail : sqlalchemy.sql.schema.Column
        Domaine de génie ou thème. Une liste de valeur est définie dans la classe Enum(Domaine)
    idWikidata : sqlalchemy.sql.schema.Column
        Clé étrangère : identifiant Wikidata de la personne ayant vécu dans le bâtiment

    Methods
    -------
    get_distinct_regions()
        permet d'obtenir l'ensemble des valeurs de l'attribut "region". 
        Cela permettra de créer facilement des listes déroulantes dans les formulaires.
    
    get_distinct_departement()
        permet d'obtenir l'ensemble des valeurs de l'attribut "dpmt" (pour départements). 
        Cela permettra de créer facilement des listes déroulantes dans les formulaires.
    
    get_distinct_regions()
        permet d'obtenir l'ensemble des valeurs de l'attribut "date_label" (pour la date de labellisation).
        Cela permettra de créer facilement des listes déroulantes dans les formulaires.
        
    """

    __tablename__ = "maisons"
    id = db.Column(db.String(500), primary_key=True)
    denomination = db.Column(db.String(45)) 
    code_postal = db.Column(db.String(5))
    dpmt = db.Column(db.String(45))
    region = db.Column(db.String(45))
    adresse = db.Column(db.String(45))
    commune = db.Column(db.String(45))
    code_INSEE = db.Column(db.String(5))
    pays = db.Column(db.String(45))
    date_label = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    museeFrance = db.Column(db.Boolean)
    monumentsInscrits = db.Column(db.Boolean)
    monumentsClasses = db.Column(db.Boolean)
    nombreSPR = db.Column(db.Integer, nullable=True)
    type = db.Column(db.Enum(Domaine))
    idWikidata = db.Column(
        db.String(20),  
        db.ForeignKey('personnes.idWikidata')) 
    
    @staticmethod
    def get_distinct_regions():
        distinct_regions = db.session.query(Maisons.region.distinct()).all()
        return [region[0] for region in distinct_regions]
    
    @staticmethod
    def get_distinct_departements():
        distinct_departements = db.session.query(Maisons.dpmt.distinct()).all()
        return [dp[0] for dp in distinct_departements]
    
    @staticmethod
    def get_distinct_date_label():
        distinct_date_label = db.session.query(Maisons.date_label.distinct()).order_by(Maisons.date_label).all()
        return [date[0] for date in distinct_date_label]
    
    def make_popup(self):
        url = url_for('info_maisons', nom_maisons=self.denomination)
        adresse = self.adresse +' '+ self.code_postal +' '+ self.commune
        icone_bootstrap = '<i class="bi bi-geo-alt"></i>'
        return f'''<p>{self.denomination}</p>
                <p>{icone_bootstrap} {adresse}</p>
                <a href="{url}" class="btn btn-primary text-dark">Plus d'informations</a>'''
    
class Personnes(db.Model):

    """
    Une classe représentant les personnes illustres associées aux maisons.

    Attributes
    ----------
    idWikidata : sqlalchemy.sql.schema.Column
         identifiant Wikidata de la personne ayant vécu dans le bâtiment. Cet attribut est la clé primaire.
    nomIllustre : sqlalchemy.sql.schema.Column
        Nom de la personne
    ddn : sqlalchemy.sql.schema.Column
    ddm : sqlalchemy.sql.schema.Column
        Dates de naissance et de mort de la personne (c'est un integer car on ne garde que l'année)
    genre : sqlalchemy.sql.schema.Column
        genre de la personne s'il peut être défini : Une liste de valeur est définie dans la classe Enum(Genre)
    image : sqlalchemy.sql.schema.Column
        une image de l'illustre personne sous la forme d'une URL
    article : sqlalchemy.sql.schema.Column
        URL de la page wikipedia de la personne illustre
    maison : sqlalchemy.sql.schema.relationship
        propriété de relation : n'existe pas en base

    """

    __tablename__ = "personnes"
    idWikidata = db.Column(db.String(20), primary_key=True)
    nomIllustre = db.Column(db.String(45))
    ddn = db.Column(db.Integer) 
    ddm = db.Column(db.Integer) 
    genre = db.Column(db.Enum(Genre))
    image = db.Column(db.String(300))
    article = db.Column(db.String(300))
    maison = db.relationship(
        "Maisons",
        backref = "maisons", 
        lazy = "dynamic"
    )


