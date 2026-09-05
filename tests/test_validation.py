"""
Unit tests for Data Validator module.
"""
import pytest
import pandas as pd

from src.validation.validator import DataValidator


@pytest.fixture
def validator():
    return DataValidator()


def test_validator_uniqueness(validator):
    df_good = pd.DataFrame({"customer_id": ["C1", "C2", "C3"]})
    errors = validator.validate_uniqueness(df_good, "customer_id", "test_table")
    assert len(errors) == 0

    df_bad = pd.DataFrame({"customer_id": ["C1", "C1", None]})
    errors = validator.validate_uniqueness(df_bad, "customer_id", "test_table")
    assert len(errors) == 2


def test_validator_referential_integrity(validator):
    parent = pd.DataFrame({"customer_id": ["C1", "C2"]})
    child_good = pd.DataFrame({"customer_id": ["C1", "C2", "C1"]})
    child_bad = pd.DataFrame({"customer_id": ["C1", "C99"]})

    errs_good = validator.validate_referential_integrity(parent, child_good, "customer_id", "customer_id", "child")
    assert len(errs_good) == 0

    errs_bad = validator.validate_referential_integrity(parent, child_bad, "customer_id", "customer_id", "child")
    assert len(errs_bad) == 1
    assert "orphaned keys" in errs_bad[0]
