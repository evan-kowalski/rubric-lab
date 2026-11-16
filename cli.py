"""Command line interface for rubric validation and scoring."""

import argparse
import json
import sys
from rubric_lab.schema import Criterion, ValidationError, validate_criterion
from rubric_lab.scoring import score_rubric


def run(json_path: str) -> int:
    """Load, validate, and score a JSON rubric file."""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        sys.stderr.write(f"Error: File not found: {json_path}
")
        return 1
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"Error: Malformed JSON: {exc}
")
        return 1
    except Exception as exc:
        sys.stderr.write(f"Error reading file: {exc}
")
        return 1

    if not isinstance(data, dict):
        sys.stderr.write("Error: Rubric root must be a JSON object
")
        return 1

    if "criteria" not in data:
        sys.stderr.write("Error: Missing required field 'criteria'
")
        return 1

    raw_criteria = data["criteria"]
    if not isinstance(raw_criteria, list) or len(raw_criteria) == 0:
        sys.stderr.write("Error: 'criteria' must be a non-empty list
")
        return 1

    criteria = []
    for index, item in enumerate(raw_criteria):
        if not isinstance(item, dict):
            sys.stderr.write(f"Error: Criterion at index {index} must be an object
")
            return 1
        if "name" not in item:
            sys.stderr.write(f"Error: Missing required field 'name' in criterion {index}
")
            return 1
        if "weight" not in item:
            sys.stderr.write(f"Error: Missing required field 'weight' in criterion {index}
")
            return 1

        try:
            criterion = Criterion(
                name=item["name"],
                description=item.get("description", item["name"]),
                weight=float(item["weight"]),
                failure_tags=item.get("failure_tags", []),
            )
            validate_criterion(criterion)
        except (ValidationError, TypeError, ValueError) as exc:
            sys.stderr.write(f"Error: Invalid criterion: {exc}
")
            return 1

        criteria.append(criterion)

    raw_scores = data.get("scores", {})
    if not isinstance(raw_scores, dict):
        sys.stderr.write("Error: 'scores' must be a JSON object
")
        return 1

    try:
        scores = {str(k): float(v) for k, v in raw_scores.items()}
    except (TypeError, ValueError) as exc:
        sys.stderr.write(f"Error: Invalid score value: {exc}
")
        return 1

    result = score_rubric(criteria, scores)

    print(f"Total score: {result.total_score:.4f} / {result.max_possible:.4f}")
    print(f"Normalized score: {result.normalized_score:.4f}")
    print("Criterion summary:")
    for cr in result.criteria_results:
        print(f"  {cr.summary}")

    print("Failure tags summary:")
    all_tags = []
    for cr in result.criteria_results:
        all_tags.extend(cr.failure_tags)

    if all_tags:
        for tag in sorted(set(all_tags)):
            print(f"  {tag}: {all_tags.count(tag)}")
    else:
        print("  None")

    return 0


def main() -> None:
    """Parse command line arguments and execute scoring."""
    parser = argparse.ArgumentParser(
        description="Validate and score evaluation rubrics."
    )
    parser.add_argument("rubric_file", help="Path to JSON rubric file")
    args = parser.parse_args()
    code = run(args.rubric_file)
    sys.exit(code)


if __name__ == "__main__":
    main()
