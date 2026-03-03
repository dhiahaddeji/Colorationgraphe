import random
import networkx as nx

def conflict_count(G: nx.Graph, col: dict) -> int:
    # un seul scan des arêtes
    return sum(1 for u, v in G.edges() if col[u] == col[v])

def fitness(G: nx.Graph, col: dict) -> int:
    # plus grand = meilleur (moins de conflits)
    return -conflict_count(G, col)

def genetic_algorithm(G: nx.Graph, max_colors: int, pop=40, gens=200, mut=0.02, elite_frac=0.2):
    nodes = list(G.nodes())
    if not nodes:
        return {}

    def rnd():
        return {v: random.randrange(max_colors) for v in nodes}

    def cross(a, b):
        cut = random.randint(1, len(nodes) - 2)
        child = {}
        for i, v in enumerate(nodes):
            child[v] = a[v] if i < cut else b[v]
        return child

    def mutate(ind):
        for v in nodes:
            if random.random() < mut:
                ind[v] = random.randrange(max_colors)

    population = [rnd() for _ in range(pop)]
    best = population[0]
    best_fit = fitness(G, best)

    elite_n = max(2, int(pop * elite_frac))

    for _ in range(gens):
        # calcule fitness UNE SEULE FOIS pour chaque individu
        fits = [(fitness(G, ind), ind) for ind in population]
        fits.sort(key=lambda x: x[0], reverse=True)  # tri sur fitness déjà calculée

        # update best
        if fits[0][0] > best_fit:
            best_fit = fits[0][0]
            best = fits[0][1]

        elite = [ind for _, ind in fits[:elite_n]]

        # nouvelle génération
        new_pop = elite[:]
        while len(new_pop) < pop:
            p1, p2 = random.sample(elite, 2)
            child = cross(p1, p2)
            mutate(child)
            new_pop.append(child)

        population = new_pop

    return best