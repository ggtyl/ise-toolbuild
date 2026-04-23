import random
from generator import Participant, SingleEliminationGenerator
from scoring import compute_fairness_score


def random_search(
    participants: list[Participant], budget: int = 100, seed: int = None
) -> tuple[int, list[Participant]]:
    """
    Perform random search to find the fairest bracket arrangement.

    Args:
        participants: list of Participant objects (ordered by seed)
        budget: maximum number of arrangements to evaluate
        seed: random seed for reproducibility

    Returns:
        best_score: lowest fairness score found
        best_arrangement: participant ordering that achieved best_score
    """
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
        ("4 participants", 4),
        ("6 participants", 6),
        ("8 participants", 8),
        ("12 participants", 12),
        ("16 participants", 16),
    ]

    for label, n in test_cases:
        participants = [Participant(id=i) for i in range(1, n + 1)]

        # Baseline score (sequential)
        baseline_score = compute_fairness_score(participants)

        # Random search score
        budget = 100
        best_score, best_arrangement, evaluations = random_search(participants, budget, seed=42)

        print(f"--- {label} ---")
        print(f"  Baseline score:      {baseline_score}")
        print(f"  Random search score: {best_score}")
        print(f"  Best arrangement:    {[p.id for p in best_arrangement]}")
        print(f"  Evaluations used:    {evaluations}/{budget}")
        print(
            f"  Improved:            {'Yes' if best_score < baseline_score else 'No'}\n"
        )
