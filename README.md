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
