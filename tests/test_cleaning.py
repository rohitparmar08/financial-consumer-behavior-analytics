"""
Unit tests for Data Cleaner module.
"""
import pytest
import pandas as pd
import numpy as np

from src.data_cleaning.cleaner import DataCleaner


@pytest.fixture
def cleaner():
    return DataCleaner()


def test_clean_customers(cleaner):
    raw_df = pd.DataFrame({
        "Customer ID": ["CUST-001", "CUST-001", "CUST-002"],
        "Age": ["25", "25", "150"],
        "Gender": [" male ", "Female", "Non-binary"],
        "Education": ["bachelor's", "MASTER'S", "High School"],
        "Employment Status": [" employed ", "retired", "unemployed"],
        "Marital Status": ["single", "married", "divorced"],
        "City Tier": ["tier 1", "tier 2", "tier 3"],
        "Occupation": ["software", "healthcare", "finance"],
        "Customer Since": ["2022-01-01", "2022-01-01", "invalid_date"]
    })

    cleaned = cleaner.clean_customers(raw_df)

    assert len(cleaned) == 2  # Duplicate removed
    assert cleaned["customer_id"].tolist() == ["CUST-001", "CUST-002"]
    assert cleaned["gender"].iloc[0] == "Male"
    assert cleaned["age"].iloc[1] == 100  # Clipped to 100 max


def test_clean_income_and_recalculation(cleaner):
    raw_df = pd.DataFrame({
        "income_id": ["INC-001", "INC-002"],
        "customer_id": ["CUST-001", "CUST-002"],
        "monthly_income": [5000.0, -100.0],
        "annual_income": [50000.0, 0.0],
        "income_source": ["Salary", "Salary"],
        "income_stability": [None, "High"]
    })

    cleaned = cleaner.clean_income(raw_df)
    assert cleaned["monthly_income"].iloc[1] == 100.0  # Clipped negative
    assert cleaned["annual_income"].iloc[0] == 60000.0  # Recalculated 5000 * 12
    assert cleaned["income_stability"].iloc[0] == "Medium"  # Imputed
