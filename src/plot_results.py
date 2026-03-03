import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

def plot_all(df: pd.DataFrame):
    out = Path("results/plots")
    out.mkdir(parents=True, exist_ok=True)

    # ordre par taille
    order = df.groupby("instance")["n_nodes"].max().sort_values().index.tolist()

    # ---------- Graphe 1 : Temps vs taille ----------
    plt.figure()
    for algo in df["algo"].unique():
        sub = df[df["algo"] == algo].set_index("instance").reindex(order)
        plt.plot(sub["n_nodes"], sub["time_s"], marker="o", label=algo)
    plt.xlabel("|V| (nombre de sommets)")
    plt.ylabel("Temps d'exécution (s)")
    plt.title("Benchmark — Temps vs taille du graphe")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "time_vs_size.png")
    plt.close()

    # ---------- Graphe 2 : Qualité (nb couleurs) vs taille ----------
    # On trace toutes les solutions, valides ou non (c’est utile),
    # et on met en plus une version "valid only" si tu veux.
    plt.figure()
    for algo in df["algo"].unique():
        sub = df[df["algo"] == algo].set_index("instance").reindex(order)
        plt.plot(sub["n_nodes"], sub["colors"], marker="o", label=algo)
    plt.xlabel("|V| (nombre de sommets)")
    plt.ylabel("Nombre de couleurs utilisées")
    plt.title("Benchmark — Qualité (nb couleurs) vs taille")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "colors_vs_size.png")
    plt.close()

    # ---------- Graphe 3 : Conflits vs taille ----------
    plt.figure()
    for algo in df["algo"].unique():
        sub = df[df["algo"] == algo].set_index("instance").reindex(order)
        plt.plot(sub["n_nodes"], sub["conflicts"], marker="o", label=algo)
    plt.xlabel("|V| (nombre de sommets)")
    plt.ylabel("Nombre de conflits (arêtes en conflit)")
    plt.title("Benchmark — Faisabilité (conflits) vs taille")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "conflicts_vs_size.png")
    plt.close()

    # ---------- BONUS (optionnel) : Gap si optimum connu ----------
    gap_df = df[df["gap"].notna()]
    if len(gap_df) > 0:
        plt.figure()
        for algo in gap_df["algo"].unique():
            sub = gap_df[gap_df["algo"] == algo].set_index("instance").reindex(order)
            plt.plot(sub["n_nodes"], sub["gap"], marker="o", label=algo)
        plt.xlabel("|V| (nombre de sommets)")
        plt.ylabel("Gap (couleurs - optimum)")
        plt.title("Benchmark — Écart à l’optimal vs taille")
        plt.legend()
        plt.tight_layout()
        plt.savefig(out / "gap_vs_size.png")
        plt.close()