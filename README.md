# rubric-lab

Lightweight evaluation rubric toolkit - schema, scoring, and CLI validation.

## About

`rubric-lab` is a small self-contained Python framework for defining evaluation rubrics as structured schemas, validating criteria, and scoring model outputs with normalized weights and edge-case handling.

## Components

- **`rubric_lab/schema.py`**: Typed dataclasses (`Criterion`, `ScoringResult`, `RubricResult`) and validation routines (`validate_criterion`).
- **`rubric_lab/scoring.py`**: Scoring engine providing `score_criterion` and `score_rubric` with boundary clamping, weighted normalization, missing-value handling, and failure tags.
- **`rubric_lab/validate.py`**: CLI entry point to load, validate, and score criteria from JSON files.
- **`tests/test_scoring.py`**: Unit tests covering boundary weights, malformed inputs, missing fields, clamping, and deterministic scoring.

## Honest Limitations

- **No CI**: No continuous integration workflow is currently configured on GitHub Actions.
- **No Pip Package**: Not published to PyPI; must be used directly from source.
- **Manual Testing**: Tests are not automatically executed on push or PRs.

## Quick Start

```python
from rubric_lab.schema import Criterion
from rubric_lab.scoring import score_rubric

c1 = Criterion(name="accuracy", weight=0.6, max_points=10.0)
c2 = Criterion(name="clarity", weight=0.4, max_points=10.0)

res = score_rubric([c1, c2], {"accuracy": 9.0, "clarity": 8.0})
print(f"Total: {res.total_score}, Normalized: {res.normalized_score}")
```

## CLI Usage

```bash
python -m rubric_lab.validate path/to/rubric.json
```

## License

MIT License.
