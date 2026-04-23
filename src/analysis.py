import os
import pandas as pd
import numpy as np
from scipy import stats

RESULTS_FILE = os.path.join(os.path.dirname(__file__), "..", "results", "results.csv")


def analyse():
    df = pd.read_csv(RESULTS_FILE)

    print("=" * 70)
    print("STATISTICAL ANALYSIS: Bracket Fairness Optimisation")
    print("=" * 70)

    for n in sorted(df["participants"].unique()):
        subset = df[df["participants"] == n]
        baseline = subset["baseline_score"].iloc[0]
        rs_scores = subset["rs_score"].values
        ga_scores = subset["ga_score"].values

        print(f"\n--- {n} participants | Baseline: {baseline} ---")

        # Mean and median
        print(f"  {'':20} {'Mean':>8} {'Median':>8} {'Min':>8} {'Max':>8}")
        print(
            f"  {'Random Search':20} {np.mean(rs_scores):>8.2f} {np.median(rs_scores):>8.2f} {np.min(rs_scores):>8} {np.max(rs_scores):>8}"
        )
        print(
            f"  {'Genetic Algorithm':20} {np.mean(ga_scores):>8.2f} {np.median(ga_scores):>8.2f} {np.min(ga_scores):>8} {np.max(ga_scores):>8}"
        )

        # Win/draw/loss (GA vs RS)
        wins = sum(ga < rs for ga, rs in zip(ga_scores, rs_scores))
        draws = sum(ga == rs for ga, rs in zip(ga_scores, rs_scores))
        losses = sum(ga > rs for ga, rs in zip(ga_scores, rs_scores))
        print(f"\n  GA vs RS — Win: {wins} | Draw: {draws} | Loss: {losses}")

        # Wilcoxon signed-rank test (GA vs RS)
        differences = rs_scores - ga_scores
        if np.all(differences == 0):
            print(f"  Wilcoxon RS vs GA: N/A (no difference)")
        else:
            stat, p = stats.wilcoxon(rs_scores, ga_scores)
            sig = "✓ significant" if p < 0.05 else "✗ not significant"
            print(f"  Wilcoxon RS vs GA: p={p:.4f} ({sig})")

        # Wilcoxon signed-rank test (RS vs baseline)
        rs_vs_baseline = [baseline] * len(rs_scores)
        if len(set(rs_scores)) == 1 and rs_scores[0] == baseline:
            print(f"  Wilcoxon RS vs Baseline: N/A (no difference)")
        else:
            stat, p = stats.wilcoxon(rs_vs_baseline, rs_scores)
            sig = "✓ significant" if p < 0.05 else "✗ not significant"
            print(f"  Wilcoxon RS vs Baseline: p={p:.4f} ({sig})")

        # Wilcoxon signed-rank test (GA vs baseline)
        ga_vs_baseline = [baseline] * len(ga_scores)
        if len(set(ga_scores)) == 1 and ga_scores[0] == baseline:
            print(f"  Wilcoxon GA vs Baseline: N/A (no difference)")
        else:
            stat, p = stats.wilcoxon(ga_vs_baseline, ga_scores)
            sig = "✓ significant" if p < 0.05 else "✗ not significant"
            print(f"  Wilcoxon GA vs Baseline: p={p:.4f} ({sig})")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    analyse()
