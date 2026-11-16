import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rubric_lab.scoring import score_rubric

def test_single_criterion_full_score():
    rubric = [{'name': 'A', 'weight': 1.0, 'score': 5, 'max_score': 5}]
    result = score_rubric(rubric)
    assert result['total'] == pytest.approx(1.0)

def test_deterministic_scoring():
    rubric = [{'name': 'A', 'weight': 0.6, 'score': 3, 'max_score': 5},
              {'name': 'B', 'weight': 0.4, 'score': 4, 'max_score': 5}]
    r1 = score_rubric(rubric)
    r2 = score_rubric(rubric)
    assert r1['total'] == r2['total']

def test_zero_weight_ignored():
    rubric = [{'name': 'A', 'weight': 0.0, 'score': 0, 'max_score': 5},
              {'name': 'B', 'weight': 1.0, 'score': 5, 'max_score': 5}]
    assert score_rubric(rubric)['total'] == pytest.approx(1.0)

def test_missing_score_raises():
    rubric = [{'name': 'A', 'weight': 1.0, 'max_score': 5}]
    with pytest.raises((KeyError, ValueError)):
        score_rubric(rubric)

def test_empty_rubric():
    with pytest.raises((ValueError, ZeroDivisionError)):
        score_rubric([])

def test_per_criterion_summaries():
    rubric = [{'name': 'A', 'weight': 0.5, 'score': 3, 'max_score': 5},
              {'name': 'B', 'weight': 0.5, 'score': 4, 'max_score': 5}]
    result = score_rubric(rubric)
    assert 'details' in result
    assert len(result['details']) == 2
