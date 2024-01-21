# 1. Description générale de l’application et de son objectif, description du ou des jeux de données. 

Notre application permettra une visualisation et une évaluation du label "Maison des Illustres" et de son évolution. 

Le label "Maison des Illustres" est décerné en France à des maisons, châteaux ou ateliers ayant appartenu à des personnalités éminentes qui ont marqué l'histoire par leurs réalisations dans les domaines de la politique, de la culture, des sciences, ou des arts. Ces lieux doivent alors proposer des visites *a minima* 40 jours dans l'année, mettant en avant leur valeur patrimoniale et l'influence de "l'illustre personne" dans l'Histoire. L’attribution d’un tel label représente une reconnaissance officielle de l’intérêt patrimonial de la Maison. Le label est également un dispositif de valorisation, qui s’accompagne d’avantages divers, en terme de visibilité notamment. De son attribution découle donc des enjeux de représentation et la mise en valeur d'une large diversité de personnes et de lieux avec un intérêt patrimonial. Est-ce vraiment le cas ? 

Le but de cette application sera de permettre un suivi de la diversité des lieux labellisés et des personnes qu'elles représentent, ainsi qu'un outil de localisation de ces bâtiments, participant ainsi à leur visibilité.

Notre jeu de donnée est une liste des maisons labellisées. Les attributs de chaque maison sont les : 
- le nom de la maison
- coordonnées géographiques
- code postal
- département
- région
- code INSEE
- adresse
- code base MÉRIMÉE
- les données de fréquentation sur 2021
- plusieurs booléens pour détecter une / des autres labellisations parmi : musées de France, monuments historiques classés, monuments historiques inscrits.
- le nombre de sites patrimoniaux remarquables dans la commune
- le nom de l'illustre personne à laquelle a appartenu la maison
- les dates de naissance et de mort de cette personne
- le genre de cette personne 
- le domaine dans lequel elle s'est illustrée
- la page wikipedia de la personne
- l'identifiant wikidata de la personne

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
- Rajouter des enregistrements, compléter la base de données avec les nouvelles maison labellisées

# 3. Tenter de faire le modèle de données de la base de données (liste des tables, des colonnes, et des relations entre tables)

```Python
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Maisons(db.Model):
    __tablename__ = "Maisons"
    id = db.Column(db.String(500), primary_key=True)
    denomination = db.Column(db.String(45)) 
    code_postal = db.Column(db.String(5))
    dpmt = db.Column(db.String(45))
    region = db.Column(db.String(45))
    adresse = db.Column(db.String(45))
    commune = db.Column(db.String(45))
    code_INSEE = db.Column(db.String(5))
    pays = db.Column(db.String(45))
    coordonnees = db.Column(db.ARRAY(db.DECIMAL(9, 6)))
    museeFrance = db.Column(db.Boolean)
    monumentsInscrits = db.Column(db.Boolean)
    monumentsClassees = db.Column(db.Boolean)
    type = db.Column(db.Enum(domaine)) 

class Personnes(db.Model):
    __tablename__ = "Personnes"
    nomIllustre = db.Column(db.String(45))
    ddn = db.Column(db.DateTime) #on ne garde que l'année
    ddm = db.Column(db.DateTime) #idem
    genre = db.Column(db.Enum(genre)) 
    wikipedia = db.Column(db.String(300))
    idWikidata = db.Column(db.String(20))

class Domaine(Enum):
    TYPE1 = 'Littérature et idées'
    TYPE2 = 'Sciences et industrie'
    TYPE3 = 'Arts et architecture'
    TYPE4 = 'Histoire et politique'
    TYPE5 = 'Musique, théâtre et cinéma'


class Genre(Enum):
    TYPE1 = 'masc'
    TYPE2 = 'fem'
    TYPE3 = 'couple/famille'
```

# 4. Liste des principales routes envisagées et description de leur fonction

- une route "all" pour afficher l'intégralité du catalogue des maisons. Rajout de lien vers les routes "instance". 
- une route "instance" avec un paramètre (dénomination de la maison) pour afficher l'intégralité des informations concernant l'instance, avec les informations sur la personne, dans un template travaillé.
- une route "map" qui mène à une carte de la répartition des entités sur le territoire français **(est-il possible d'appliquer des filtres ?)**

*Exemple :*

![](https://lh7-us.googleusercontent.com/GzUGyTkDCvZBgVq7AucL2jAp0diDTxK_wVrR3cfwCOPvunEmafqMh1b04gMnPSD2gKtVSYKPvVEPexLAYfoEMP4MpM1kaQf9_xZtPnJPpmWQ6s0sq_OAFYUCtId9fWryOggTlx1U6jmC-jR2kNK15Rg)

- une route "add" qui offre un formulaire pour rajouter des enregistrements 
- une route "region" ou "département" qui permet d'afficher maisons selon les régions / département. 
- Une route "label" qui permet l'affichage des maisons en fonction de leurs autres labels.
- Une route "date" qui permet l'affichage des maisons en fonction de la période à laquelle a vécu l'illustre (granularité : par siècle). 
- Une route "genre" qui permet l'affichage des maisons en fonction du genre de l'illustre.
- Une route "domaine" qui permet l'affichage des maisons en fonction du domaine dans lequel la personne s'est illustrée ('Littérature et idées', 'Sciences et industrie', 'Arts et architecture', 'Histoire et politique', 'Musique, théâtre et cinéma').
- Une route "request" qui offre un formulaire permettant d'appliquer plusieurs filtre. 
- route "graphique" qui affiche deux ou trois visualisations (choisir les plus réussies).

# 5. 2-3 étapes pour le développement, et la charge estimée (en heures ou en personne) pour les gros blocs de développement

- production d'une maquette (pour le 5 février : Pauline resp / Kutay Clara et Maddalena consultées)
- Structure (squelette) de l'application, relier la base de données (6 heures) : Clara + Kutay consultable
- Modèle de données : Clara 
- Construction des routes (20 heures) : Kutay + Clara (en parallèle de la construction des templates)
- Construction des templates (20 heures) : Clara + Pauline (en parallèle de la construction des routes)
- Construction des statics et les inclure dans les templates (6 heures): Clara + Pauline + Maddalena
- Débogage et test (10 heures) : Kutay + Clara, ~10 mars
- optimisation (10 heuers) : Kutay et Pauline 
- rédaction de la documentation et organisation du dépôt Github (10 heures) : Clara et Maddalena

