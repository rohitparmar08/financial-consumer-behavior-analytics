"""
Reconciliation Tests: Verifies analytical view metrics against underlying base tables to prevent JOIN multiplication.
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


def test_reconcile_customer_counts(active_conn):
    base_count = active_conn.execute("SELECT COUNT(*) FROM customers;").fetchone()[0]
    profile_count = active_conn.execute("SELECT COUNT(*) FROM vw_customer_financial_profile;").fetchone()[0]
    assert profile_count == base_count == 15000


def test_reconcile_total_income(active_conn):
    base_income_sum = active_conn.execute("SELECT ROUND(SUM(annual_income), 2) FROM income;").fetchone()[0]
    profile_income_sum = active_conn.execute("SELECT ROUND(SUM(annual_income), 2) FROM vw_customer_financial_profile;").fetchone()[0]
    assert abs(profile_income_sum - base_income_sum) < 0.01


def test_reconcile_total_transaction_amount(active_conn):
    base_txn_sum = active_conn.execute("SELECT ROUND(SUM(amount), 2) FROM transactions;").fetchone()[0]
    profile_txn_sum = active_conn.execute("SELECT ROUND(SUM(total_transaction_amount), 2) FROM vw_customer_financial_profile;").fetchone()[0]
    assert abs(profile_txn_sum - base_txn_sum) < 0.01


def test_reconcile_total_product_holdings(active_conn):
    base_prod_count = active_conn.execute("SELECT COUNT(*) FROM financial_products;").fetchone()[0]
    profile_prod_sum = active_conn.execute("SELECT SUM(total_products) FROM vw_customer_financial_profile;").fetchone()[0]
    assert profile_prod_sum == base_prod_count
