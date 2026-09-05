"""
Power BI Star-Schema Export Engine.
Extracts clean, normalized dimension and fact CSV datasets into data/exports/powerbi/.
"""

from pathlib import Path
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List

from src.config import Config
from src.utils.logger import setup_logger

logger = setup_logger("powerbi_exporter")


class PowerBIExporter:
    """
    Generates Power BI star-schema dimension and fact CSV files.
    """

    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.db_path = self.config.database_path
        self.pbi_export_dir = self.config.exports_dir / "powerbi"

    def get_connection(self) -> sqlite3.Connection:
        """Connects to SQLite database with foreign keys enabled."""
        if not self.db_path.exists():
            raise FileNotFoundError(f"SQLite database not found at {self.db_path}. Build database first.")
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def export_dim_customer(self, conn: sqlite3.Connection) -> pd.DataFrame:
        """Generates DIM_CUSTOMER (1 row per customer, 15,000 rows)."""
        logger.info("Generating DIM_CUSTOMER dataset...")
        query = """
        SELECT 
            c.customer_id,
            c.age,
            CASE 
                WHEN c.age < 25 THEN '18-24'
                WHEN c.age < 35 THEN '25-34'
                WHEN c.age < 50 THEN '35-49'
                WHEN c.age < 65 THEN '50-64'
                ELSE '65+'
            END AS age_group,
            c.gender,
            c.education,
            c.employment_status,
            c.marital_status,
            c.city_tier,
            c.occupation,
            c.customer_since,
            ROUND((JULIANDAY('2025-12-31') - JULIANDAY(c.customer_since)) / 365.25, 2) AS customer_tenure_years,
            CASE 
                WHEN i.monthly_income < 2500 THEN 'Low (<$2.5k)'
                WHEN i.monthly_income < 6000 THEN 'Middle ($2.5k-$6k)'
                WHEN i.monthly_income < 10000 THEN 'Upper-Middle ($6k-$10k)'
                ELSE 'High (>$10k)'
            END AS income_band
        FROM customers c
        JOIN income i ON c.customer_id = i.customer_id;
        """
        df = pd.read_sql_query(query, conn)
        return df

    def generate_dim_date(self) -> pd.DataFrame:
        """Generates continuous DIM_DATE calendar dimension (2018-01-01 to 2025-12-31, 2,922 rows)."""
        logger.info("Generating DIM_DATE calendar dimension...")
        start_date = datetime(2018, 1, 1)
        end_date = datetime(2025, 12, 31)

        date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        dates = []
        for d in date_list:
            dt_str = d.strftime("%Y-%m-%d")
            dates.append({
                "date": dt_str,
                "year": d.year,
                "quarter": (d.month - 1) // 3 + 1,
                "quarter_name": f"Q{(d.month - 1) // 3 + 1}",
                "month_num": d.month,
                "month_name": d.strftime("%B"),
                "year_month": d.strftime("%Y-%m"),
                "week_num": int(d.strftime("%U")),
                "day_of_month": d.day,
                "day_of_week": d.isoweekday(),
                "day_name": d.strftime("%A"),
                "is_weekend": 1 if d.isoweekday() in [6, 7] else 0,
                "month_start_date": d.replace(day=1).strftime("%Y-%m-%d"),
                "month_end_date": (d.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            })

        df = pd.DataFrame(dates)
        df["month_end_date"] = pd.to_datetime(df["month_end_date"]).dt.strftime("%Y-%m-%d")
        return df

    def generate_dim_product(self) -> pd.DataFrame:
        """Generates DIM_PRODUCT master dimension (7 product types)."""
        logger.info("Generating DIM_PRODUCT master dimension...")
        products = [
            {"product_type_key": "PROD_SAVINGS", "product_type": "Savings Account", "product_category": "Deposit Account", "description": "Core liquidity savings account"},
            {"product_type_key": "PROD_CREDIT_CARD", "product_type": "Credit Card", "product_category": "Revolving Credit", "description": "Revolving credit line card"},
            {"product_type_key": "PROD_PERSONAL_LOAN", "product_type": "Personal Loan", "product_category": "Unsecured Installment", "description": "Unsecured personal loan"},
            {"product_type_key": "PROD_MORTGAGE", "product_type": "Mortgage", "product_category": "Secured Real Estate", "description": "Residential real estate mortgage"},
            {"product_type_key": "PROD_INVESTMENT", "product_type": "Investment Account", "product_category": "Wealth & Securities", "description": "Brokerage investment portfolio"},
            {"product_type_key": "PROD_AUTO_LOAN", "product_type": "Auto Loan", "product_category": "Secured Vehicle", "description": "Vehicle financing loan"},
            {"product_type_key": "PROD_RETIREMENT", "product_type": "Retirement Account", "product_category": "Wealth & Pensions", "description": "Long-term tax-deferred retirement plan"}
        ]
        return pd.DataFrame(products)

    def generate_dim_segment(self) -> pd.DataFrame:
        """Generates DIM_SEGMENT dimension (7 primary business segments)."""
        logger.info("Generating DIM_SEGMENT dimension...")
        segments = [
            {"segment_key": "SEG_STRONG", "customer_segment": "Financially Strong", "segment_category": "High Value", "priority_level": 1, "description": "High income, top credit score, low DTI, healthy savings rate"},
            {"segment_key": "SEG_HIGH_SPEND", "customer_segment": "High-Income High-Spenders", "segment_category": "Revenue Driver", "priority_level": 2, "description": "High income with heavy expense ratio (>=70%) and low savings rate"},
            {"segment_key": "SEG_SAVERS", "customer_segment": "Disciplined Savers", "segment_category": "Saver Base", "priority_level": 3, "description": "Moderate income with high savings rate (>=20%) and fully funded emergency reserve"},
            {"segment_key": "SEG_DEBT_BURDENED", "customer_segment": "Debt-Burdened", "segment_category": "Credit Risk", "priority_level": 4, "description": "High DTI (>=0.45) or heavy total liabilities (>=$50k)"},
            {"segment_key": "SEG_CREDIT_RISK", "customer_segment": "Credit-Risk Customers", "segment_category": "Delinquency Target", "priority_level": 5, "description": "Credit score <580, missed payments >=3, or very high risk tier"},
            {"segment_key": "SEG_LOW_ENGAGED", "customer_segment": "Low-Engagement Customers", "segment_category": "Retention Risk", "priority_level": 6, "description": "Low transaction volume (<=3) and single product holding"},
            {"segment_key": "SEG_EMERGING", "customer_segment": "Emerging Customers", "segment_category": "General", "priority_level": 7, "description": "General customer demographic base"}
        ]
        return pd.DataFrame(segments)

    def export_dim_risk(self, conn: sqlite3.Connection) -> pd.DataFrame:
        """Generates DIM_RISK dimension (9 risk classifications)."""
        logger.info("Generating DIM_RISK dimension...")
        query = "SELECT DISTINCT credit_risk_category, debt_risk_tier FROM vw_customer_financial_profile;"
        df_risk = pd.read_sql_query(query, conn)

        risk_rows = []
        for idx, row in df_risk.iterrows():
            c_risk = row["credit_risk_category"]
            d_risk = row["debt_risk_tier"]
            r_key = f"RISK_{c_risk.upper().replace(' ', '_')}_{d_risk.upper().replace(' ', '_')}"

            # Severity rank (1=Critical, 4=Low)
            if "Critical" in d_risk or "Very High" in c_risk:
                rank = 1
            elif "High" in d_risk or "High" in c_risk:
                rank = 2
            elif "Moderate" in d_risk or "Medium" in c_risk:
                rank = 3
            else:
                rank = 4

            risk_rows.append({
                "risk_key": r_key,
                "credit_risk_category": c_risk,
                "debt_risk_tier": d_risk,
                "risk_severity_rank": rank,
                "description": f"Credit Bureau: {c_risk} | Debt Burden: {d_risk}"
            })

        return pd.DataFrame(risk_rows)

    def export_fact_transactions(self, conn: sqlite3.Connection) -> pd.DataFrame:
        """Generates FACT_TRANSACTIONS (1 row per transaction, 75,744 rows)."""
        logger.info("Generating FACT_TRANSACTIONS dataset...")
        query = """
        SELECT 
            transaction_id,
            customer_id,
            SUBSTR(transaction_date, 1, 10) AS transaction_date_key,
            transaction_date AS transaction_datetime,
            transaction_type,
            category,
            amount,
            payment_method,
            merchant_type
        FROM transactions;
        """
        df = pd.read_sql_query(query, conn)
        return df

    def export_fact_customer_financial(self, conn: sqlite3.Connection) -> pd.DataFrame:
        """Generates FACT_CUSTOMER_FINANCIAL (1 row per customer, 15,000 rows)."""
        logger.info("Generating FACT_CUSTOMER_FINANCIAL dataset...")
        query = """
        SELECT 
            p.customer_id,
            CASE p.customer_segment
                WHEN 'Financially Strong' THEN 'SEG_STRONG'
                WHEN 'High-Income High-Spenders' THEN 'SEG_HIGH_SPEND'
                WHEN 'Disciplined Savers' THEN 'SEG_SAVERS'
                WHEN 'Debt-Burdened' THEN 'SEG_DEBT_BURDENED'
                WHEN 'Credit-Risk Customers' THEN 'SEG_CREDIT_RISK'
                WHEN 'Low-Engagement Customers' THEN 'SEG_LOW_ENGAGED'
                ELSE 'SEG_EMERGING'
            END AS segment_key,
            ('RISK_' || UPPER(REPLACE(p.credit_risk_category, ' ', '_')) || '_' || UPPER(REPLACE(p.debt_risk_tier, ' ', '_'))) AS risk_key,
            p.monthly_income,
            p.annual_income,
            p.total_monthly_expense,
            p.housing_expense,
            p.food_expense,
            p.transportation_expense,
            p.healthcare_expense,
            p.entertainment_expense,
            p.utilities_expense,
            p.other_expense,
            p.disposable_income,
            p.expense_to_income_ratio,
            p.monthly_savings,
            p.savings_balance,
            p.savings_rate,
            p.emergency_fund_status,
            p.net_savings_capacity,
            p.savings_behavior_tier,
            p.credit_card_debt,
            p.personal_loan,
            p.education_loan,
            p.vehicle_loan,
            p.mortgage,
            p.total_debt,
            p.debt_to_income_ratio,
            p.credit_score,
            p.payment_behavior,
            p.missed_payments,
            p.credit_utilization,
            p.credit_risk_category,
            p.debt_risk_tier,
            p.total_transactions,
            p.total_transaction_amount,
            p.avg_transaction_amount,
            p.total_products,
            p.active_products,
            r.r_score,
            r.f_score,
            r.m_score,
            r.rfm_score_code,
            r.rfm_composite_score,
            r.rfm_segment
        FROM vw_customer_financial_profile p
        JOIN vw_rfm_segments r ON p.customer_id = r.customer_id;
        """
        df = pd.read_sql_query(query, conn)

        # Calculate Financial Health Score (0-100 index)
        # Component 1: Savings Rate (max 30 pts) -> min(30, savings_rate * 150)
        c1 = np.minimum(30.0, df["savings_rate"].values * 150.0)

        # Component 2: Debt Burden (max 25 pts) -> max(0, 25 - DTI * 25)
        c2 = np.maximum(0.0, 25.0 - df["debt_to_income_ratio"].values * 25.0)

        # Component 3: Credit Quality (max 25 pts) -> min(25, max(0, (credit_score - 300) / 22))
        c3 = np.minimum(25.0, np.maximum(0.0, (df["credit_score"].values - 300.0) / 22.0))

        # Component 4: Payment History (max 20 pts) -> max(0, 20 - missed_payments * 5)
        c4 = np.maximum(0.0, 20.0 - df["missed_payments"].values * 5.0)

        df["financial_health_score"] = np.round(np.clip(c1 + c2 + c3 + c4, 0.0, 100.0), 2)
        return df

    def export_fact_product_holdings(self, conn: sqlite3.Connection) -> pd.DataFrame:
        """Generates FACT_PRODUCT_HOLDINGS (1 row per product holding, 31,274 rows)."""
        logger.info("Generating FACT_PRODUCT_HOLDINGS dataset...")
        query = """
        SELECT 
            fp.product_id,
            fp.customer_id,
            CASE fp.product_type
                WHEN 'Savings Account' THEN 'PROD_SAVINGS'
                WHEN 'Credit Card' THEN 'PROD_CREDIT_CARD'
                WHEN 'Personal Loan' THEN 'PROD_PERSONAL_LOAN'
                WHEN 'Mortgage' THEN 'PROD_MORTGAGE'
                WHEN 'Investment Account' THEN 'PROD_INVESTMENT'
                WHEN 'Auto Loan' THEN 'PROD_AUTO_LOAN'
                WHEN 'Retirement Account' THEN 'PROD_RETIREMENT'
                ELSE 'PROD_SAVINGS'
            END AS product_type_key,
            fp.product_type,
            fp.product_status,
            fp.signup_date AS signup_date_key,
            CASE WHEN fp.product_status = 'Active' THEN 1 ELSE 0 END AS is_active
        FROM financial_products fp;
        """
        df = pd.read_sql_query(query, conn)
        return df

    def export_all(self) -> Dict[str, int]:
        """
        Full Power BI dataset generation workflow.
        """
        self.pbi_export_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Starting Power BI star-schema export to {self.pbi_export_dir}...")

        conn = self.get_connection()
        try:
            dim_customer = self.export_dim_customer(conn)
            dim_date = self.generate_dim_date()
            dim_product = self.generate_dim_product()
            dim_segment = self.generate_dim_segment()
            dim_risk = self.export_dim_risk(conn)

            fact_transactions = self.export_fact_transactions(conn)
            fact_customer_financial = self.export_fact_customer_financial(conn)
            fact_product_holdings = self.export_fact_fact_product_holdings(conn) if hasattr(self, 'export_fact_fact_product_holdings') else self.export_fact_product_holdings(conn)

            exports = {
                "dim_customer.csv": dim_customer,
                "dim_date.csv": dim_date,
                "dim_product.csv": dim_product,
                "dim_segment.csv": dim_segment,
                "dim_risk.csv": dim_risk,
                "fact_transactions.csv": fact_transactions,
                "fact_customer_financial.csv": fact_customer_financial,
                "fact_product_holdings.csv": fact_product_holdings
            }

            counts = {}
            for filename, df in exports.items():
                out_path = self.pbi_export_dir / filename
                df.to_csv(out_path, index=False)
                counts[filename] = len(df)
                logger.info(f"Saved Power BI dataset: {filename} ({len(df):,} rows, {len(df.columns)} columns).")

            logger.info("[SUCCESS] Power BI star-schema export completed successfully.")
            return counts
        finally:
            conn.close()


if __name__ == "__main__":
    exporter = PowerBIExporter()
    exporter.export_all()
