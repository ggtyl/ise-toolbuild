import math
from generator import Participant, SingleEliminationGenerator


def compute_fairness_score(participants: list[Participant]) -> int:
    n = len(participants)
    next_power_of_two = 2 ** math.ceil(math.log2(n))
    byes = next_power_of_two - n
    total_rounds = int(math.log2(next_power_of_two))

    bracket = SingleEliminationGenerator.generate_bracket(participants)
    round1 = bracket.rounds[0]

    # --- Rule 2: Bye fairness ---
    # Top b seeds should receive byes (b = number of byes)
    top_seeds = set(range(1, byes + 1))
    bye_penalty = 0
    for match in round1:
        if match.participant2 is None:  # bye match
            if match.participant1.id not in top_seeds:
                bye_penalty += 1

    # --- Simulate bracket forward ---
    # Track which seed occupies each match slot per round
    # Round 1: extract seeds from actual participants
    current_round_seeds = []
    for match in round1:
        p1 = match.participant1.id if match.participant1 else None
        p2 = match.participant2.id if match.participant2 else None
        current_round_seeds.append((p1, p2))

    # --- Score all rounds ---
    round_score = 0
    for round_idx in range(total_rounds):
        rounds_remaining = total_rounds - round_idx
        ideal_sum = 2 ** rounds_remaining + 1

        next_round_seeds = []
        for p1, p2 in current_round_seeds:
            if p2 is None:
                # Bye match — real participant advances, no scoring
                next_round_seeds.append(p1)
            else:
                # Real match — score and advance lower seed (stronger)
                round_score += abs((p1 + p2) - ideal_sum)
                winner = min(p1, p2)
                next_round_seeds.append(winner)

        # Pair winners for next round
        if len(next_round_seeds) > 1:
            current_round_seeds = [
                (next_round_seeds[i], next_round_seeds[i + 1])
                for i in range(0, len(next_round_seeds), 2)
            ]
        else:
            break

    return bye_penalty + round_score


if __name__ == "__main__":
    print("=== Smoke Test: Scoring Function ===\n")

    test_cases = {
        "6 participants — baseline (sequential)": [1, 2, 3, 4, 5, 6],
        "6 participants — ideal":                 [1, 2, 4, 5, 3, 6],  # byes to seed 1,2; matches: 3v6, 4v5 — will verify
        "6 participants — wrong bye allocation":  [3, 5, 1, 2, 4, 6],  # byes to seed 3,5
        "8 participants — baseline (sequential)": [1, 2, 3, 4, 5, 6, 7, 8],
        "8 participants — ideal":                 [1, 8, 5, 4, 3, 6, 7, 2],
        "12 participants — baseline":             list(range(1, 13)),
        "12 participants — ideal":                [1, 4, 3, 2, 8, 9, 5, 12, 6, 11, 7, 10],  # will verify
        "16 participants — baseline":             list(range(1, 17)),
        "16 participants — ideal":                [1, 16, 8, 9, 4, 13, 5, 12, 3, 14, 6, 11, 2, 15, 7, 10],
    }

    for label, seeds in test_cases.items():
        participants = [Participant(id=s) for s in seeds]
        score = compute_fairness_score(participants)
        print(f"{label}")
        print(f"  Arrangement: {seeds}")
        print(f"  Score: {score}\n")