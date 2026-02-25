import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.algorithms import bipartite

JEUX_CIBLES = [
    'Counter-Strike', 'Dota 2', 'Team Fortress 2', 'Left 4 Dead 2', 'Portal 2',
    'Garry\'s Mod', 'Sid Meier\'s Civilization V', 'Half-Life 2',
    'Borderlands 2', 'Warframe', 'Fallout 4',
    'Grand Theft Auto V', 'PAYDAY 2', 'Unturned', 'Terraria',
    'The Elder Scrolls V Skyrim'
]

try:
    df = pd.read_csv('steam_data.csv', header=None).iloc[:, [0, 1]]
    df.columns = ['user_id', 'game_name']
    df_filtered = df[df['game_name'].isin(JEUX_CIBLES)].drop_duplicates()
    
    user_counts = df_filtered['user_id'].value_counts()
    active_users = user_counts[user_counts >= 2].index
    df_filtered = df_filtered[df_filtered['user_id'].isin(active_users)]

    sample_users = df_filtered['user_id'].unique()[:15]
    df_sample = df_filtered[df_filtered['user_id'].isin(sample_users)].copy()
    df_sample['user_id'] = df_sample['user_id'].astype(str)
except Exception as e:
    print(f"Erreur lors de la lecture des données : {e}")
    exit()

G = nx.Graph()
joueurs = list(df_sample['user_id'].unique())
jeux = list(df_sample['game_name'].unique())

G.add_nodes_from(joueurs, bipartite=0)
G.add_nodes_from(jeux, bipartite=1)
G.add_edges_from(zip(df_sample['user_id'], df_sample['game_name']))

G_proj_jeux = bipartite.weighted_projected_graph(G, jeux)
G_proj_joueurs = bipartite.weighted_projected_graph(G, joueurs)

def afficher_toutes_recommandations(G_bipartite, proj_jeux, proj_joueurs):
    print("\n" + "╔" + "═"*50 + "╗")
    print("║   ANALYSE DES JEUX       ║")
    print("╚" + "═"*50 + "╝")
    
    for jeu in sorted(list(proj_jeux.nodes())):
        voisins = proj_jeux[jeu]
        
        # Ident des catégories
        recos_fortes = [v for v, data in voisins.items() if data['weight'] >= 2]
        # Hors-piste
        hors_piste_faible = [v for v, data in voisins.items() if data['weight'] < 2]
        
        print(f"\n Analyse pour : [{jeu}]")
        a_affiche_quelque_chose = False

        # Recommandations solides
        if recos_fortes:
            recos_fortes_sorted = sorted(recos_fortes, key=lambda x: voisins[x]['weight'], reverse=True)[:2]
            rec_str = ", ".join([f"{name} ({voisins[name]['weight']} communs)" for name in recos_fortes_sorted])
            print(f"  Recommandé : {rec_str}")
            a_affiche_quelque_chose = True
        
        # Hors-Piste
        if hors_piste_faible:
            hp_sorted = sorted(hors_piste_faible, key=lambda x: voisins[x]['weight'])[:2]
            hp_str = ", ".join([f"{name} ({voisins[name]['weight']} commun)" for name in hp_sorted])
            
            if not recos_fortes:
                print(f"  Aucune recommandation forte trouvée. Note : [{hp_str}] est considéré Hors-Piste.")
            else:
                print(f"  Hors-Piste détecté : [{hp_str}]")
            a_affiche_quelque_chose = True

        #  Cas "Rien du tout"
        if not a_affiche_quelque_chose:
            print("  Rien à recommander, mais rien de hors-piste non plus.")

    print("\n" + "╔" + "═"*50 + "╗")
    print("║             RECOMMANDATIONS D'AMIS              ║")
    print("╚" + "═"*50 + "╝")
    
    for joueur in sorted(list(proj_joueurs.nodes())):
        amis_potentiels = proj_joueurs[joueur]
        affinites = [a for a, data in amis_potentiels.items() if data['weight'] >= 2]
        divergences = [a for a, data in amis_potentiels.items() if data['weight'] < 2]

        print(f" Joueur [{joueur}] :")
        
        if affinites:
            meilleur_ami = sorted(affinites, key=lambda x: amis_potentiels[x]['weight'], reverse=True)[0]
            print(f" Affinité : S'entendrait bien avec [{meilleur_ami}] ({amis_potentiels[meilleur_ami]['weight']} jeux communs).")
        else:
            print(" Aucune affinité forte détectée")
            
        if divergences:
            plus_atypique = sorted(divergences, key=lambda x: amis_potentiels[x]['weight'])[0]
            print(f" Divergence : Goûts différents de [{plus_atypique}] ({amis_potentiels[plus_atypique]['weight']} jeu commun).")
            
        print("-" * 15)

    print("\n" + "╔" + "═"*50 + "╗")
    print("║            --- ANALYSE DE NICHE ---             ║")
    print("╚" + "═"*50 + "╝")
    
    niche_jeux = [n for n in jeux if G_bipartite.degree(n) == 1]
    if niche_jeux:
        print("Les jeux suivants sont peu populaires dans cet échantillon (1 seul joueur) :")
        for j in niche_jeux: print(f" {j}")
    else:
        print("Aucun jeu de niche détecté.")

colors_joueurs = plt.cm.Set1(np.linspace(0, 1, len(joueurs)))
color_map_joueurs = dict(zip(joueurs, colors_joueurs))
colors_jeux = plt.cm.viridis(np.linspace(0.2, 0.8, len(jeux)))

game_sizes = []
for jeu in jeux:
    ses_joueurs = list(G.neighbors(jeu))
    score_partage = sum(G.degree(j) - 1 for j in ses_joueurs) 
    game_sizes.append(150 + (score_partage * 70)) 

fig, ax = plt.subplots(figsize=(10, 10), facecolor='whitesmoke')
pos = {}
for i, jeu in enumerate(jeux):
    angle = 2 * np.pi * i / len(jeux)
    pos[jeu] = np.array([3.5 * np.cos(angle), 3.5 * np.sin(angle)])
for i, joueur in enumerate(joueurs):
    angle = 2 * np.pi * i / len(joueurs)
    pos[joueur] = np.array([8 * np.cos(angle), 8 * np.sin(angle)])

for u, v in G.edges():
    user_node = u if u in joueurs else v
    plt.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=color_map_joueurs[user_node], alpha=0.4)

for i, jeu in enumerate(jeux):
    nx.draw_networkx_nodes(G, pos, nodelist=[jeu], node_color=[colors_jeux[i]], node_size=game_sizes[i], node_shape='s')

for joueur in joueurs:
    nx.draw_networkx_nodes(G, pos, nodelist=[joueur], node_color=[color_map_joueurs[joueur]], node_size=200)

for n in G.nodes():
    x, y = pos[n]
    plt.text(x*1.1, y*1.1, s=n if n in jeux else f"ID:{n[-3:]}", fontsize=8, ha='center')

plt.title("Graphe Steam : Recommandations et Divergences", fontsize=14)
plt.axis('off')
plt.show()

afficher_toutes_recommandations(G, G_proj_jeux, G_proj_joueurs)
