"""
Visualisation: Bracket Fairness Optimisation Results

Generates figures and summary table for the report:
  1. Box plot  — percentage improvement over baseline per participant count
                 (Random Search vs Genetic Algorithm, 30 runs)
  2. Line plot — mean percentage improvement vs participant count
                 with standard deviation shading

Percentage improvement = (baseline - score) / baseline * 100
Higher improvement = fairer bracket found.

Figures saved to: results/
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

RESULTS_FILE = os.path.join(os.path.dirname(__file__), '..', 'results', 'results.csv')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')


def load_and_compute(df: pd.DataFrame) -> pd.DataFrame:
    # Compute percentage improvement over baseline for RS and GA.
    df['rs_improvement'] = (df['baseline_score'] - df['rs_score']) / df['baseline_score'] * 100
    df['ga_improvement'] = (df['baseline_score'] - df['ga_score']) / df['baseline_score'] * 100
    return df


def plot_boxplot(df: pd.DataFrame):
    # Box plot of percentage improvement over baseline per participant count.
    participant_counts = sorted(df['participants'].unique())
    n_groups = len(participant_counts)

    fig, ax = plt.subplots(figsize=(12, 6))

    # Position groups
    x = np.arange(n_groups)
    width = 0.35

    rs_data = [df[df['participants'] == n]['rs_improvement'].values for n in participant_counts]
    ga_data = [df[df['participants'] == n]['ga_improvement'].values for n in participant_counts]

    bp1 = ax.boxplot(rs_data, positions=x - width/2, widths=width*0.8,
                     patch_artist=True,
                     boxprops=dict(facecolor='#5B9BD5', alpha=0.8),
                     medianprops=dict(color='black', linewidth=2),
                     whiskerprops=dict(linewidth=1.5),
                     capprops=dict(linewidth=1.5),
                     flierprops=dict(marker='o', markersize=4))

    bp2 = ax.boxplot(ga_data, positions=x + width/2, widths=width*0.8,
                     patch_artist=True,
                     boxprops=dict(facecolor='#ED7D31', alpha=0.8),
                     medianprops=dict(color='black', linewidth=2),
                     whiskerprops=dict(linewidth=1.5),
                     capprops=dict(linewidth=1.5),
                     flierprops=dict(marker='o', markersize=4))

    ax.set_xlabel('Number of Participants', fontsize=12)
    ax.set_ylabel('Improvement over Baseline (%)', fontsize=12)
    ax.set_title('Bracket Fairness Improvement over Baseline\n(Random Search vs Genetic Algorithm, 30 runs)', fontsize=13)
    ax.set_xticks(x)
    ax.set_xticklabels(participant_counts)
    ax.legend([bp1['boxes'][0], bp2['boxes'][0]], ['Random Search', 'Genetic Algorithm'],
              loc='upper left', fontsize=11)
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'boxplot_improvement.png')
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def plot_lineplot(df: pd.DataFrame):
    # Line plot of mean percentage improvement vs participant count.
    participant_counts = sorted(df['participants'].unique())

    rs_means = [df[df['participants'] == n]['rs_improvement'].mean() for n in participant_counts]
    ga_means = [df[df['participants'] == n]['ga_improvement'].mean() for n in participant_counts]
    rs_stds  = [df[df['participants'] == n]['rs_improvement'].std() for n in participant_counts]
    ga_stds  = [df[df['participants'] == n]['ga_improvement'].std() for n in participant_counts]

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(participant_counts, rs_means, marker='o', color='#5B9BD5',
            linewidth=2, markersize=7, label='Random Search')
    ax.fill_between(participant_counts,
                    np.array(rs_means) - np.array(rs_stds),
                    np.array(rs_means) + np.array(rs_stds),
                    alpha=0.15, color='#5B9BD5')

    ax.plot(participant_counts, ga_means, marker='s', color='#ED7D31',
            linewidth=2, markersize=7, label='Genetic Algorithm')
    ax.fill_between(participant_counts,
                    np.array(ga_means) - np.array(ga_stds),
                    np.array(ga_means) + np.array(ga_stds),
                    alpha=0.15, color='#ED7D31')

    ax.set_xlabel('Number of Participants', fontsize=12)
    ax.set_ylabel('Mean Improvement over Baseline (%)', fontsize=12)
    ax.set_title('Mean Bracket Fairness Improvement over Baseline\n(Random Search vs Genetic Algorithm)', fontsize=13)
    ax.legend(fontsize=11)
    ax.xaxis.grid(True, linestyle='--', alpha=0.5)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xticks(participant_counts)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'lineplot_improvement.png')
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def print_summary_table(df: pd.DataFrame):
    # Print summary table for report.
    from scipy import stats

    print("\n=== Summary Table ===")
    print(f"{'N':>6} {'Baseline':>10} {'RS Mean':>10} {'GA Mean':>10} {'RS Impr%':>10} {'GA Impr%':>10} {'p-value':>10} {'Sig':>5}")
    print("-" * 75)

    for n in sorted(df['participants'].unique()):
        subset = df[df['participants'] == n]
        baseline = subset['baseline_score'].iloc[0]
        rs_scores = subset['rs_score'].values
        ga_scores = subset['ga_score'].values
        rs_impr = subset['rs_improvement'].mean()
        ga_impr = subset['ga_improvement'].mean()

        differences = rs_scores - ga_scores
        if np.all(differences == 0):
            p_str = "N/A"
            sig = "-"
        else:
            _, p = stats.wilcoxon(rs_scores, ga_scores)
            p_str = f"{p:.4f}"
            sig = "✓" if p < 0.05 else "✗"

        print(f"{n:>6} {baseline:>10} {np.mean(rs_scores):>10.2f} {np.mean(ga_scores):>10.2f} "
              f"{rs_impr:>9.1f}% {ga_impr:>9.1f}% {p_str:>10} {sig:>5}")


if __name__ == "__main__":
    df = pd.read_csv(RESULTS_FILE)
    df = load_and_compute(df)

    plot_boxplot(df)
    plot_lineplot(df)
    print_summary_table(df)