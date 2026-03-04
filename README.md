# Coloration de Graphe — Benchmark des algorithmes

Ce projet implémente et compare différents algorithmes pour le **problème de coloration de graphe**, avec des benchmarks sur des instances standards (DIMACS).

## 📁 Structure du projet
Colorationgraphe/
├── data/ # Instances de graphes DIMACS
├── src/ # Code source (loaders, algorithmes, métriques)
├── results/ # Résultats et plots générés
├── benchmark.py # Script principal de benchmark
├── plot_results.py # Script de création des graphiques
├── README.md # Documentation du projet
├── .gitignore


## 🧪 Algorithmes comparés

| Abréviation | Algorithme |
|-------------|------------|
| Exact       | Recherche exhaustive / backtracking |
| ACO         | Ant Colony Optimization |
| SA          | Recuit simulé |
| Tabu        | Tabu Search |
| GA          | Algorithme génétique |

## 📊 Instances testées

| Catégorie | Instance | Sommets | Arêtes |
|-----------|----------|---------|--------|
| small     | myciel3 | 11 | 20 |
| medium    | le450_15a | 450 | ~8000 |
| large     | DSJC1000.1 | 1000 | ~62000 |

Les fichiers sont stockés dans `data/{small,medium,large}`.

## ▶️ Comment lancer le benchmark

Assurez-vous d’être dans le dossier du projet, puis :

```bash
python benchmark.py
