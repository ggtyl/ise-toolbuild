import random
from generator import Participant
from scoring import compute_fairness_score


def _tournament_selection(
    population: list[list[Participant]],
    scores: list[int],
    k: int = 2
) -> list[Participant]:
    """Select best individual from k randomly chosen candidates."""
    candidates = random.sample(range(len(population)), k)
    best = min(candidates, key=lambda i: scores[i])
    return population[best][:]


def _order_crossover(
    parent_a: list[Participant],
    parent_b: list[Participant]
) -> list[Participant]:
    """
    Order Crossover (OX) for permutation problems.
    Preserves relative order of elements from both parents
    while ensuring no duplicates.
    """
    n = len(parent_a)

    # Pick random segment from parent A
    start = random.randint(0, n - 2)
    end = random.randint(start + 1, n - 1)
    segment = parent_a[start:end + 1]
    segment_ids = {p.id for p in segment}

    # Fill remaining from parent B in order, skipping segment elements
    remaining = [p for p in parent_b if p.id not in segment_ids]

    # Build child
    child = [None] * n
    child[start:end + 1] = segment

    # Fill positions before and after segment
    remaining_iter = iter(remaining)
    for i in list(range(end + 1, n)) + list(range(0, start)):
        child[i] = next(remaining_iter)

    return child


def _mutate(
    arrangement: list[Participant],
    mutation_rate: float = 0.2
) -> list[Participant]:
    """Randomly swap two positions with given probability."""
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(arrangement)), 2)
        arrangement[i], arrangement[j] = arrangement[j], arrangement[i]
    return arrangement


def genetic_algorithm(
    participants: list[Participant],
    budget: int = 100,
    population_size: int = 20,
    mutation_rate: float = 0.2,
    tournament_k: int = 2,
    seed: int = None
) -> tuple[int, list[Participant], int]:
    """
    Perform genetic algorithm search to find the fairest bracket arrangement.

    Args:
        participants: list of Participant objects (ordered by seed)
        budget: maximum number of arrangements to evaluate
        population_size: number of individuals per generation
        mutation_rate: probability of mutation
        tournament_k: number of candidates in tournament selection
        seed: random seed for reproducibility

    Returns:
        best_score: lowest fairness score found
        best_arrangement: participant ordering that achieved best_score
        evaluations: number of evaluations used
    """
    if seed is not None:
        random.seed(seed)

    evaluations = 0
    best_score = float('inf')
    best_arrangement = None

    # --- Initialisation ---
    population = []
    scores = []
    for _ in range(min(population_size, budget)):
        individual = participants[:]
        random.shuffle(individual)
        score = compute_fairness_score(individual)
        evaluations += 1

        population.append(individual)
        scores.append(score)

        if score < best_score:
            best_score = score
            best_arrangement = individual[:]

        if best_score == 0:
            return best_score, best_arrangement, evaluations

    # --- Evolution ---
    while evaluations < budget:
        # Elitism — find best individual index
        elite_idx = min(range(len(scores)), key=lambda i: scores[i])

        # Generate new population
        new_population = [population[elite_idx][:]]  # keep elite
        new_scores = [scores[elite_idx]]

        while len(new_population) < population_size and evaluations < budget:
            # Selection
            parent_a = _tournament_selection(population, scores, tournament_k)
            parent_b = _tournament_selection(population, scores, tournament_k)

            # Crossover
            child = _order_crossover(parent_a, parent_b)

            # Mutation
            child = _mutate(child, mutation_rate)

            # Evaluate
            score = compute_fairness_score(child)
            evaluations += 1

            new_population.append(child)
            new_scores.append(score)

            if score < best_score:
                best_score = score
                best_arrangement = child[:]

            if best_score == 0:
                return best_score, best_arrangement, evaluations

        population = new_population
        scores = new_scores

    return best_score, best_arrangement, evaluations


if __name__ == "__main__":
    print("=== Smoke Test: Genetic Algorithm ===\n")

    test_cases = [
        ("4 participants",  4),
        ("6 participants",  6),
        ("8 participants",  8),
        ("12 participants", 12),
        ("16 participants", 16),
    ]

    for label, n in test_cases:
        participants = [Participant(id=i) for i in range(1, n + 1)]

        # Baseline score
        baseline_score = compute_fairness_score(participants)

        # Random search score
        from random_search import random_search
        rs_score, _, rs_evals = random_search(participants, budget=100, seed=42)

        # GA score
        ga_score, ga_arrangement, ga_evals = genetic_algorithm(
            participants, budget=100, seed=42
        )

        print(f"--- {label} ---")
        print(f"  Baseline score:      {baseline_score}")
        print(f"  Random search score: {rs_score} (evals: {rs_evals})")
        print(f"  GA score:            {ga_score} (evals: {ga_evals})")
        print(f"  Best arrangement:    {[p.id for p in ga_arrangement]}")
        print(f"  GA improved over RS: {'Yes' if ga_score < rs_score else 'No'}\n")