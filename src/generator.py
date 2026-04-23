"""
Baseline: Single Elimination Bracket Generator

Ported from Tournado, a web-based single-elimination tournament management
system developed as a final year project (original implementation in TypeScript/NestJS).

The generator uses sequential pairing — participants are paired in the order
they are given, with byes assigned to the first participants in the list.
This sequential approach serves as the baseline for the bracket fairness optimiser.
"""

import math
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Participant:
    id: int


@dataclass
class Match:
    round_number: int
    match_number: int
    participant1: Optional[Participant] = None
    participant2: Optional[Participant] = None
    id: Optional[int] = None


@dataclass
class Bracket:
    rounds: list[list[Match]] = field(default_factory=list)


class SingleEliminationGenerator:

    @staticmethod
    def generate(participants: list[Participant]) -> Bracket:
        SingleEliminationGenerator._validate_minimum_participants(participants)
        return SingleEliminationGenerator.generate_bracket(participants)

    @staticmethod
    def _validate_minimum_participants(participants: list[Participant]) -> None:
        if not participants or len(participants) < 2:
            raise ValueError("At least two participants are required")

    @staticmethod
    def generate_bracket(participants: list[Participant]) -> Bracket:
        rounds = []
        total_participants = len(participants)

        # Calculate number of byes
        next_power_of_two = 2 ** math.ceil(math.log2(total_participants))
        byes = next_power_of_two - total_participants

        # Round 1
        round1 = []
        index = 0
        match_id = 1

        # Bye matches — assigned to first participants sequentially
        for _ in range(byes):
            round1.append(
                Match(
                    id=match_id,
                    round_number=1,
                    match_number=len(round1) + 1,
                    participant1=participants[index],
                    participant2=None,
                )
            )
            match_id += 1
            index += 1

        # Normal matches — paired sequentially
        while index < len(participants):
            round1.append(
                Match(
                    id=match_id,
                    round_number=1,
                    match_number=len(round1) + 1,
                    participant1=participants[index],
                    participant2=participants[index + 1],
                )
            )
            match_id += 1
            index += 2

        rounds.append(round1)

        # Future rounds
        previous_round = round1
        round_number = 2

        while len(previous_round) > 1:
            matches = []
            for i in range(0, len(previous_round), 2):
                matches.append(
                    Match(
                        id=match_id,
                        round_number=round_number,
                        match_number=len(matches) + 1,
                        participant1=None,
                        participant2=None,
                    )
                )
                match_id += 1
            rounds.append(matches)
            previous_round = matches
            round_number += 1

        return Bracket(rounds=rounds)

    @staticmethod
    def visualise(bracket: Bracket) -> None:
        output = "===== TOURNAMENT BRACKET =====\n"
        for round_idx, round_matches in enumerate(bracket.rounds):
            output += f"\nRound {round_matches[0].round_number} ({len(round_matches)} matches):\n"
            for match_idx, match in enumerate(round_matches):
                if round_idx == 0:
                    p1 = (
                        f"Player #{match.participant1.id}"
                        if match.participant1
                        else "BYE"
                    )
                    p2 = (
                        f"Player #{match.participant2.id}"
                        if match.participant2
                        else "BYE"
                    )
                else:
                    prev_round = bracket.rounds[round_idx - 1]
                    src1 = (
                        prev_round[match_idx * 2]
                        if match_idx * 2 < len(prev_round)
                        else None
                    )
                    src2 = (
                        prev_round[match_idx * 2 + 1]
                        if match_idx * 2 + 1 < len(prev_round)
                        else None
                    )
                    p1 = (
                        f"Winner of R{src1.round_number}-M{src1.match_number}"
                        if src1
                        else "TBD"
                    )
                    p2 = (
                        f"Winner of R{src2.round_number}-M{src2.match_number}"
                        if src2
                        else "TBD"
                    )
                output += (
                    f"  [R{match.round_number}-M{match.match_number}]: {p1} vs {p2}\n"
                )
        output += "=============================="
        print(output)


if __name__ == "__main__":
    # Quick smoke test with 6 participants
    participants = [Participant(id=i) for i in range(1, 7)]
    bracket = SingleEliminationGenerator.generate(participants)
    SingleEliminationGenerator.visualise(bracket)
