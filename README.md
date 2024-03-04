# Projet de groupe M2 TNAH 2023/2024 : Maisons des Illustres

## 1. Description générale de l’application

Le label "Maison des Illustres" est décerné en France à des maisons, châteaux ou ateliers ayant appartenu à des personnalités éminentes qui ont marqué l'histoire par leurs réalisations dans les domaines de la politique, de la culture, des sciences ou des arts. Ces lieux doivent alors proposer des visites *a minima* 40 jours dans l'année, mettant en avant leur valeur patrimoniale et l'influence de "l'illustre personne" dans l'Histoire. L’attribution d’un tel label représente une reconnaissance officielle de l’intérêt patrimonial de la Maison. Le label est également un dispositif de valorisation, qui s’accompagne d’avantages divers, en termes de visibilité notamment. De son attribution découle donc des enjeux de représentation et la mise en valeur d'une large diversité de personnes et de lieux avec un intérêt patrimonial. Est-ce vraiment le cas ? 

Le but de cette application est de permettre un suivi de la diversité des lieux labellisés et des personnes qu'elles représentent, ainsi qu'un outil de localisation de ces bâtiments, participant ainsi à leur visibilité.

## 2. Contributeurs

Maddalena ACCARDO

Pauline CHARRIER

Clara GROMETTO

Kutay SEFIL

## 3. Mode d'emploi de l'application 

Pour une première utilisation sur Ubuntu, veuillez suivre pas à pas les instructions suivantes :

1. Télécharger la base de données disponible dans ce répertoire GitHub. 

2. Cloner le dépôt GitHub de l'application avec la commande suivante : 
```bash
git clone https://github.com/gromettoclara/maisons_illustres.git
```
   
3.  Installer Python :
```bash
sudo apt-get install python3
```

4. Installer Pip :
 ```bash
sudo apt install python3-pip
```

5. Créer un fichier .env dans le dossier "appli" avec les variables ci-dessous en complétant avec le chemin absolu de la base de données : 
```Python
DEBUG=True
SQLALCHEMY_DATABASE_URI=
SQLALCHEMY_ECHO=False
WTF_CSRF_ENABLE=True
```

6. Installer le package "virtualenv" avec la commande suivante :
```bash
pip install virtualenv
```

7. Installer un environnement virtuel dans le dossier "appli" :
```bash
virtualenv env -p python3
```

8. Activer l'environnement virtuel avec la commande : 
```bash
source env/bin/activate
```

9. Installer les dépendances requises : 
```bash
pip install -r requirements.txt
```

10. Lancer l'application :
```bash
python run.py
```

Pour une utilisation ultérieure de l'application, il suffit de répéter les étapes 8 et 10 uniquement.

## 4. Fonctionnalités de l'application

La page d'accueil affiche un catalogue de toutes les maisons d'illustres organisées par ordre alphabétique sur 25 pages ainsi qu'un formulaire qui permet d'effectuer une recherche en fonction de plusieurs filtres (nom de la maison, genre de l'illustre, labels...). 
Ce formulaire est aussi accessible depuis l'onglet "Recherche" situé dans la barre de navigation supérieure.

*Screenshot page d'accueil*

Pour chaque maison, le catalogue propose un bouton "Supprimer" et un bouton "Éditer" qui permettent respectivement de supprimer la maison ou de mettre à jour les différentes informations relatives à la maison.

*Screenshot update maison*

Le menu défilant situé au niveau de la barre de navigation donne accès à un catalogue des personnes illustres qui est donc différent de celui des maisons, ainsi qu'à 2 options qui permettent d'ajouter au choix une nouvelle maison ou une nouvelle personne à la base de données.

*Screenshot catalogue personnes avec le menu défilant*

Ensuite, l'onglet "Carte" affiche une carte avec l'emplacement de toutes les maisons d'illustres avec la présence de plusieurs filtres là aussi.

*Screenshot carte*

L'onglet "graphiques" permet quant à lui d'afficher les différentes visualisations graphiques réalisées à partir des données.

*Screenshot d'un graphique*

Enfin, la barre de recherche située à droite nous donne la possibilité d'effectuer une recherche rapide en plein texte sur l'ensemble des maisons.



