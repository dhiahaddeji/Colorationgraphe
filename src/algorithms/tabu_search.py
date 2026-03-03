import random
import networkx as nx
from collections import deque, defaultdict

def tabu_search(G: nx.Graph, max_colors: int, iters=20000, tenure=80, sample_moves=40):
    """
    Tabu Search multi-objectif RAPIDE :
    - objectif = conflicts*1000 + colors_used
    - explore un petit voisinage (sample_moves) à chaque itération
    - évalue les mouvements par DELTA local (pas de scan complet des arêtes)
    """
    nodes = list(G.nodes())
    if not nodes:
        return {}

    # init random coloring
    col = {v: random.randrange(max_colors) for v in nodes}

    # --- helper structures ---
    # neighbor_colors[v][c] = combien de voisins de v ont la couleur c
    neighbor_colors = {v: [0] * max_colors for v in nodes}
    for u, v in G.edges():
        cu, cv = col[u], col[v]
        neighbor_colors[u][cv] += 1
        neighbor_colors[v][cu] += 1

    # conflicts per node = nb voisins avec même couleur
    node_conf = {v: neighbor_colors[v][col[v]] for v in nodes}
    total_conf = sum(node_conf.values()) // 2  # chaque conflit compté 2 fois

    # colors usage count
    color_count = [0] * max_colors
    for v in nodes:
        color_count[col[v]] += 1
    used_colors = sum(1 for c in color_count if c > 0)

    def score(total_conflicts, used_c):
        return total_conflicts * 1000 + used_c

    best_col = dict(col)
    best_score = score(total_conf, used_colors)

    tabu = deque(maxlen=tenure)

    def apply_move(v, new_c):
        """Applique v: old_c -> new_c en mettant à jour toutes les structures en O(deg(v))."""
        nonlocal total_conf, used_colors

        old_c = col[v]
        if old_c == new_c:
            return

        # --- update global used_colors (via counts) ---
        color_count[old_c] -= 1
        if color_count[old_c] == 0:
            used_colors -= 1

        if color_count[new_c] == 0:
            used_colors += 1
        color_count[new_c] += 1

        # --- update conflicts ---
        # conflits impliquant v changent de:
        # old_conf_v = nb voisins couleur old_c
        # new_conf_v = nb voisins couleur new_c
        old_conf_v = neighbor_colors[v][old_c]
        new_conf_v = neighbor_colors[v][new_c]

        # total_conf: on retire les anciens conflits de v et on ajoute les nouveaux
        total_conf += (new_conf_v - old_conf_v)

        # mettre à jour node_conf[v] après changement
        node_conf[v] = new_conf_v

        # Pour chaque voisin u de v :
        # u voit la couleur de v changer, donc neighbor_colors[u][old_c]-- et [new_c]++
        # et si u avait la même couleur que v avant/après, son node_conf change aussi
        for u in G.neighbors(v):
            cu = col[u]

            # u perd un voisin de couleur old_c
            neighbor_colors[u][old_c] -= 1
            # u gagne un voisin de couleur new_c
            neighbor_colors[u][new_c] += 1

            # update node_conf[u] si la couleur de u est impactée
            # si cu == old_c : u avait un conflit avec v avant -> -1
            if cu == old_c:
                node_conf[u] -= 1
            # si cu == new_c : u a un conflit avec v après -> +1
            if cu == new_c:
                node_conf[u] += 1

        # enfin, changer la couleur de v
        col[v] = new_c

    for _ in range(iters):
        # choisir un ensemble de sommets à explorer :
        # prioriser les sommets en conflit
        conflicted = [v for v in nodes if node_conf[v] > 0]
        if conflicted:
            candidates_v = random.sample(conflicted, min(len(conflicted), max(10, sample_moves // 2)))
        else:
            candidates_v = random.sample(nodes, min(len(nodes), max(10, sample_moves // 2)))

        best_move = None
        best_move_score = None

        # explorer quelques mouvements (voisinage échantillonné)
        for _m in range(sample_moves):
            v = random.choice(candidates_v)
            old_c = col[v]
            new_c = random.randrange(max_colors)
            if new_c == old_c:
                continue

            move = (v, new_c)
            if move in tabu:
                continue

            # delta conflicts (local) :
            # old_conf_v = neighbor_colors[v][old_c]
            # new_conf_v = neighbor_colors[v][new_c]
            old_conf_v = neighbor_colors[v][old_c]
            new_conf_v = neighbor_colors[v][new_c]
            delta_conf = new_conf_v - old_conf_v

            # delta used_colors :
            delta_used = 0
            if color_count[old_c] == 1:
                delta_used -= 1
            if color_count[new_c] == 0:
                delta_used += 1

            cand_score = score(total_conf + delta_conf, used_colors + delta_used)

            if best_move_score is None or cand_score < best_move_score:
                best_move_score = cand_score
                best_move = (v, new_c, old_c)

        if best_move is None:
            continue

        v, new_c, old_c = best_move
        apply_move(v, new_c)
        tabu.append((v, old_c))  # interdire retour immédiat

        s = score(total_conf, used_colors)
        if s < best_score:
            best_score = s
            best_col = dict(col)

        # si solution valide et couleurs déjà pas mal, on peut laisser tourner,
        # mais tu peux ajouter un early stop si tu veux.

    return best_col