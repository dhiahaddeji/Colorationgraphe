import networkx as nx

def conflict_count(G: nx.Graph, coloring: dict) -> int:
    """Nombre d'arêtes en conflit (u,v) avec même couleur."""
    return sum(
        1 for u, v in G.edges()
        if coloring.get(u) is not None
        and coloring.get(v) is not None
        and coloring[u] == coloring[v]
    )

def is_valid_coloring(G: nx.Graph, coloring: dict) -> bool:
    return conflict_count(G, coloring) == 0

def colors_used(coloring: dict) -> int:
    """Nombre de couleurs distinctes utilisées."""
    if not coloring:
        return 0
    return len(set(coloring.values()))

def gap_to_opt(sol_colors: int, optimum: int | None):
    """Gap à l’optimal (si optimum connu)."""
    return None if optimum is None else sol_colors - optimum