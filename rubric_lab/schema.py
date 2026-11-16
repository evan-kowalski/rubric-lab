"""schema definitions for evaluation rubrics."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


@dataclass
class Anchor:
    """concrete score anchor describing expected output characteristics."""
    score: float
    description: str
    examples: List[str] = field(default_factory=list)


@dataclass
class Dimension:
    """a single evaluation dimension within a rubric."""
    name: str
    description: str
    min_score: float = 1.0
    max_score: float = 5.0
    weight: float = 1.0
    anchors: List[Anchor] = field(default_factory=list)


@dataclass
class Rubric:
    """structured evaluation rubric containing multiple dimensions."""
    name: str
    description: str
    version: str = "0.1.0"
    dimensions: List[Dimension] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Rubric:
        """instantiate a rubric from a python dictionary."""
        dimensions = []
        for dim_data in data.get("dimensions", []):
            anchors = [
                Anchor(
                    score=float(a["score"]),
                    description=a["description"],
                    examples=a.get("examples", []),
                )
                for a in dim_data.get("anchors", [])
            ]
            dimension = Dimension(
                name=dim_data["name"],
                description=dim_data.get("description", ""),
                min_score=float(dim_data.get("min_score", 1.0)),
                max_score=float(dim_data.get("max_score", 5.0)),
                weight=float(dim_data.get("weight", 1.0)),
                anchors=anchors,
            )
            dimensions.append(dimension)

        return cls(
            name=data["name"],
            description=data.get("description", ""),
            version=data.get("version", "0.1.0"),
            dimensions=dimensions,
            metadata=data.get("metadata", {}),
        )

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> Rubric:
        """load a rubric from a json file."""
        file_path = Path(path)
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)
