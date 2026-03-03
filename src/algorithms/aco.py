import random
import networkx as nx
from collections import defaultdict

def aco_coloring(G: nx.Graph, max_colors: int, ants=15, iters=60, rho=0.2):
    nodes = list(G.nodes())
    pher = defaultdict(lambda: [1.0] * max_colors)

    def conflicts(col):
        return sum(1 for u, v in G.edges() if col[u] == col[v])

    best = {v: 0 for v in nodes}
    best_conf = float("inf")

    for _ in range(iters):
        sols = []
        for _a in range(ants):
            col = {}
            for v in nodes:
                probs = pher[v][:]

                # penalize neighbor used colors
                for u in G.neighbors(v):
                    if u in col:
                        probs[col[u]] *= 0.05

                s = sum(probs)
                r = random.random() * s
                acc = 0.0
                chosen = 0
                for c in range(max_colors):
                    acc += probs[c]
                    if acc >= r:
                        chosen = c
                        break
                col[v] = chosen

            conf = conflicts(col)
            sols.append((col, conf))
            if conf < best_conf:
                best, best_conf = dict(col), conf

        # evaporation
        for v in nodes:
            for c in range(max_colors):
                pher[v][c] *= (1 - rho)

        # deposit from best of iteration
        best_iter, conf_iter = min(sols, key=lambda x: x[1])
        dep = 1.0 / (1 + conf_iter)
        for v, c in best_iter.items():
            pher[v][c] += dep

    return best