import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rubric_lab.schema import validate_criterion, Criterion

def test_valid_criterion():
    c = Criterion(name='Clarity', weight=0.5, description='How clear')
    validate_criterion(c)  # should not raise

def test_empty_name_raises():
    with pytest.raises(ValueError, match='name'):
        validate_criterion(Criterion(name='', weight=0.5, description='x'))

def test_weight_below_zero():
    with pytest.raises(ValueError, match='weight'):
        validate_criterion(Criterion(name='A', weight=-0.1, description='x'))

def test_weight_above_one():
    with pytest.raises(ValueError, match='weight'):
        validate_criterion(Criterion(name='A', weight=1.1, description='x'))

def test_missing_description():
    with pytest.raises((ValueError, TypeError)):
        validate_criterion(Criterion(name='A', weight=0.5, description=None))

def test_weight_boundary_zero():
    validate_criterion(Criterion(name='Edge', weight=0.0, description='ok'))

def test_weight_boundary_one():
    validate_criterion(Criterion(name='Edge', weight=1.0, description='ok'))
