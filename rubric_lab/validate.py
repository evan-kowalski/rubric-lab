"""validate.py – Evaluation rubric data validation utilities.

Provides functions to validate Rubric, Dimension, Anchor, and evaluation entries
against schema constraints, ensuring data integrity across scoring pipelines.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union
from .schema import Anchor, Dimension, Rubric


class ValidationError(Exception):
    """Raised when rubric or evaluation data fails validation constraints."""
    pass


def validate_anchor(anchor: Anchor, min_score: float, max_score: float) -> List[str]:
    """Validate an Anchor against score bounds and description requirements."""
    errors: List[str] = []
    if not isinstance(anchor.score, (int, float)):
        errors.append("Anchor score must be numeric.")
    elif anchor.score < min_score or anchor.score > max_score:
        errors.append(f"Anchor score {anchor.score} out of bounds [{min_score}, {max_score}].")
    if not anchor.description or not anchor.description.strip():
        errors.append("Anchor description cannot be empty.")
    return errors


def validate_dimension(dim: Dimension) -> List[str]:
    """Validate a single evaluation Dimension and its associated anchors."""
    errors: List[str] = []
    if not dim.name or not dim.name.strip():
        errors.append("Dimension name cannot be empty.")
    if dim.min_score >= dim.max_score:
        errors.append(f"min_score ({dim.min_score}) must be strictly less than max_score ({dim.max_score}).")
    if dim.weight <= 0:
        errors.append(f"Dimension weight must be positive, got {dim.weight}.")
    for idx, anchor in enumerate(dim.anchors):
        anchor_errors = validate_anchor(anchor, dim.min_score, dim.max_score)
        for err in anchor_errors:
            errors.append(f"Anchor[{idx}]: {err}")
    return errors


def validate_rubric(rubric: Rubric, strict: bool = False) -> Dict[str, List[str]]:
    """Validate an entire Rubric instance. If strict=True, raise ValidationError on failure."""
    report: Dict[str, List[str]] = {}
    if not rubric.name or not rubric.name.strip():
        report["name"] = ["Rubric name cannot be empty."]
    if not rubric.dimensions:
        report["dimensions"] = ["Rubric must contain at least one dimension."]
    for dim in rubric.dimensions:
        dim_errors = validate_dimension(dim)
        if dim_errors:
            report[dim.name or "unnamed_dimension"] = dim_errors
    if strict and report:
        raise ValidationError(f"Rubric validation failed: {report}")
    return report


def validate_entry(entry: Dict[str, Any], rubric: Rubric) -> List[str]:
    """Validate a single evaluation entry score dictionary against a Rubric."""
    errors: List[str] = []
    dim_names = {dim.name: dim for dim in rubric.dimensions}
    scores = entry.get("scores", {})
    if not isinstance(scores, dict):
        return ["Entry 'scores' must be a dictionary of dimension names to scores."]
    for dim_name, score in scores.items():
        if dim_name not in dim_names:
            errors.append(f"Unknown dimension '{dim_name}' in entry scores.")
            continue
        dim = dim_names[dim_name]
        if not isinstance(score, (int, float)):
            errors.append(f"Score for '{dim_name}' must be numeric.")
        elif score < dim.min_score or score > dim.max_score:
            errors.append(f"Score {score} for '{dim_name}' is out of bounds [{dim.min_score}, {dim.max_score}].")
    return errors


def validate_batch(entries: List[Dict[str, Any]], rubric: Rubric, strict: bool = False) -> Dict[int, List[str]]:
    """Validate a batch of evaluation entries against a Rubric."""
    report: Dict[int, List[str]] = {}
    for idx, entry in enumerate(entries):
        errs = validate_entry(entry, rubric)
        if errs:
            report[idx] = errs
            if strict:
                raise ValidationError(f"Batch entry at index {idx} failed validation: {errs}")
    return report
