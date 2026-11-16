# rubric-lab

lightweight evaluation rubric toolkit — schema, scoring, and worked examples.

## about

rubric-lab is a small self-contained framework for defining eval rubrics as structured schemas, scoring model outputs, and collecting worked examples.

## current status

early development, hand-written examples from public model behavior only.

## directory structure

rubric-lab/
├── README.md
├── ROADMAP.md
├── rubric_lab/
│   ├── __init__.py
│   ├── schema.py
│   ├── scoring.py
│   └── validate.py
├── examples/
│   ├── factuality.json
│   └── tone.json
└── tests/
    └── test_scoring.py

## quick start

```python
from rubric_lab.schema import Rubric
from rubric_lab.scoring import score_output

rubric = Rubric.from_file("examples/factuality.json")
scores = {"correctness": 4, "specificity": 5, "source_grounding": 3}
result = score_output(rubric, scores)
print(result["total_score"], result["percentage"])
```

## license

mit license.
