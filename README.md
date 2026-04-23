# ise-toolbuild

A search-based bracket fairness optimiser for single-elimination tournaments, built as part of the Intelligent Software Engineering coursework.

The baseline generator is ported from [Tournado](https://gitlab.com/your-tournado-repo), a web-based tournament management system.

## Project Structure
```
src/
generator.py          # Baseline: sequential bracket generator (ported from Tournado)
scoring.py            # Fairness scoring function (match sum deviation)
random_search.py      # Random Search optimiser
genetic_algorithm.py  # Genetic Algorithm optimiser
experiment.py         # Experiment runner
analysis.py           # Statistical analysis (Wilcoxon signed-rank test)
visualise.py          # Figure generation
results/
results.csv           # Raw experiment results
boxplot_improvement.png
lineplot_improvement.png
```

## Experiment Parameters

- Participant counts: 8, 12, 16, 24, 32, 48, 64
- Runs: 30 (seeds 1-30)
- Budget: scaled per participant count (100-1500)

## Running

See `replication.pdf` for full replication instructions.