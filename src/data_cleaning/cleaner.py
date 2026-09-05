"""
Data Cleaning Engine for Financial Consumer Behavior Analytics.
Standardizes, cleans, imputes missing values, removes duplicates, and recalculates metrics.
"""

from pathlib import Path
import pandas as pd
import numpy as np
from typing import Dict

from src.config import Config
from src.utils.logger import setup_logger

logger = setup_logger("data_cleaning")


class DataCleaner:
    """
    Cleans raw CSV datasets into normalized, high-quality processed datasets.
    """

    def __init__(self, config: Config = None):
        self.config = config or Config()

    @staticmethod
    def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Standardizes column names to snake_case."""
        df = df.copy()
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("-", "_")
        return df

    def clean_customers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans and standardizes the CUSTOMERS table."""
        logger.info("Cleaning CUSTOMERS table...")
        df = self._standardize_columns(df)

        # Strip whitespace and normalize title case for text columns
        text_cols = ["gender", "education", "employment_status", "marital_status", "city_tier", "occupation"]
        for col in text_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.title()

        # Validate age bounds (18-100)
        df["age"] = pd.to_numeric(df["age"], errors="coerce").fillna(30).astype(int)
        df["age"] = df["age"].clip(lower=18, upper=100)

        # Format dates
        df["customer_since"] = pd.to_datetime(df["customer_since"], errors="coerce").dt.strftime("%Y-%m-%d")

        # Deduplicate on customer_id
        initial_len = len(df)
        df = df.drop_duplicates(subset=["customer_id"]).reset_index(drop=True)
        if len(df) < initial_len:
            logger.info(f"Removed {initial_len - len(df)} duplicate customer records.")

        return df

    def clean_income(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans and standardizes the INCOME table."""
        logger.info("Cleaning INCOME table...")
        df = self._standardize_columns(df)

        df["monthly_income"] = pd.to_numeric(df["monthly_income"], errors="coerce").fillna(500.0)
        df["monthly_income"] = df["monthly_income"].apply(lambda x: max(100.0, float(x)))

        # Recalculate annual_income for 100% consistency
        df["annual_income"] = np.round(df["monthly_income"] * 12.0, 2)

        # Impute missing income_stability
        df["income_stability"] = df["income_stability"].fillna("Medium").astype(str).str.strip().str.title()

        df = df.drop_duplicates(subset=["customer_id"]).reset_index(drop=True)
        return df

    def clean_expenses(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans and standardizes the EXPENSES table."""
        logger.info("Cleaning EXPENSES table...")
        df = self._standardize_columns(df)

        exp_cols = [
            "housing_expense", "food_expense", "transportation_expense",
            "healthcare_expense", "entertainment_expense", "utilities_expense", "other_expense"
        ]

        for col in exp_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
            df[col] = df[col].apply(lambda x: max(0.0, float(x)))

        # Recalculate total_monthly_expense
        df["total_monthly_expense"] = np.round(df[exp_cols].sum(axis=1), 2)

        df = df.drop_duplicates(subset=["customer_id"]).reset_index(drop=True)
        return df

    def clean_savings(self, df: pd.DataFrame, df_income: pd.DataFrame, df_expenses: pd.DataFrame) -> pd.DataFrame:
        """Cleans SAVINGS table and enforces mathematical consistency."""
        logger.info("Cleaning SAVINGS table...")
        df = self._standardize_columns(df)

        df = df.drop_duplicates(subset=["customer_id"]).reset_index(drop=True)

        df["monthly_savings"] = pd.to_numeric(df["monthly_savings"], errors="coerce").fillna(0.0).apply(lambda x: max(0.0, float(x)))
        df["savings_balance"] = pd.to_numeric(df["savings_balance"], errors="coerce").fillna(0.0).apply(lambda x: max(0.0, float(x)))

        # Join with income to re-verify savings_rate
        inc_map = df_income.set_index("customer_id")["monthly_income"].to_dict()
        exp_map = df_expenses.set_index("customer_id")["total_monthly_expense"].to_dict()

        monthly_inc_series = df["customer_id"].map(inc_map).fillna(1.0)
        total_exp_series = df["customer_id"].map(exp_map).fillna(1.0)

        # Recalculate savings_rate
        df["savings_rate"] = np.round(df["monthly_savings"] / np.maximum(monthly_inc_series, 1.0), 4)

        # Recalculate emergency_fund_status based on savings_balance / total_monthly_expense
        months_covered = df["savings_balance"] / np.maximum(total_exp_series, 1.0)

        statuses = []
        for m in months_covered:
            if pd.isna(m):
                statuses.append("No Fund")
            elif m >= 6.0:
                statuses.append("Fully Funded")
            elif m >= 3.0:
                statuses.append("Partially Funded")
            elif m >= 1.0:
                statuses.append("Low")
            else:
                statuses.append("No Fund")

        df["emergency_fund_status"] = statuses
        df["emergency_fund_status"] = df["emergency_fund_status"].fillna("No Fund")
        return df

    def clean_debt(self, df: pd.DataFrame, df_income: pd.DataFrame) -> pd.DataFrame:
        """Cleans DEBT table and recalculates totals and DTI ratios."""
        logger.info("Cleaning DEBT table...")
        df = self._standardize_columns(df)

        df = df.drop_duplicates(subset=["customer_id"]).reset_index(drop=True)

        debt_cols = ["credit_card_debt", "personal_loan", "education_loan", "vehicle_loan", "mortgage"]
        for col in debt_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0).apply(lambda x: max(0.0, float(x)))

        # Recalculate total_debt
        df["total_debt"] = np.round(df[debt_cols].sum(axis=1), 2)

        # Recalculate debt_to_income_ratio
        inc_map = df_income.set_index("customer_id")["monthly_income"].to_dict()
        monthly_inc = df["customer_id"].map(inc_map).fillna(1.0)
        est_monthly_payment = df["total_debt"] * 0.012
        df["debt_to_income_ratio"] = np.round(np.minimum(2.5, est_monthly_payment / np.maximum(monthly_inc, 1.0)), 4)

        return df

    def clean_credit(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans CREDIT table and enforces score ranges and categories."""
        logger.info("Cleaning CREDIT table...")
        df = self._standardize_columns(df)

        df = df.drop_duplicates(subset=["customer_id"]).reset_index(drop=True)

        df["credit_score"] = pd.to_numeric(df["credit_score"], errors="coerce").fillna(650).astype(int)
        df["credit_score"] = df["credit_score"].clip(lower=300, upper=850)

        df["missed_payments"] = pd.to_numeric(df["missed_payments"], errors="coerce").fillna(0).astype(int).clip(lower=0)
        df["credit_utilization"] = pd.to_numeric(df["credit_utilization"], errors="coerce").fillna(0.3).astype(float).clip(0.0, 1.0)

        # Recalculate risk category
        risk_cats = []
        for score in df["credit_score"]:
            if score >= 750:
                risk_cats.append("Low Risk")
            elif score >= 670:
                risk_cats.append("Medium Risk")
            elif score >= 580:
                risk_cats.append("High Risk")
            else:
                risk_cats.append("Very High Risk")
        df["credit_risk_category"] = risk_cats

        df["payment_behavior"] = df["payment_behavior"].astype(str).str.strip().str.title()
        df = df.drop_duplicates(subset=["credit_id"]).reset_index(drop=True)
        return df

    def clean_transactions(self, df: pd.DataFrame, valid_customer_ids: set) -> pd.DataFrame:
        """Cleans TRANSACTIONS log table, deduplicates, and filters orphaned keys."""
        logger.info("Cleaning TRANSACTIONS table...")
        df = self._standardize_columns(df)

        # Filter orphaned customer IDs
        initial_len = len(df)
        df = df[df["customer_id"].isin(valid_customer_ids)].copy()
        if len(df) < initial_len:
            logger.info(f"Filtered out {initial_len - len(df)} transactions with invalid customer_id.")

        # Deduplicate
        df = df.drop_duplicates(subset=["transaction_id"]).reset_index(drop=True)

        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(1.0).apply(lambda x: max(0.01, float(x)))
        df["amount"] = np.round(df["amount"], 2)

        # Impute missing merchant_type
        df["merchant_type"] = df["merchant_type"].fillna("General Merchant").astype(str).str.strip().str.title()

        df["transaction_type"] = df["transaction_type"].astype(str).str.strip().str.title()
        df["category"] = df["category"].astype(str).str.strip().str.title()
        df["payment_method"] = df["payment_method"].astype(str).str.strip().str.title()

        # Format dates
        df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce").dt.strftime("%Y-%m-%d %H:%M:%S")

        return df

    def clean_financial_products(self, df: pd.DataFrame, valid_customer_ids: set) -> pd.DataFrame:
        """Cleans FINANCIAL_PRODUCTS entity table."""
        logger.info("Cleaning FINANCIAL_PRODUCTS table...")
        df = self._standardize_columns(df)

        df = df[df["customer_id"].isin(valid_customer_ids)].copy()
        df = df.drop_duplicates(subset=["product_id"]).reset_index(drop=True)

        df["product_type"] = df["product_type"].astype(str).str.strip().str.title()
        df["product_status"] = df["product_status"].astype(str).str.strip().str.title()
        df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce").dt.strftime("%Y-%m-%d")

        return df

    def clean_all(self, raw_dir: Path = None, processed_dir: Path = None) -> Dict[str, pd.DataFrame]:
        """
        Executes full data cleaning pipeline from raw CSVs and outputs processed CSVs.
        """
        raw_dir = raw_dir or self.config.raw_data_dir
        processed_dir = processed_dir or self.config.processed_data_dir
        processed_dir.mkdir(parents=True, exist_ok=True)

        logger.info("Starting end-to-end data cleaning pipeline...")

        # Load raw files
        raw_cust = pd.read_csv(raw_dir / "customers.csv")
        raw_inc = pd.read_csv(raw_dir / "income.csv")
        raw_exp = pd.read_csv(raw_dir / "expenses.csv")
        raw_sav = pd.read_csv(raw_dir / "savings.csv")
        raw_debt = pd.read_csv(raw_dir / "debt.csv")
        raw_cred = pd.read_csv(raw_dir / "credit.csv")
        raw_txn = pd.read_csv(raw_dir / "transactions.csv")
        raw_prod = pd.read_csv(raw_dir / "financial_products.csv")

        # Clean in dependency order
        clean_cust = self.clean_customers(raw_cust)
        valid_cust_ids = set(clean_cust["customer_id"].unique())

        clean_inc = self.clean_income(raw_inc)
        clean_exp = self.clean_expenses(raw_exp)
        clean_sav = self.clean_savings(raw_sav, clean_inc, clean_exp)
        clean_debt = self.clean_debt(raw_debt, clean_inc)
        clean_cred = self.clean_credit(raw_cred)
        clean_txn = self.clean_transactions(raw_txn, valid_cust_ids)
        clean_prod = self.clean_financial_products(raw_prod, valid_cust_ids)

        processed_dict = {
            "customers": clean_cust,
            "income": clean_inc,
            "expenses": clean_exp,
            "savings": clean_sav,
            "debt": clean_debt,
            "credit": clean_cred,
            "transactions": clean_txn,
            "financial_products": clean_prod
        }

        # Save processed CSVs
        for name, df in processed_dict.items():
            filepath = processed_dir / f"{name}.csv"
            df.to_csv(filepath, index=False)
            logger.info(f"Saved processed {name}.csv with {len(df)} rows.")

        return processed_dict


if __name__ == "__main__":
    cleaner = DataCleaner()
    cleaner.clean_all()
