"""
Power BI Star-Schema Export Validator.
Validates table grains, primary keys, foreign key referential integrity, and reconciliation against SQLite base tables.
"""

from pathlib import Path
import pandas as pd
import sqlite3
from typing import Dict, List, Tuple

from src.config import Config
from src.utils.logger import setup_logger

logger = setup_logger("powerbi_validator")


class PowerBIExportValidator:
    """
    Validates star-schema integrity and reconciles Power BI CSV exports with SQLite base data.
    """

    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.pbi_dir = self.config.exports_dir / "powerbi"
        self.db_path = self.config.database_path

    def validate_all(self) -> Tuple[bool, List[str]]:
        """Executes complete validation checks across all Power BI datasets."""
        logger.info(f"Validating Power BI datasets in {self.pbi_dir}...")
        errors = []

        expected_files = [
            "dim_customer.csv", "dim_date.csv", "dim_product.csv",
            "dim_segment.csv", "dim_risk.csv", "fact_transactions.csv",
            "fact_customer_financial.csv", "fact_product_holdings.csv"
        ]

        # 1. Check file existence
        for filename in expected_files:
            file_path = self.pbi_dir / filename
            if not file_path.exists():
                errors.append(f"Missing required Power BI dataset: {filename}")

        if errors:
            return False, errors

        # Load datasets
        df_dim_cust = pd.read_csv(self.pbi_dir / "dim_customer.csv")
        df_dim_date = pd.read_csv(self.pbi_dir / "dim_date.csv")
        df_dim_prod = pd.read_csv(self.pbi_dir / "dim_product.csv")
        df_dim_seg = pd.read_csv(self.pbi_dir / "dim_segment.csv")
        df_dim_risk = pd.read_csv(self.pbi_dir / "dim_risk.csv")

        df_fact_txn = pd.read_csv(self.pbi_dir / "fact_transactions.csv")
        df_fact_fin = pd.read_csv(self.pbi_dir / "fact_customer_financial.csv")
        df_fact_prod = pd.read_csv(self.pbi_dir / "fact_product_holdings.csv")

        # 2. Check grains and row counts
        if len(df_dim_cust) != 15000:
            errors.append(f"dim_customer row count mismatch ({len(df_dim_cust)} vs expected 15,000).")

        if df_dim_cust["customer_id"].duplicated().sum() > 0:
            errors.append(f"dim_customer contains {df_dim_cust['customer_id'].duplicated().sum()} duplicate customer_id keys.")

        if len(df_dim_date) != 2922:
            errors.append(f"dim_date row count mismatch ({len(df_dim_date)} vs expected 2,922).")

        if df_dim_date["date"].duplicated().sum() > 0:
            errors.append("dim_date contains duplicate date keys.")

        if len(df_dim_prod) != 7:
            errors.append(f"dim_product row count mismatch ({len(df_dim_prod)} vs expected 7).")

        if len(df_dim_seg) != 7:
            errors.append(f"dim_segment row count mismatch ({len(df_dim_seg)} vs expected 7).")

        if len(df_dim_risk) != 9:
            errors.append(f"dim_risk row count mismatch ({len(df_dim_risk)} vs expected 9).")

        if len(df_fact_fin) != 15000:
            errors.append(f"fact_customer_financial row count mismatch ({len(df_fact_fin)} vs expected 15,000).")

        if len(df_fact_txn) != 75744:
            errors.append(f"fact_transactions row count mismatch ({len(df_fact_txn)} vs expected 75,744).")

        if len(df_fact_prod) != 31274:
            errors.append(f"fact_product_holdings row count mismatch ({len(df_fact_prod)} vs expected 31,274).")

        # 3. Check Foreign Key Referential Integrity
        cust_keys = set(df_dim_cust["customer_id"].unique())
        date_keys = set(df_dim_date["date"].unique())
        prod_keys = set(df_dim_prod["product_type"].unique())
        seg_keys = set(df_dim_seg["segment_key"].unique())
        risk_keys = set(df_dim_risk["risk_key"].unique())

        orphan_txn_cust = set(df_fact_txn["customer_id"].unique()) - cust_keys
        if orphan_txn_cust:
            errors.append(f"fact_transactions contains {len(orphan_txn_cust)} orphaned customer_ids.")

        orphan_txn_date = set(df_fact_txn["transaction_date_key"].unique()) - date_keys
        if orphan_txn_date:
            errors.append(f"fact_transactions contains {len(orphan_txn_date)} orphaned transaction_date_keys.")

        orphan_fin_cust = set(df_fact_fin["customer_id"].unique()) - cust_keys
        if orphan_fin_cust:
            errors.append(f"fact_customer_financial contains {len(orphan_fin_cust)} orphaned customer_ids.")

        orphan_fin_seg = set(df_fact_fin["segment_key"].unique()) - seg_keys
        if orphan_fin_seg:
            errors.append(f"fact_customer_financial contains {len(orphan_fin_seg)} orphaned segment_keys.")

        orphan_fin_risk = set(df_fact_fin["risk_key"].unique()) - risk_keys
        if orphan_fin_risk:
            errors.append(f"fact_customer_financial contains {len(orphan_fin_risk)} orphaned risk_keys.")

        orphan_prod_cust = set(df_fact_prod["customer_id"].unique()) - cust_keys
        if orphan_prod_cust:
            errors.append(f"fact_product_holdings contains {len(orphan_prod_cust)} orphaned customer_ids.")

        # 4. Reconciliation against SQLite base tables
        if self.db_path.exists():
            conn = sqlite3.connect(self.db_path)
            try:
                db_income_sum = conn.execute("SELECT ROUND(SUM(annual_income), 2) FROM income;").fetchone()[0]
                pbi_income_sum = round(df_fact_fin["annual_income"].sum(), 2)
                if abs(db_income_sum - pbi_income_sum) > 0.01:
                    errors.append(f"Income sum mismatch: SQLite (${db_income_sum:,.2f}) vs PBI (${pbi_income_sum:,.2f}).")

                db_txn_sum = conn.execute("SELECT ROUND(SUM(amount), 2) FROM transactions;").fetchone()[0]
                pbi_txn_sum = round(df_fact_txn["amount"].sum(), 2)
                if abs(db_txn_sum - pbi_txn_sum) > 0.01:
                    errors.append(f"Transaction spend mismatch: SQLite (${db_txn_sum:,.2f}) vs PBI (${pbi_txn_sum:,.2f}).")
            finally:
                conn.close()

        is_valid = len(errors) == 0
        if is_valid:
            logger.info("[SUCCESS] Power BI star-schema dataset validation passed with 0 errors!")
        else:
            logger.error(f"[ERROR] Power BI validation failed with {len(errors)} errors:")
            for err in errors:
                logger.error(f"  - {err}")

        return is_valid, errors


if __name__ == "__main__":
    validator = PowerBIExportValidator()
    validator.validate_all()
