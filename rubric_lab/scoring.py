from typing import List, Optional
from .schema import Criterion, ScoringResult, RubricResult, validate_criterion, ValidationError

def score_criterion(criterion: Criterion, raw_score: float, max_score: float = 1.0) -> ScoringResult:
    validate_criterion(criterion)
    if max_score <= 0:
        raise ValueError("max_score must be positive")
    clamped = max(0.0, min(raw_score, max_score))
    weighted = (clamped / max_score) * criterion.weight
    tags = criterion.failure_tags if clamped < max_score * 0.5 else []
    summary = f"{criterion.name}: {clamped}/{max_score} (weighted {weighted:.4f})"
    return ScoringResult(criterion.name, clamped, max_score, weighted, summary, tags)

def score_rubric(criteria: List[Criterion], raw_scores: dict, max_score: float = 1.0) -> RubricResult:
    results, missing = [], []
    for c in criteria:
        if c.name not in raw_scores:
            missing.append(c.name)
            results.append(score_criterion(c, 0.0, max_score))
        else:
            results.append(score_criterion(c, raw_scores[c.name], max_score))
    total = sum(r.weighted_score for r in results)
    weight_sum = sum(c.weight for c in criteria)
    normalized = total / weight_sum if weight_sum > 0 else 0.0
    return RubricResult(results, total, weight_sum, normalized, missing)
