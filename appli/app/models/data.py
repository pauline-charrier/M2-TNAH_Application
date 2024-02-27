from ..app import app, db
from ..utils.transformations import nettoyage_string_to_int
from enum import Enum
from unidecode import unidecode

class Domaine(Enum):
    TYPE1 = 'Littérature et idées'
    TYPE2 = 'Sciences et industrie'
    TYPE3 = 'Arts et architecture'
    TYPE4 = 'Histoire et politique'
    TYPE5 = 'Musique, théâtre et cinéma'

    @classmethod
    def obtenir_clef(cls, value):
        for member in cls:
            if member.value == value:
                return member.name

    @classmethod
    def comparer_valeurs(cls, value):
        for member in cls:
            if value.lower() in member.value.lower():
                return member.name

class Genre(Enum):
    TYPE1 = 'masc'
    TYPE2 = 'fem'
    TYPE3 = 'couple/famille'

    @classmethod
    def obtenir_clef(cls, value):
        for member in cls:
            if member.value == value:
                return member.name

class Maisons(db.Model):
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
    
    def get_denomination_sans_accents(self):
        return unidecode(self.denomination) if self.denomination else None

    def get_region_sans_accents(self):
        return unidecode(self.region) if self.region else None
    
    def get_pays_sans_accents(self):
        return unidecode(self.pays) if self.pays else None

class Personnes(db.Model):
    __tablename__ = "personnes"
    idWikidata = db.Column(db.String(20), primary_key=True)
    nomIllustre = db.Column(db.String(45))
    ddn = db.Column(db.Integer) #on ne garde que l'année
    ddm = db.Column(db.Integer) #idem
    genre = db.Column(db.Enum(Genre))
    image = db.Column(db.String(300))
    article = db.Column(db.String(300))
    maison = db.relationship(
        "Maisons",
        backref = "maisons", 
        lazy = "dynamic"
    )

    def siecles_vie(self):
        annee_naissance = self.ddn
        annee_mort = self.ddm
        duree_vie = annee_mort-annee_naissance
        siecle_naissance = self.ddn // 100
        siecle_mort = self.ddm // 100

        if siecle_naissance != siecle_mort:
            if (siecle_mort*100)-annee_naissance <=30 and duree_vie >=70:
                return siecle_mort
            elif (siecle_mort*100)-annee_naissance <=30 and duree_vie < 70:
                return siecle_mort, siecle_naissance
            else:
                return siecle_naissance
        else:
            return siecle_naissance
        
    def get_distinct_siecles(self):
        distinct_siecles = db.session.query(Personnes.siecles_vie.distinct()).all()
        return [siecles_vie[0] for siecles_vie in distinct_siecles]
        

'''

    def __repr__(self):
        return '<Area %r>' % (self.total) 

class Boundaries(db.Model):
    __tablename__ = "boundaries"

    total = db.Column(db.String(100), primary_key=True)
    border_countries = db.Column(db.String(1000))
    note = db.Column(db.String(1000))

    # clés étrangères
    id = db.Column(
        db.String(100),  
        db.ForeignKey('country.id')
    )

    def total_int(self):
        return nettoyage_string_to_int(self.total)

    def __repr__(self):
        return '<Boundaries %r>' % (self.total) 

class Elevation(db.Model):
    __tablename__ = "elevation"

    highest_point = db.Column(db.String(100), primary_key=True)
    lowest_point = db.Column(db.String(100))
    mean_elevation = db.Column(db.String(100))
    note =db.Column(db.Text)

    # clés étrangères
    id = db.Column(
        db.String(100),  
        db.ForeignKey('country.id')
    )

    def __repr__(self):
        return '<Elevation %r>' % (self.highest_point)

class Geography(db.Model):
    __tablename__ = "geography"

    location = db.Column(db.String(1000), primary_key=True)
    coordinates = db.Column(db.String(100))
    coastline = db.Column(db.String(100))
    climate = db.Column(db.Text)
    terrain = db.Column(db.Text)
    irrigated_land = db.Column(db.Text)
    fresh_water_lakes = db.Column(db.Text)
    salted_water_lakes = db.Column(db.Text)
    major_rivers = db.Column(db.Text)
    major_watersheds = db.Column(db.Text)
    major_aquifers = db.Column(db.Text)
    population_distribution = db.Column(db.Text)
    natural_hazards = db.Column(db.Text)
    geography_note = db.Column(db.Text) 

    # clés étrangères
    id = db.Column(
        db.String(100),  
        db.ForeignKey('country.id')
    )

    def coastline_int(self):
        return nettoyage_string_to_int(self.coastline)

    def irrigated_land_int(self):
        return nettoyage_string_to_int(self.irrigated_land)

    def __repr__(self):
        return '<Geography %r>' % (self.location)

class Landuse(db.Model):
    __tablename__ = "landuse"

    landuse_id = db.Column(db.Integer, primary_key=True)
    agricultural_land = db.Column(db.Text)
    arable_land = db.Column(db.Text)
    permanent_crops = db.Column(db.Text)
    permanent_pasture = db.Column(db.Text)
    forest = db.Column(db.Text)
    other = db.Column(db.Text)

    # clés étrangères
    id = db.Column(
        db.String(100),  
        db.ForeignKey('country.id')
    )

    def __repr__(self):
        return '<Landuse %r>' % (self.landuse_id)

class Map(db.Model):
    __tablename__ = "map"

    id = db.Column(db.String(100))
    name = db.Column(db.Text, primary_key=True)

    def __repr__(self):
        return '<Map %r>' % (self.name)

class Resources(db.Model):
    __tablename__ = "resources"

    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.Text)

    def __repr__(self):
        return '<Resources %r>' % (self.name)

    def get_resourceid(self):
        return Resources.query.filter(Resources.name == self.name).first().id

    def get_pays(self):
        pays_par_ressource = []

        for pays in Country.query.all():
            for ressource in pays.resources:
                if ressource == self:
                    if pays.name not in pays_par_ressource:
                        pays_par_ressource.append(pays.name)
        
        return pays_par_ressource
'''