import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rubric_lab.schema import validate_criterion, Criterion

def test_valid_criterion():
    c = Criterion(name='Clarity', weight=0.5, description='How clear')
    validate_criterion(c)

def test_empty_name_raises():
    with pytest.raises(ValueError, match='name'):
        validate_criterion(Criterion(name='', weight=0.5, description='x'))

def test_weight_below_zero():
    with pytest.raises(ValueError, match='weight'):
        validate_criterion(Criterion(name='A', weight=-0.1, description='x'))

def test_weight_above_one():
    with pytest.raises(ValueError, match='weight'):
        validate_criterion(Criterion(name='A', weight=1.1, description='x'))

def test_boundary_weights():
    validate_criterion(Criterion(name='Edge0', weight=0.0, description='ok'))
    validate_criterion(Criterion(name='Edge1', weight=1.0, description='ok'))

def test_empty_description():
    with pytest.raises(ValueError):
        validate_criterion(Criterion(name='A', weight=0.5, description=''))

def test_failure_tags_not_list():
    with pytest.raises((ValueError, TypeError)):
        validate_criterion(Criterion(name='A', weight=0.5, description='ok', failure_tags='string'))
