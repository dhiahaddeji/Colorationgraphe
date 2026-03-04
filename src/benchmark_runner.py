import time
import os
import pandas as pd
import sys

sys.setrecursionlimit(1000000)

from src.loaders.dimacs_loader import load_dimacs
from src.metrics import conflict_count, colors_used, gap_to_opt

from src.algorithms.exact_backtracking import exact_coloring_backtracking
from src.algorithms.aco import aco_coloring
from src.algorithms.simulated_annealing import simulated_annealing
from src.algorithms.tabu_search import tabu_search
from src.algorithms.genetic import genetic_algorithm


OPTIMUM = {
    "myciel3": 4,
    "le450_15a": 15,
    "flat300_28_0": 28,
    "DSJC1000.1": None
}


def _name_from_path(p: str) -> str:
    base = os.path.basename(p)
    return base.replace(".col", "")


def run_benchmark():

    instances = [
        "data/small/myciel3.col",
        "data/medium/le450_15a.col",
        "data/large/DSJC1000.1.col",
    ]

    rows = []

    for path in instances:

        name = _name_from_path(path)
        print("\n===== INSTANCE :", name, "=====")

        G = load_dimacs(path)

        n = G.number_of_nodes()
        m = G.number_of_edges()

        degrees = dict(G.degree())
        max_colors = max(degrees.values()) + 1 if degrees else 1

        opt = OPTIMUM.get(name)

        # même time limit pour toutes les tailles
        exact_time_limit = 20

        algos = [
            ("Exact", lambda: exact_coloring_backtracking(G, time_limit_s=exact_time_limit)),
            ("ACO", lambda: aco_coloring(G, max_colors=max_colors)),
            ("SA", lambda: simulated_annealing(G, max_colors=max_colors)),
            ("Tabu", lambda: tabu_search(G, max_colors=max_colors)),
            ("GA", lambda: genetic_algorithm(G, max_colors=max_colors)),
        ]

        for algo, fn in algos:

            try:

                t0 = time.perf_counter()
                col = fn()
                t1 = time.perf_counter()

                runtime = t1 - t0

                conflicts = conflict_count(G, col)
                valid = conflicts == 0
                k = colors_used(col)
                gap = gap_to_opt(k, opt)

            except Exception as e:

                runtime = None
                conflicts = None
                valid = False
                k = None
                gap = None
                print("ERROR:", algo, e)

            rows.append({
                "instance": name,
                "n_nodes": n,
                "n_edges": m,
                "optimum": opt,
                "algo": algo,
                "time_s": runtime,
                "valid": valid,
                "colors": k,
                "gap": gap,
                "conflicts": conflicts
            })

            print(f"{name:15} | {algo:5} | time={runtime:.3f}s | valid={valid} | colors={k} | gap={gap}")

    df = pd.DataFrame(rows)

    os.makedirs("results", exist_ok=True)

    df.to_csv("results/runs_final.csv", index=False)

    return df