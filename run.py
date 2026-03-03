from src.loaders.dimacs_loader import load_dimacs

G = load_dimacs("data/medium/flat300_28_0.col")

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())