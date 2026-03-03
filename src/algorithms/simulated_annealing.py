import random, math
import networkx as nx

def simulated_annealing(G: nx.Graph, max_colors: int, iters=25000, t0=1.0, alpha=0.9995):
    nodes = list(G.nodes())
    if not nodes:
        return {}

    # init random coloring
    col = {v: random.randrange(max_colors) for v in nodes}

    # neighbor_colors[v][c] = nb voisins de v avec couleur c
    neighbor_colors = {v: [0] * max_colors for v in nodes}
    for u, v in G.edges():
        cu, cv = col[u], col[v]
        neighbor_colors[u][cv] += 1
        neighbor_colors[v][cu] += 1

    # conflicts per node and total conflicts
    node_conf = {v: neighbor_colors[v][col[v]] for v in nodes}
    total_conf = sum(node_conf.values()) // 2

    best = dict(col)
    best_conf = total_conf

    T = t0

    def apply_move(v, new_c):
        """Applique v: old->new avec update O(deg(v))"""
        nonlocal total_conf
        old_c = col[v]
        if old_c == new_c:
            return

        old_conf_v = neighbor_colors[v][old_c]
        new_conf_v = neighbor_colors[v][new_c]

        # update total conflicts due to v change
        total_conf += (new_conf_v - old_conf_v)
        node_conf[v] = new_conf_v

        # update neighbors stats
        for u in G.neighbors(v):
            cu = col[u]
            neighbor_colors[u][old_c] -= 1
            neighbor_colors[u][new_c] += 1

            if cu == old_c:
                node_conf[u] -= 1
            if cu == new_c:
                node_conf[u] += 1

        col[v] = new_c

    for _ in range(iters):
        v = random.choice(nodes)
        old_c = col[v]
        new_c = random.randrange(max_colors)
        if new_c == old_c:
            continue

        # delta conflicts if we move v -> new_c
        old_conf_v = neighbor_colors[v][old_c]
        new_conf_v = neighbor_colors[v][new_c]
        delta = new_conf_v - old_conf_v

        new_total = total_conf + delta

        # accept rule (minimize conflicts)
        if new_total <= total_conf or random.random() < math.exp(-(new_total - total_conf) / max(T, 1e-9)):
            apply_move(v, new_c)
            if total_conf < best_conf:
                best = dict(col)
                best_conf = total_conf

        T *= alpha

    return best