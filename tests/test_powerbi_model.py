"""
Unit tests for Power BI Star-Schema Data Model.
Validates key uniqueness, referential integrity, table grains, and database reconciliation.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path

from src.config import Config
from src.database.export_powerbi_tables import PowerBIExporter
from src.database.run_sql_analysis import SQLAnalysisRunner
from src.validation.validate_powerbi_exports import PowerBIExportValidator


@pytest.fixture(scope="module")
def powerbi_exports(tmp_path_factory):
    """Generates Power BI CSV exports in a temporary directory for testing."""
    tmp_dir = tmp_path_factory.mktemp("pbi_data")
    cfg = Config()
    cfg.exports_dir = tmp_dir / "exports"
    
    # Run SQL views deployment first if database exists
    sql_runner = SQLAnalysisRunner(config=cfg)
    conn = sql_runner.get_connection()
    try:
        sql_runner.deploy_views(conn)
    finally:
        conn.close()
        
    exporter = PowerBIExporter(config=cfg)
    exporter.pbi_export_dir = cfg.exports_dir / "powerbi"
    counts = exporter.export_all()
    
    return cfg.exports_dir / "powerbi", counts


def test_powerbi_export_files_exist(powerbi_exports):
    pbi_dir, counts = powerbi_exports
    expected_files = [
        "dim_customer.csv",
        "dim_date.csv",
        "dim_product.csv",
        "dim_segment.csv",
        "dim_risk.csv",
        "fact_transactions.csv",
        "fact_customer_financial.csv",
        "fact_product_holdings.csv"
    ]
    for filename in expected_files:
        assert (pbi_dir / filename).exists(), f"Missing export file: {filename}"
        assert counts[filename] > 0, f"Export file {filename} is empty"


def test_dimension_primary_key_uniqueness(powerbi_exports):
    pbi_dir, _ = powerbi_exports
    
    # dim_customer
    df_customer = pd.read_csv(pbi_dir / "dim_customer.csv")
    assert len(df_customer) == 15000, "dim_customer must have exactly 15,000 rows"
    assert df_customer["customer_id"].is_unique, "dim_customer customer_id must be unique"
    
    # dim_date
    df_date = pd.read_csv(pbi_dir / "dim_date.csv")
    assert len(df_date) == 2922, "dim_date must have 2,922 rows (2018-2025)"
    assert df_date["date"].is_unique, "dim_date date must be unique"
    
    # dim_product
    df_product = pd.read_csv(pbi_dir / "dim_product.csv")
    assert len(df_product) == 7, "dim_product must have 7 product types"
    assert df_product["product_type_key"].is_unique, "dim_product product_type_key must be unique"
    
    # dim_segment
    df_segment = pd.read_csv(pbi_dir / "dim_segment.csv")
    assert len(df_segment) == 7, "dim_segment must have 7 segments"
    assert df_segment["segment_key"].is_unique, "dim_segment segment_key must be unique"
    
    # dim_risk
    df_risk = pd.read_csv(pbi_dir / "dim_risk.csv")
    assert len(df_risk) == 9, "dim_risk must have 9 risk combinations"
    assert df_risk["risk_key"].is_unique, "dim_risk risk_key must be unique"


def test_fact_table_referential_integrity(powerbi_exports):
    pbi_dir, _ = powerbi_exports
    
    df_customer = pd.read_csv(pbi_dir / "dim_customer.csv")
    df_date = pd.read_csv(pbi_dir / "dim_date.csv")
    df_product = pd.read_csv(pbi_dir / "dim_product.csv")
    df_segment = pd.read_csv(pbi_dir / "dim_segment.csv")
    df_risk = pd.read_csv(pbi_dir / "dim_risk.csv")
    
    customer_ids = set(df_customer["customer_id"])
    dates = set(df_date["date"])
    product_keys = set(df_product["product_type_key"])
    segment_keys = set(df_segment["segment_key"])
    risk_keys = set(df_risk["risk_key"])
    
    # fact_customer_financial
    df_fact_cust = pd.read_csv(pbi_dir / "fact_customer_financial.csv")
    assert len(df_fact_cust) == 15000, "fact_customer_financial must have 15,000 rows"
    assert df_fact_cust["customer_id"].is_unique, "fact_customer_financial customer_id must be unique (1-to-1 grain)"
    assert set(df_fact_cust["customer_id"]).issubset(customer_ids), "Invalid customer_id in fact_customer_financial"
    assert set(df_fact_cust["segment_key"]).issubset(segment_keys), "Invalid segment_key in fact_customer_financial"
    assert set(df_fact_cust["risk_key"]).issubset(risk_keys), "Invalid risk_key in fact_customer_financial"
    
    # fact_transactions
    df_fact_tx = pd.read_csv(pbi_dir / "fact_transactions.csv")
    assert set(df_fact_tx["customer_id"]).issubset(customer_ids), "Invalid customer_id in fact_transactions"
    assert set(df_fact_tx["transaction_date_key"]).issubset(dates), "Invalid transaction_date_key in fact_transactions"
    
    # fact_product_holdings
    df_fact_prod = pd.read_csv(pbi_dir / "fact_product_holdings.csv")
    assert set(df_fact_prod["customer_id"]).issubset(customer_ids), "Invalid customer_id in fact_product_holdings"
    assert set(df_fact_prod["product_type_key"]).issubset(product_keys), "Invalid product_type_key in fact_product_holdings"


def test_financial_health_score_range(powerbi_exports):
    pbi_dir, _ = powerbi_exports
    df_fact_cust = pd.read_csv(pbi_dir / "fact_customer_financial.csv")
    
    assert "financial_health_score" in df_fact_cust.columns
    health_scores = df_fact_cust["financial_health_score"]
    
    assert health_scores.min() >= 0.0, "Financial health score cannot be < 0"
    assert health_scores.max() <= 100.0, "Financial health score cannot be > 100"
    assert health_scores.isnull().sum() == 0, "Financial health score cannot contain nulls"


def test_powerbi_export_validation_runner():
    cfg = Config()
    exporter = PowerBIExporter(config=cfg)
    exporter.export_all()
    
    validator = PowerBIExportValidator(config=cfg)
    is_valid, errors = validator.validate_all()
    
    assert is_valid is True, f"PowerBIExportValidator detected errors: {errors}"
