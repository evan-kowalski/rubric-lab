from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Criterion:
    name: str
    description: str
    weight: float
    failure_tags: List[str] = field(default_factory=list)

@dataclass
class ScoringResult:
    criterion_name: str
    score: float
    max_score: float
    weighted_score: float
    summary: str
    failure_tags: List[str] = field(default_factory=list)

@dataclass
class RubricResult:
    criteria_results: List[ScoringResult]
    total_score: float
    max_possible: float
    normalized_score: float
    missing_fields: List[str] = field(default_factory=list)

class ValidationError(Exception):
    pass

def validate_criterion(c: Criterion) -> None:
    if not isinstance(c.name, str) or not c.name.strip():
        raise ValidationError("Criterion name must be a non-empty string")
    if not isinstance(c.description, str) or not c.description.strip():
        raise ValidationError("Criterion description must be a non-empty string")
    if not isinstance(c.weight, (int, float)) or c.weight < 0.0 or c.weight > 1.0:
        raise ValidationError(f"Criterion weight must be between 0.0 and 1.0, got {c.weight}")
    for tag in c.failure_tags:
        if not isinstance(tag, str) or not tag.strip():
            raise ValidationError("Each failure_tag must be a non-empty string")
