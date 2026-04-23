# ise-toolbuild

Baseline: Single Elimination Bracket Generator
Ported from Tournado (TypeScript) to Python.

The generator uses sequential pairing — participants are paired in the order
they are given, with byes assigned to the first participants in the list.
This serves as the baseline for the bracket fairness optimiser.

Scoring Function: Bracket Fairness via Match Sum Deviation

Evaluates how fair a bracket arrangement is based on:
  1. Bye fairness   — are byes allocated to the top b seeds?
  2. Match sum rule — do match sums equal the ideal sum for each round?
                      Ideal sum for round r = 2^(rounds_remaining + 1) + 1
                      assuming stronger seed always advances.

Score of 0 = perfectly fair bracket (lower is better).

Random Search Optimiser: Bracket Fairness

Randomly shuffles participant ordering within a given budget,
evaluating the fairness score of each arrangement using the
baseline generator. Returns the best arrangement found.

Termination conditions:
  1. Budget exhausted
  2. Optimal solution found (score = 0)