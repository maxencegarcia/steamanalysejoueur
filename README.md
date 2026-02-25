# Projet Graphe Steam relations Joueurs, Jeux
DUCRET Elouhan
GARCIA Maxence

projet de creation d'un graphe reliant les joueur entre eux en fonctions d'un jeux commun

# Prérequis

# Bibliothèques Python
Installer les dépendances :
    pandas networkx matplotlib

#Dataset Kaggle

Dataset recommandé : Steam Video Games
Lien : https://www.kaggle.com/datasets/tamber/steam-video-games
Fichier : steam-200k.csv

Instructions de téléchargement :
1) Créer un compte Kaggle
2) Télécharger le fichier CSV
3) Renommer le fichier en steam_data.csv
4) Placer le fichier dans le même dossier que steam_graph_project.py

# Fonctionnalitées du script

### 1. Visualisation du Graphe
* Type : Graphe biparti circulaire.
* Nœuds : Joueurs (cercles extérieurs) et Jeux (carrés intérieurs).
* Arêtes : Un lien est créé si un joueur possède un jeu de la liste cible.
* Dynamique : La taille des nœuds "Jeux" est proportionnelle au score de partage entre les joueurs.

### 2. Moteur d'Analyse (Console)
Le script génère désormais trois types d'analyses avancées :
* Recommandations de jeux : Identifie les proximités fortes (poids >= 2) et les suggestions "hors-piste" (poids faible) basées sur les projections du graphe.
* Affinités sociales : Recherche les joueurs ayant les plus fortes similarités de bibliothèque (minimum 2 jeux communs).
* Analyse de niche : Identification des jeux possédés par un seul utilisateur dans l'échantillon.

# Résultat attendu
Le script va charger les données, filtrer uniquement sur 16 jeux spécifiques (CS, Dota 2, Skyrim...), ne garder que les joueurs possédant au moins 2 de ces jeux, et générer un graphe biparti circulaire.

# Structure du graphe

# Type de graphe
Graphe biparti circulaire avec deux types de nœuds :
Joueurs (cercle sur la partie exterieur)
Jeux (carre sur la partie interieur)

# Arêtes
Une arête relie un joueur à un jeu s'il y a joué et si un autre joueur y a jouer aussi.


## Fichiers du projet

projet-steam/
│
|--- steam_graph_project.py    # Script principal
|--- steam_data.csv             # Données Kaggle (à télécharger)
|--- steam_graph.png            # Graphe généré
|--- README.md                  # Ce fichier

# Statistiques affichées

Détails techniques de l'affichage
Le script effectue les réglages suivants :
Filtrage : Seuls les joueurs avec >=2 jeux de la liste sont conservés.
Échantillon : Pour la lisibilité, le graphe n'affiche que les 15 premiers joueurs trouvés.
Taille des nœuds : La taille des carrés (jeux) varie selon le "score de partage" (nombre de connexions des joueurs qui y jouent).
Labels : Affiche le nom complet des jeux, mais seulement les 4 derniers chiffres des ID joueurs pour ne pas surcharger.


# Améliorations possibles

Pour aller plus loin (hors projet de base) :
- Utiliser le fichier complet avec les heures de jeu
- Calculer des métriques (centralité, communautés)
- Graphe interactif avec Plotly

# Ressources

- NetworkX : https://networkx.org/documentation/stable/
- Pandas : https://pandas.pydata.org/docs/
- Matplotlib : https://matplotlib.org/stable/
