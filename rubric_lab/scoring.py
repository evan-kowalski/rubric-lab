from __future__ import annotations

from typing import Any, Dict, List, Sequence
from rubric_lab.schema import Criterion, RubricResult, ScoringResult


def score_criterion(criterion: Criterion, raw_score: float, max_score: float) -> ScoringResult:
    if raw_score < 0:
        raise ValueError(f"Criterion '{getattr(criterion, 'name', '')}': raw_score cannot be negative, got {raw_score}")
    if max_score < 0:
        raise ValueError(f"Criterion '{getattr(criterion, 'name', '')}': max_score cannot be negative, got {max_score}")

    crit_name = getattr(criterion, "name", str(criterion))
    weight = getattr(criterion, "weight", 1.0)
    failure_tags = list(getattr(criterion, "failure_tags", []))

    if max_score == 0:
        summary = f"Criterion '{crit_name}': division-by-zero avoided (max_score is 0), score set to 0.0"
        return ScoringResult(
            criterion_name=crit_name,
            score=0.0,
            max_score=0.0,
            weighted_score=0.0,
            summary=summary,
            failure_tags=failure_tags,
        )

    clamped_score = min(raw_score, max_score)
    weighted_score = (clamped_score / max_score) * weight
    summary = (
        f"Criterion '{crit_name}': raw_score={raw_score}, max_score={max_score}, "
        f"clamped={clamped_score}, weighted_score={weighted_score:.4f}"
    )

    return ScoringResult(
        criterion_name=crit_name,
        score=clamped_score,
        max_score=max_score,
        weighted_score=weighted_score,
        summary=summary,
        failure_tags=failure_tags,
    )


def score_rubric(
    criteria: Sequence[Criterion],
    scores_dict: Dict[str, Any],
) -> RubricResult:
    criteria_results: List[ScoringResult] = []
    missing_fields: List[str] = []

    for criterion in criteria:
        name = getattr(criterion, "name", None)
        if name is None and isinstance(criterion, dict):
            name = criterion.get("name")

        if name not in scores_dict or scores_dict[name] is None:
            missing_fields.append(name if name is not None else "")
            continue

        entry = scores_dict[name]
        if isinstance(entry, (tuple, list)):
            raw = float(entry[0])
            max_s = float(entry[1]) if len(entry) > 1 else 1.0
        elif isinstance(entry, dict):
            raw = float(entry.get("raw_score", entry.get("score", 0.0)))
            max_s = float(entry.get("max_score", 1.0))
        else:
            raw = float(entry)
            max_s = 1.0

        res = score_criterion(criterion, raw, max_s)
        criteria_results.append(res)

    total_score = sum(r.weighted_score for r in criteria_results)
    max_possible = sum(
        getattr(c, "weight", c.get("weight", 1.0) if isinstance(c, dict) else 1.0)
        for c in criteria
    )
    normalized_score = (total_score / max_possible) if max_possible > 0 else 0.0

    return RubricResult(
        criteria_results=criteria_results,
        total_score=total_score,
        max_possible=max_possible,
        normalized_score=normalized_score,
        missing_fields=missing_fields,
    )
