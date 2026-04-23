"""
Random Search Optimiser: Bracket Fairness

Randomly shuffles participant ordering within a given budget,
evaluating the fairness score of each arrangement using the
baseline generator. Returns the best arrangement found.

Parameters:
  participants: list of Participant objects (ordered by seed rank)
  budget: maximum number of arrangements to evaluate
  seed: random seed for reproducibility

Returns:
  best_score: lowest fairness score found
  best_arrangement: participant ordering that achieved best_score
  evaluations: number of evaluations used

Termination conditions:
  1. Budget exhausted
  2. Optimal solution found (score = 0)
"""

import random
from generator import Participant
from scoring import compute_fairness_score


def random_search(
    participants: list[Participant], budget: int = 100, seed: int = None
) -> tuple[int, list[Participant]]:
    if seed is not None:
        random.seed(seed)

    best_score = float("inf")
    best_arrangement = None
    evaluations = 0

    for _ in range(budget):
        evaluations += 1
        # Randomly shuffle participant order
        arrangement = participants[:]
        random.shuffle(arrangement)

        # Score the arrangement
        score = compute_fairness_score(arrangement)

        # Update best if improved
        if score < best_score:
            best_score = score
            best_arrangement = arrangement

        # Early stopping — optimal solution found
        if best_score == 0:
            break

    return best_score, best_arrangement, evaluations


if __name__ == "__main__":
    print("=== Smoke Test: Random Search ===\n")

    test_cases = [
        ("8 participants", 8, 100),
        ("12 participants", 12, 200),
        ("16 participants", 16, 300),
        ("24 participants", 24, 500),
        ("32 participants", 32, 750),
    ]

    for label, n, budget in test_cases:
        participants = [Participant(id=i) for i in range(1, n + 1)]
        baseline_score = compute_fairness_score(participants)
        best_score, best_arrangement, evaluations = random_search(
            participants, budget, seed=42
        )

        print(f"--- {label} ---")
        print(f"  Baseline score:      {baseline_score}")
        print(f"  Random search score: {best_score}")
        print(f"  Best arrangement:    {[p.id for p in best_arrangement]}")
        print(f"  Evaluations used:    {evaluations}/{budget}")
        print(
            f"  Improved:            {'Yes' if best_score < baseline_score else 'No'}\n"
        )
