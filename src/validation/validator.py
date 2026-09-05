"""
Data Quality Validation Engine for Financial Consumer Behavior Analytics.
Enforces schema validation, referential integrity, range bounds, and business rules.
"""

from pathlib import Path
import pandas as pd
from typing import Dict, List, Tuple

from src.config import Config
from src.utils.logger import setup_logger

logger = setup_logger("validation")


class DataValidationError(Exception):
    """Exception raised when critical data validation rules fail."""
    pass


class DataValidator:
    """
    Validates data quality, completeness, referential integrity, and business logic constraints.
    """

    def __init__(self, config: Config = None):
        self.config = config or Config()

    def validate_uniqueness(self, df: pd.DataFrame, key_column: str, table_name: str) -> List[str]:
        """Verifies that primary key column has unique non-null values."""
        errors = []
        if key_column not in df.columns:
            errors.append(f"Table '{table_name}' missing primary key column '{key_column}'.")
            return errors

        if df[key_column].isnull().any():
            errors.append(f"Table '{table_name}' contains NULL values in primary key '{key_column}'.")

        duplicates = df[key_column].duplicated().sum()
        if duplicates > 0:
            errors.append(f"Table '{table_name}' contains {duplicates} duplicate primary key values in '{key_column}'.")

        return errors

    def validate_referential_integrity(self, parent_df: pd.DataFrame, child_df: pd.DataFrame, parent_key: str, child_key: str, child_table_name: str) -> List[str]:
        """Verifies that all foreign key references exist in parent table."""
        errors = []
        parent_keys = set(parent_df[parent_key].unique())
        child_keys = set(child_df[child_key].unique())

        orphans = child_keys - parent_keys
        if orphans:
            errors.append(f"Referential integrity failure: '{child_table_name}.{child_key}' contains {len(orphans)} orphaned keys not in parent table.")

        return errors

    def validate_range_bounds(self, df: pd.DataFrame, column: str, min_val: float = None, max_val: float = None, table_name: str = "") -> List[str]:
        """Validates numerical range bounds."""
        errors = []
        if column not in df.columns:
            return errors

        numeric_vals = pd.to_numeric(df[column], errors="coerce")
        if numeric_vals.isnull().any():
            errors.append(f"Table '{table_name}' column '{column}' contains non-numeric values.")

        if min_val is not None:
            below_min = (numeric_vals < min_val).sum()
            if below_min > 0:
                errors.append(f"Table '{table_name}' column '{column}' has {below_min} values below minimum threshold ({min_val}).")

        if max_val is not None:
            above_max = (numeric_vals > max_val).sum()
            if above_max > 0:
                errors.append(f"Table '{table_name}' column '{column}' has {above_max} values above maximum threshold ({max_val}).")

        return errors

    def validate_customers(self, df: pd.DataFrame) -> List[str]:
        """Validates CUSTOMERS table."""
        errors = self.validate_uniqueness(df, "customer_id", "customers")
        errors.extend(self.validate_range_bounds(df, "age", min_val=18, max_val=100, table_name="customers"))

        valid_genders = {"Male", "Female", "Non-Binary"}
        invalid_genders = set(df["gender"].unique()) - valid_genders
        if invalid_genders:
            errors.append(f"CUSTOMERS table contains invalid gender values: {invalid_genders}")

        return errors

    def validate_income(self, df: pd.DataFrame) -> List[str]:
        """Validates INCOME table."""
        errors = self.validate_uniqueness(df, "income_id", "income")
        errors.extend(self.validate_range_bounds(df, "monthly_income", min_val=0.01, table_name="income"))
        errors.extend(self.validate_range_bounds(df, "annual_income", min_val=0.12, table_name="income"))
        return errors

    def validate_expenses(self, df: pd.DataFrame) -> List[str]:
        """Validates EXPENSES table."""
        errors = self.validate_uniqueness(df, "expense_id", "expenses")
        errors.extend(self.validate_range_bounds(df, "total_monthly_expense", min_val=0.0, table_name="expenses"))
        return errors

    def validate_savings(self, df: pd.DataFrame) -> List[str]:
        """Validates SAVINGS table."""
        errors = self.validate_uniqueness(df, "savings_id", "savings")
        errors.extend(self.validate_range_bounds(df, "monthly_savings", min_val=0.0, table_name="savings"))
        errors.extend(self.validate_range_bounds(df, "savings_balance", min_val=0.0, table_name="savings"))
        errors.extend(self.validate_range_bounds(df, "savings_rate", min_val=0.0, max_val=1.0, table_name="savings"))
        return errors

    def validate_debt(self, df: pd.DataFrame) -> List[str]:
        """Validates DEBT table."""
        errors = self.validate_uniqueness(df, "debt_id", "debt")
        errors.extend(self.validate_range_bounds(df, "total_debt", min_val=0.0, table_name="debt"))
        errors.extend(self.validate_range_bounds(df, "debt_to_income_ratio", min_val=0.0, max_val=5.0, table_name="debt"))
        return errors

    def validate_credit(self, df: pd.DataFrame) -> List[str]:
        """Validates CREDIT table."""
        errors = self.validate_uniqueness(df, "credit_id", "credit")
        errors.extend(self.validate_range_bounds(df, "credit_score", min_val=300, max_val=850, table_name="credit"))
        errors.extend(self.validate_range_bounds(df, "credit_utilization", min_val=0.0, max_val=1.0, table_name="credit"))
        return errors

    def validate_transactions(self, df: pd.DataFrame) -> List[str]:
        """Validates TRANSACTIONS table."""
        errors = self.validate_uniqueness(df, "transaction_id", "transactions")
        errors.extend(self.validate_range_bounds(df, "amount", min_val=0.01, table_name="transactions"))
        return errors

    def validate_financial_products(self, df: pd.DataFrame) -> List[str]:
        """Validates FINANCIAL_PRODUCTS table."""
        errors = self.validate_uniqueness(df, "product_id", "financial_products")
        return errors

    def validate_all(self, data_dict: Dict[str, pd.DataFrame]) -> Tuple[bool, List[str]]:
        """
        Runs comprehensive data quality validation across all entity tables.
        """
        logger.info("Executing comprehensive data quality validation checks...")
        all_errors = []

        # 1. Individual Table Validations
        all_errors.extend(self.validate_customers(data_dict["customers"]))
        all_errors.extend(self.validate_income(data_dict["income"]))
        all_errors.extend(self.validate_expenses(data_dict["expenses"]))
        all_errors.extend(self.validate_savings(data_dict["savings"]))
        all_errors.extend(self.validate_debt(data_dict["debt"]))
        all_errors.extend(self.validate_credit(data_dict["credit"]))
        all_errors.extend(self.validate_transactions(data_dict["transactions"]))
        all_errors.extend(self.validate_financial_products(data_dict["financial_products"]))

        # 2. Referential Integrity Checks
        parent_cust = data_dict["customers"]
        child_tables = ["income", "expenses", "savings", "debt", "credit", "transactions", "financial_products"]
        for child in child_tables:
            all_errors.extend(self.validate_referential_integrity(
                parent_df=parent_cust,
                child_df=data_dict[child],
                parent_key="customer_id",
                child_key="customer_id",
                child_table_name=child
            ))

        # 3. Minimum Expected Row Counts Check
        num_cust = len(data_dict["customers"])
        if num_cust < 1000:
            all_errors.append(f"Unexpectedly low customer record count ({num_cust}). Expected >= 1000.")

        is_valid = len(all_errors) == 0
        if is_valid:
            logger.info("[SUCCESS] All data quality and referential integrity validations passed successfully!")
        else:
            logger.error(f"[ERROR] Data validation failed with {len(all_errors)} errors:")
            for err in all_errors:
                logger.error(f"  - {err}")

        return is_valid, all_errors


if __name__ == "__main__":
    from src.data_cleaning.cleaner import DataCleaner
    cleaner = DataCleaner()
    processed_data = cleaner.clean_all()

    validator = DataValidator()
    valid, errs = validator.validate_all(processed_data)
