"""validate.py - CLI entry point for validating and scoring JSON rubrics."""

from __future__ import annotations

import argparse
import json
import sys
from rubric_lab.schema import Criterion, validate_criterion
from rubric_lab.scoring import score_rubric


def run(json_path: str) -> None:
    """Load JSON, validate criteria, compute rubric score, and print results."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    criteria = []
    for item in data.get("criteria", []):
        c = Criterion(
            name=item.get("name", ""),
            description=item.get("description", ""),
            weight=float(item.get("weight", 1.0)),
            failure_tags=item.get("failure_tags", [])
        ) if isinstance(item, dict) else item
        validate_criterion(c)
        criteria.append(c)

    scores = {str(k): float(v) for k, v in data.get("scores", {}).items()}
    result = score_rubric(criteria, scores)
    print(f"Total Score: {result.total_score} / {result.max_possible}")
    print(f"Normalized Score: {result.normalized_score:.4f}")
    for cr in result.criteria_results:
        print(f"  - {cr.criterion_name}: {cr.score}/{cr.max_score}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and score evaluation rubrics.")
    parser.add_argument("json_file", help="Path to JSON rubric file")
    args = parser.parse_args()
    run(args.json_file)


if __name__ == "__main__":
    main()
