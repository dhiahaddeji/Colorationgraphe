import time
import networkx as nx

def exact_coloring_backtracking(G: nx.Graph, time_limit_s: float = 10.0):
    nodes = list(G.nodes())
    nodes.sort(key=lambda x: G.degree(x), reverse=True)

    coloring = {}
    best = {"colors": float("inf"), "coloring": None}
    start = time.perf_counter()

    def can_color(v, c):
        for u in G.neighbors(v):
            if coloring.get(u) == c:
                return False
        return True

    def backtrack(i, used_colors):
        if time.perf_counter() - start > time_limit_s:
            return

        if i == len(nodes):
            if used_colors < best["colors"]:
                best["colors"] = used_colors
                best["coloring"] = dict(coloring)
            return

        if used_colors >= best["colors"]:
            return

        v = nodes[i]
        for c in range(used_colors):
            if can_color(v, c):
                coloring[v] = c
                backtrack(i + 1, used_colors)
                del coloring[v]

        # try new color
        if used_colors + 1 < best["colors"]:
            coloring[v] = used_colors
            backtrack(i + 1, used_colors + 1)
            del coloring[v]

    backtrack(0, 0)

    return best["coloring"] if best["coloring"] is not None else {}