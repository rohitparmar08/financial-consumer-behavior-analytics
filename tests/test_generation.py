"""
Unit tests for Synthetic Data Generator.
"""
import pytest
import pandas as pd

from src.config import Config
from src.data_generation.generator import SyntheticDataGenerator


@pytest.fixture
def generator():
    # Use small customer count for fast testing
    cfg = Config()
    cfg.num_customers = 100
    return SyntheticDataGenerator(config=cfg)


def test_generation_customer_count(generator):
    df_cust = generator.generate_customers()
    assert len(df_cust) == 100
    assert df_cust["customer_id"].nunique() == 100
    assert "age" in df_cust.columns
    assert (df_cust["age"] >= 18).all() and (df_cust["age"] <= 100).all()


def test_generation_income_correlation(generator):
    df_cust = generator.generate_customers()
    df_inc = generator.generate_income(df_cust)

    assert len(df_inc) == 100
    assert (df_inc["monthly_income"] > 0).all()
    assert (df_inc["annual_income"] == (df_inc["monthly_income"] * 12).round(2)).all()


def test_generation_all_tables(generator):
    data_dict = generator.generate_all()
    expected_tables = ["customers", "income", "expenses", "savings", "debt", "credit", "transactions", "financial_products"]
    for t in expected_tables:
        assert t in data_dict
        assert isinstance(data_dict[t], pd.DataFrame)
        assert len(data_dict[t]) > 0
