"""validate.py – Data-validation helpers for evaluation rubrics."""
from typing import Any, Dict, List
from .schema import Anchor, Dimension, Rubric

class ValidationError(Exception):
    """Raised when a rubric fails validation."""

def validate_dimension(dim: Dimension) -> List[str]:
    """Return a list of validation errors for a dimension."""
    errors = []
    if not dim.name or not dim.name.strip():
        errors.append("dimension name is empty")
    if dim.min_score >= dim.max_score:
        errors.append("min_score must be less than max_score")
    if dim.weight <= 0:
        errors.append("weight must be positive")
    return errors

def validate_rubric(rubric: Rubric, strict: bool = False) -> Dict[str, List[str]]:
    """Validate a rubric. If strict, raise on first error."""
    report = {}
    if not rubric.name or not rubric.name.strip():
        report["name"] = ["rubric name is empty"]
    for dim in rubric.dimensions:
        errs = validate_dimension(dim)
        if errs:
            if strict:
                raise ValidationError(f"{dim.name}: {errs}")
            report[dim.name] = errs
    return report

def validate_case(case: Any) -> List[str]:
    """Return a list of validation errors."""
    errors = []
    if hasattr(case, "case_id") and not case.case_id:
        errors.append("case_id is empty")
    return errors

def validate_batch(cases: List[Any], strict: bool = False) -> Dict:
    """Validate a batch of cases."""
    report = {}
    for case in cases:
        errs = validate_case(case)
        if errs:
            cid = getattr(case, "case_id", "unknown")
            if strict:
                raise ValidationError(f"{cid}: {errs}")
            report[cid] = errs
    return report
