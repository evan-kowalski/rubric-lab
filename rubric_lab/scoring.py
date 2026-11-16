"""scoring engine for evaluating model outputs against rubrics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from rubric_lab.schema import Rubric


@dataclass
class DimensionScore:
    """breakdown for a single evaluated dimension."""
    raw_score: float
    clamped_score: float
    weight: float
    weighted_score: float


@dataclass
class ScoreResult:
    """aggregated scoring result containing total and per-dimension breakdown."""
    total_score: float
    weighted_total: float
    total_weight: float
    normalized_score: float
    breakdown: Dict[str, DimensionScore] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """convert score result to dictionary representation."""
        return {
            "total_score": self.total_score,
            "weighted_total": self.weighted_total,
            "total_weight": self.total_weight,
            "normalized_score": self.normalized_score,
            "breakdown": {
                name: {
                    "raw_score": d.raw_score,
                    "clamped_score": d.clamped_score,
                    "weight": d.weight,
                    "weighted_score": d.weighted_score,
                }
                for name, d in self.breakdown.items()
            },
        }


def score_output(
    rubric: Rubric,
    scores: Dict[str, float],
    clamp: bool = True,
    strict: bool = True,
) -> ScoreResult:
    """score a model output based on per-dimension evaluations.

    Args:
        rubric: the Rubric definition.
        scores: dictionary mapping dimension name to numeric score.
        clamp: whether to clamp scores within [min_score, max_score].
        strict: if True, raises ValueError when a rubric dimension is missing.

    Returns:
        ScoreResult containing totals and per-dimension breakdown.
    """
    breakdown: Dict[str, DimensionScore] = {}
    weighted_total = 0.0
    total_weight = 0.0

    for dim in rubric.dimensions:
        if dim.name not in scores:
            if strict:
                raise ValueError(f"missing score for dimension: '{dim.name}'")
            continue

        raw = float(scores[dim.name])
        if clamp:
            clamped = max(dim.min_score, min(dim.max_score, raw))
        else:
            clamped = raw

        weighted = clamped * dim.weight
        weighted_total += weighted
        total_weight += dim.weight

        breakdown[dim.name] = DimensionScore(
            raw_score=raw,
            clamped_score=clamped,
            weight=dim.weight,
            weighted_score=weighted,
        )

    normalized = (weighted_total / total_weight) if total_weight > 0 else 0.0

    return ScoreResult(
        total_score=normalized,
        weighted_total=weighted_total,
        total_weight=total_weight,
        normalized_score=normalized,
        breakdown=breakdown,
    )
