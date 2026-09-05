"""
Unit & Integration Tests for Part 2 Analytical SQL Views.
"""
import pytest
import sqlite3
import pandas as pd

from src.config import Config
from src.database.run_sql_analysis import SQLAnalysisRunner


@pytest.fixture
def runner():
    return SQLAnalysisRunner()


@pytest.fixture
def active_conn(runner):
    conn = runner.get_connection()
    runner.deploy_views(conn)
    yield conn
    conn.close()


def test_customer_financial_profile_row_count_and_uniqueness(active_conn):
    df_cust = pd.read_sql_query("SELECT customer_id FROM customers;", active_conn)
    df_profile = pd.read_sql_query("SELECT customer_id FROM vw_customer_financial_profile;", active_conn)

    assert len(df_profile) == len(df_cust) == 15000
    assert df_profile["customer_id"].nunique() == 15000


def test_rfm_scores_bounded(active_conn):
    df_rfm = pd.read_sql_query("SELECT r_score, f_score, m_score, rfm_segment FROM vw_rfm_segments;", active_conn)
    assert len(df_rfm) == 15000
    assert (df_rfm["r_score"] >= 1).all() and (df_rfm["r_score"] <= 5).all()
    assert (df_rfm["f_score"] >= 1).all() and (df_rfm["f_score"] <= 5).all()
    assert (df_rfm["m_score"] >= 1).all() and (df_rfm["m_score"] <= 5).all()
    assert not df_rfm["rfm_segment"].isnull().any()


def test_all_views_queryable(active_conn):
    views = [
        "vw_customer_financial_profile",
        "vw_customer_behavior_summary",
        "vw_customer_segments",
        "vw_rfm_segments",
        "vw_monthly_transaction_summary",
        "vw_product_adoption_summary",
        "vw_financial_risk_summary"
    ]
    for v in views:
        df = pd.read_sql_query(f"SELECT * FROM {v} LIMIT 5;", active_conn)
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
