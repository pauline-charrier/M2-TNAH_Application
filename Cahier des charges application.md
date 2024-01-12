Pour le cahier des charges, voici ce que j’attends (et qui vous fera gagner du temps ensuite pour le développement) :

# 1. Description générale de l’application et de son objectif, description du ou des jeux de données. 

Notre application permettra une visualisation et une évaluation du label "Maison des Illustres" et de son évolution. 

Le label "Maison des Illustres" est une décerné en France à des maisons, châteaux ou ateliers ayant appartenu à des personnalités éminentes qui ont marqué l'histoire par leurs réalisations dans les domaines de la politique, de la culture, des sciences, ou des arts. Ces lieux doivent alors proposer des visites *a minima* 40 jours dans l'année, mettant en avant leur valeur patrimoniale et l'influence de "l'illustre personne" dans l'Histoire. L’attribution d’un tel label représente une reconnaissance officielle de l’intérêt patrimonial de la Maison. Le label est également un dispositif de valorisation, qui s’accompagne d’avantages divers, en terme de visibilité notamment. De son attribution découle donc des enjeux de représentation et la mise en valeur d'une large diversité de personnes et de lieux avec un intérêt patrimonial. Est-ce vraiiment le cas ? 

Le but de cette application sera de permettre un suivi de la diversité des lieux labélisés et des personnes qu'elles représentent, ainsi qu'un outil de localisation de ces bâtiments, participant ainsi à leur visibilité.

Notre jeu de donnée est une liste des maisons labellisées. Les attributs de chaque maison sont les : 
- coordonnées géographiques
- (code postal)
- (on l'espère) les données de fréquentation sur 2022
- plusieurs booléen pour détecter une / des autres labellisations parmi : musées de France, monuments historiques, monuments nationaux, jardins remarquables, 
- le nom de l'illustre personne à laquelle a appartenu la maison
- les dates de naissance et de mort de cette personne
- le genre de cette personne 
- le domaine dans lequel elle s'est illustrée
- son genre
- la page wikipedia de la personne
- une photo ? 

Les collectivités pourront alors obtenir un catalogue des entités labellisées filtrable en fonction des données de multilabellisation ou des informations concernant les illustres. Elles pourront aussi obtenir une carte pour filtrer les données en fonction de leur emplacement. 

La visualisation de ces données, que l'on pourra mettre à jour, permettra d'évaluer un certain nombre de critères : 
- répartition géographique
- diversité des personnes qualifiées "illustres"
- proportion de multilabellisations

Une telle évaluation pourra éventuellement aider à orienter les labellisations futures, pour aller vers une répartition égale sur le territoire, une large diversité de personnes représentées ou encore pour comparer l'efficacité des labels en terme de visibilité. 

# 2. Liste des fonctionnalités souhaitées (catalogue, cartes, graphiques, actions sur les données, etc)

- Affichage d'un catalogue sous forme de liste avec la possibilité d'appliquer des filtres
- Affichage d'une carte avec la possibilité d'appliquer des filtres
- Visualisation des données sous la forme de graphiques

# 3. Tenter de faire le modèle de données de la base de données (liste des tables, des colonnes, et des relations entre tables)

```Python
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MaisonsIllustres(db.Model):
    __tablename__ = "MaisonsIllustres"

    #id = db.Column(db.Integer, primary_key=True) ??????
    denomination = db.Column(db.String(45), primary_key=True)
    dpmt = db.Column(db.String(45))  # ou région ???
    coordonnees = db.Column(db.ARRAY(db.DECIMAL(9, 6)))
    museeFrance = db.Column(db.Boolean)
    jardinRemarquable = db.Column(db.Boolean)
    archiModerne = db.Column(db.Boolean)
    monumentsNationaux = db.Column(db.Boolean)
    monumentsHistoriques = db.Column(db.Boolean)
    freq2021 = db.Column(db.Integer)  # si on a les données
    nomIllustre = db.Column(db.String(45))
    dobIllustres = db.Column(db.DateTime)
    dodIllustres = db.Column(db.DateTime)
    typeIllustre = db.Column(db.Enum(Domaine))  # ou Str
    genreIllustre = db.Column(db.Enum(Genre))  # ou Str
    wikiIllustre = db.Column(db.String(300))
    image = db.Column(db.String(500))

class Domaine(Enum):
    TYPE1 = 'Littérature et idées'
    TYPE2 = 'Sciences et industrie'
    TYPE3 = 'Arts et architecture'
    TYPE4 = 'Histoire et politique'
    TYPE5 = 'Musique, théâtre et cinéma'

class Genre(Enum):
    TYPE1 = 'masc'
    TYPE2 = 'fem'

```

# 4. Liste des principales routes envisagées et description de leur fonction

- une route "all" pour afficher l'intégralité un catalogue avec l'intégralité des enregistrements. Rajout de lien vers les routes "instance". 
- une route "instance" avec un paramètre (dénomination de la maison) pour afficher l'intégralité des informations concernant l'instance, dans un template travaillé.
- une route "map" qui mène à une carte de la répartition des entités sur le territoire français **(est-il possible d'appliquer des filtres ?)** *Exemple :*

![](https://lh7-us.googleusercontent.com/GzUGyTkDCvZBgVq7AucL2jAp0diDTxK_wVrR3cfwCOPvunEmafqMh1b04gMnPSD2gKtVSYKPvVEPexLAYfoEMP4MpM1kaQf9_xZtPnJPpmWQ6s0sq_OAFYUCtId9fWryOggTlx1U6jmC-jR2kNK15Rg)
- une route "add" qui offre un formulaire pour rajouter des enregistrements 
- une route "region" ou "département" qui permet d'afficher maisons selon les régions / département. 
- Une route "label" qui permet l'affichage des maisons en fonction de leurs autres labels
- Une route "date" qui permet l'affichage des maisons en fonction de la période à laquelle a vécu l'illustre (granularité : par siècle). 
- Une route "genre" qui permet l'affichage des maisons en fonction du genre de l'illustre.
- Une route "domaine" qui permet l'affichage des maisons en fonction du domaine dans lequel la personne s'est illustrée ('Littérature et idées', 'Sciences et industrie', 'Arts et architecture', 'Histoire et politique', 'Musique, théâtre et cinéma').
- **Est-il possible de faire une route "request" qui offre un formulaire permettant d'appliquer plusieurs filtre ? Plutôt travailler "orienté objet" avec des méthodes dans le modèle de données ?** 
- route "graphique" affiche deux ou trois visualisations (choisir les plus réussies)


# 5. 2-3 étapes pour le développement, et la charge estimée (en heures ou en personne) pour les gros blocs de développement

- Structure (squelette) de l'application, relier la base de données (6 heures) : Clara + Kutay consultable
- Modèle de données : Clara 
- Construction des routes (20 heures) : Kutay + Clara (en parallèle de la construction des templates)
- Construction des templates (20 heures) : Clara + Pauline (en parralèle de la construction des templates)
- Construction des statics et les inclure dans les templates (6 heures): Clara + Pauline + Maddalena
- Esthétique des des templates : Clara + Maddale
- débogage (5 heures) : Kutay + Clara


**BD rel avec plusieurs table ?**
