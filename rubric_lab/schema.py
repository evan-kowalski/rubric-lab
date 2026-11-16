from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Criterion:
    name: str
    description: str
    weight: float
    failure_tags: list[str] = field(default_factory=list)


@dataclass
class ScoringResult:
    criterion_name: str
    score: float
    max_score: float
    weighted_score: float
    summary: str
    failure_tags: list[str] = field(default_factory=list)


@dataclass
class RubricResult:
    criteria_results: list[ScoringResult]
    total_score: float
    max_possible: float
    normalized_score: float
    missing_fields: list[str] = field(default_factory=list)


def validate_criterion(criterion: Criterion) -> None:
    if not isinstance(criterion.name, str) or not criterion.name.strip():
        raise ValueError(f'Criterion "{getattr(criterion, "name", "")}": name must be a non-empty string')
    if not isinstance(criterion.weight, (int, float)) or not (0.0 <= float(criterion.weight) <= 1.0):
        raise ValueError(f'Criterion "{criterion.name}": weight must be between 0.0 and 1.0, got {criterion.weight}')
    if not isinstance(criterion.description, str) or not criterion.description.strip():
        raise ValueError(f'Criterion "{criterion.name}": description must be a non-empty string')
    if not isinstance(criterion.failure_tags, list) or not all(isinstance(tag, str) for tag in criterion.failure_tags):
        raise ValueError(f'Criterion "{criterion.name}": failure_tags must be a list of strings')
