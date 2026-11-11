# Reddit Comment Ranking — DEL02 Initial Computational Prototype

A small Mesa adaptation that compares two ways of ordering a synthetic 100-comment discussion thread:

- **Baseline:** rank every comment by net vote score.
- **Alternative:** reserve two positions in the top ten for the highest-scoring comments posted in the second half of the thread, and fill the other eight positions by net vote score.

The same synthetic comment dataset is used in both conditions. The only experimental difference is the ranking rule.

## Requirements

- Python 3.10 or 3.11
- Mesa 3.3.1
- pandas 2.2.3

The preserved Epstein Civil Violence source snapshot is from Mesa tag `v3.3.1`.

## Setup

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows

python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the Reddit ranking prototype

```bash
python -m src.project_model.run_experiment
```

The command runs one Mesa step for each condition and writes four CSV files to `outputs/`:

| File | Contents |
|---|---|
| `baseline_raw_00_comment_scores.csv` | All 100 comments and their synthetic vote data |
| `baseline_processed_00_top10_ranking.csv` | Baseline top-ten ranking |
| `alternative_raw_00_comment_scores.csv` | The same 100 comments used in the alternative condition |
| `alternative_processed_00_top10_ranking.csv` | Alternative top-ten ranking, including reserved positions |

The processed files include `is_newer` and `reserved_slot` columns so the intervention is directly inspectable.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

The tests check reproducibility, identical starting data, top-ten size, reserved newer-comment placement, uniqueness, and the Mesa `step()` execution path.

## Preserved Mesa source example

The original Mesa example is preserved under:

```text
src/civil_violence/
```

It is the Epstein Civil Violence example from Mesa `v3.3.1`. The original files are kept separate from the project adaptation in `src/project_model/`.

The original interactive example can be launched with:

```bash
solara run src/civil_violence/app.py
```

This uses the installed Mesa package's `mesa.examples.advanced.epstein_civil_violence` module, matching the imports in the original Mesa source. The visualization dependencies are included through the `mesa[rec]` extra in `requirements.txt`.

## Repository layout

```text
.
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── civil_violence/          # preserved Mesa source example
│   │   ├── __init__.py
│   │   ├── agents.py
│   │   ├── model.py
│   │   ├── app.py
│   │   └── SOURCE.md
│   └── project_model/           # Reddit ranking adaptation
│       ├── __init__.py
│       ├── agents.py
│       ├── model.py
│       └── run_experiment.py
├── tests/
│   └── test_model.py
├── docs/
│   └── DEL02_REPORT_ALIGNMENT.md
└── outputs/
```

## Model scope and limitations

This is a static ranking prototype. Comment agents hold timestamp and vote-count state; the model applies a ranking rule when `ThreadModel.step()` is called. It does **not** simulate real readers, commenters, vote changes, exposure-driven voting, or Reddit's proprietary ranking algorithm. The dataset and ranking intervention are synthetic and illustrative.

The prototype demonstrates what the specified ranking rules produce under the same starting data. It does not establish how actual Reddit users or platform systems behave.

## Reproducibility

Both conditions use `seed=42` and the same data-generation procedure. The experiment checks that their raw dataframes are identical before writing outputs. The baseline/alternative comparison therefore changes the ranking condition, not the synthetic comment data.
