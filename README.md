# ise-toolbuild

A search-based bracket fairness optimiser for single-elimination tournaments.

The tool optimises the participant ordering fed into a single-elimination bracket generator, using Random Search and a Genetic Algorithm to minimise a structural fairness score. The baseline generator is ported from Tournado, a web-based tournament management system developed as a final year project (original implementation in TypeScript/NestJS).

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
results.csv                  # Raw experiment results
boxplot_improvement.png      # Box plot figure
lineplot_improvement.png     # Line plot figure
requirements.pdf        # Dependencies and versions
manual.pdf              # User manual
replication.pdf         # Replication instructions
```

## Setup

1. Ensure Python 3.12+ is installed
2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running

All scripts should be run from the repo root with the virtual environment activated.

**Run the experiment:**
```bash
python3 src/experiment.py
```

**Run statistical analysis:**
```bash
python3 src/analysis.py
```

**Generate figures:**
```bash
python3 src/visualise.py
```

**Run individual smoke tests:**
```bash
python3 src/generator.py
python3 src/scoring.py
python3 src/random_search.py
python3 src/genetic_algorithm.py
```

## Experiment Parameters

| Parameter | Value |
|---|---|
| Participant counts | 8, 12, 16, 24, 32, 48, 64 |
| Runs per count | 30 |
| Seeds | 1–30 |
| Budget (scaled) | 100–1500 |

## Reproducibility

See `replication.pdf` for full replication instructions to reproduce the exact results reported.