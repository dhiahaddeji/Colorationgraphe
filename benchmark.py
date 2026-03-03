from src.benchmark_runner import run_benchmark
from src.plot_results import plot_all

if __name__ == "__main__":
    df = run_benchmark()
    plot_all(df)
    print("\n✅ Done. Results in results/runs.csv and results/plots/")