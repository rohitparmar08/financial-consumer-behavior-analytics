"""
Unit tests for Power BI CSV Exports.
"""
import pytest
import pandas as pd
from pathlib import Path

from src.config import Config
from src.database.run_sql_analysis import SQLAnalysisRunner


def test_analytical_exports_generated(tmp_path):
    cfg = Config()
    cfg.exports_dir = tmp_path / "exports"

    runner = SQLAnalysisRunner(config=cfg)
    conn = runner.get_connection()
    try:
        runner.deploy_views(conn)
        counts = runner.export_analytical_tables(conn)

        assert "customer_financial_profile.csv" in counts
        assert counts["customer_financial_profile.csv"] == 15000

        # Read exported file and assert columns
        df_profile = pd.read_csv(cfg.exports_dir / "customer_financial_profile.csv")
        assert len(df_profile) == 15000
        assert "customer_id" in df_profile.columns
        assert "customer_segment" in df_profile.columns
        assert "income_band" in df_profile.columns
    finally:
        conn.close()
