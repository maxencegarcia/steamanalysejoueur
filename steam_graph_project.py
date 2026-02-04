import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.algorithms import bipartite


JEUX_CIBLES = [
    'Counter-Strike', 'Dota 2', 
    'Team Fortress 2', 'Left 4 Dead 2', 'Portal 2',
    'Garry\'s Mod', 'Sid Meier\'s Civilization V', 'Half-Life 2',
    'Borderlands 2', 'Warframe', 'Fallout 4',
    'Grand Theft Auto V', 'PAYDAY 2', 'Unturned', 'Terraria',
    'The Elder Scrolls V Skyrim'
]

try:
    df = pd.read_csv('steam_data.csv', header=None).iloc[:, [0, 1]]
    df.columns = ['user_id', 'game_name']
    df_filtered = df[df['game_name'].isin(JEUX_CIBLES)].drop_duplicates()
    
    # Joueurs avec au moins 2 jeux
    user_counts = df_filtered['user_id'].value_counts()
    active_users = user_counts[user_counts >= 2].index
    df_filtered = df_filtered[df_filtered['user_id'].isin(active_users)]

    # Échantillon (ajusté à 15 pour la clarté)
    sample_users = df_filtered['user_id'].unique()[:15]
    df_sample = df_filtered[df_filtered['user_id'].isin(sample_users)].copy()
    df_sample['user_id'] = df_sample['user_id'].astype(str)
except Exception as e:
    print(f"Erreur : {e}")
    exit()


G = nx.Graph()
joueurs = list(df_sample['user_id'].unique())
jeux = list(df_sample['game_name'].unique())

G.add_nodes_from(joueurs, bipartite=0)
G.add_nodes_from(jeux, bipartite=1)
G.add_edges_from(zip(df_sample['user_id'], df_sample['game_name']))


# 1. Couleurs des joueurs (Palette vive)
colors_joueurs = plt.cm.Set1(np.linspace(0, 1, len(joueurs)))
color_map_joueurs = dict(zip(joueurs, colors_joueurs))

# 2. Couleurs des jeux (Palette nuancée)
colors_jeux = plt.cm.viridis(np.linspace(0.2, 0.8, len(jeux)))

# 3. Taille des jeux (Proportionnalité des relations)
game_sizes = []
for jeu in jeux:
    ses_joueurs = list(G.neighbors(jeu))
    score_partage = sum(G.degree(j) - 1 for j in ses_joueurs) 
    game_sizes.append(150 + (score_partage * 70)) 

fig, ax = plt.subplots(figsize=(12, 12), facecolor='whitesmoke')

pos = {}
for i, jeu in enumerate(jeux):
    angle = 2 * np.pi * i / len(jeux)
    pos[jeu] = np.array([3.5 * np.cos(angle), 3.5 * np.sin(angle)])

for i, joueur in enumerate(joueurs):
    angle = 2 * np.pi * i / len(joueurs)
    pos[joueur] = np.array([8 * np.cos(angle), 8 * np.sin(angle)])

# Dessin des arêtes
for u, v in G.edges():
    user_node = u if u in joueurs else v
    plt.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], 
             color=color_map_joueurs[user_node], alpha=0.6, lw=1.2)

# Dessin des nœuds JEUX
for i, jeu in enumerate(jeux):
    nx.draw_networkx_nodes(G, pos, nodelist=[jeu], 
                           node_color=[colors_jeux[i]], 
                           node_size=game_sizes[i], 
                           node_shape='s', edgecolors='#555555', linewidths=0.5)

# Dessin des nœuds JOUEURS
for joueur in joueurs:
    nx.draw_networkx_nodes(G, pos, nodelist=[joueur], 
                           node_color=[color_map_joueurs[joueur]], 
                           node_size=250)

# Labels (Noms des jeux en noir, IDs joueurs en gris)
for n in G.nodes():
    x, y = pos[n]
    if n in jeux:
        plt.text(x*1.15, y*1.15, s=n, fontsize=9, fontweight='bold', 
                 color='black', ha='center', va='center', rotation=0)
    else:
        plt.text(x*1.1, y*1.1, s=f"ID:{n[-4:]}", fontsize=7, 
                 color='#666666', ha='center', va='center')

plt.axis('off')
plt.tight_layout()
plt.show()