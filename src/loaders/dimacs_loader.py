import networkx as nx

def load_dimacs(path):
    G = nx.Graph()

    with open(path, "r", encoding="latin1") as f:
        for line in f:
            line = line.strip()

            # ignorer commentaires
            if not line or line.startswith("c"):
                continue

            parts = line.split()

            # lignes arêtes : e u v
            if len(parts) >= 3 and parts[0] == "e":
                u = int(parts[1])
                v = int(parts[2])
                G.add_edge(u, v)

    return G