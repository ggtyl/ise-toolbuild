"""
Experiment Runner: Bracket Fairness Optimisation

Runs the baseline, Random Search, and Genetic Algorithm across
multiple participant counts and independent runs, recording all
results to a CSV file for subsequent statistical analysis.

Experiment Parameters:
  Participant counts: 8, 12, 16, 24, 32, 48, 64
  Runs:               30 (seeds 1-30 for reproducibility)
  Budget:             scaled per participant count (100-1500)

Output:
  results/results.csv — one row per run per participant count
"""

import os
import csv
from generator import Participant
from scoring import compute_fairness_score
from random_search import random_search
from genetic_algorithm import genetic_algorithm

# --- Experiment Parameters ---
PARTICIPANT_COUNTS = [8, 12, 16, 24, 32, 48, 64]
RUNS = 30
SEEDS = list(range(1, RUNS + 1))
BUDGETS = {
    8: 100,
    12: 200,
    16: 300,
    24: 500,
    32: 750,
    48: 1000,
    64: 1500,
}
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
RESULTS_FILE = os.path.join(RESULTS_DIR, "results.csv")


def run_experiments():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    with open(RESULTS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "participants",
                "baseline_score",
                "run",
                "seed",
                "budget",
                "rs_score",
                "rs_evals",
                "ga_score",
                "ga_evals",
            ]
        )

        for n in PARTICIPANT_COUNTS:
            participants = [Participant(id=i) for i in range(1, n + 1)]
            budget = BUDGETS[n]

            # Baseline — deterministic, compute once
            baseline_score = compute_fairness_score(participants)
            print(
                f"\n=== {n} participants | Baseline: {baseline_score} | Budget: {budget} ==="
            )

            for run, seed in enumerate(SEEDS, start=1):
                print(f"  Run {run:02d}/30 (seed={seed})...", end=" ", flush=True)

                # Random Search
                rs_score, _, rs_evals = random_search(
                    participants, budget=budget, seed=seed
                )

                # Genetic Algorithm
                ga_score, _, ga_evals = genetic_algorithm(
                    participants, budget=budget, seed=seed
                )

                print(
                    f"RS={rs_score} ({rs_evals} evals) | GA={ga_score} ({ga_evals} evals)"
                )

                writer.writerow(
                    [
                        n,
                        baseline_score,
                        run,
                        seed,
                        budget,
                        rs_score,
                        rs_evals,
                        ga_score,
                        ga_evals,
                    ]
                )

    print(f"\nResults saved to {RESULTS_FILE}")


if __name__ == "__main__":
    run_experiments()
