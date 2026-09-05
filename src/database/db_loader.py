"""
SQLite Database Loader for Financial Consumer Behavior Analytics.
Executes DDL schema creation and populates SQLite database tables from cleaned CSV files.
"""

from pathlib import Path
import sqlite3
import pandas as pd
from typing import Dict

from src.config import Config
from src.utils.logger import setup_logger

logger = setup_logger("database_loader")


class DatabaseLoader:
    """
    Manages SQLite database creation, schema deployment, and dataset ingestion.
    """

    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.db_path = self.config.database_path

    def get_connection(self) -> sqlite3.Connection:
        """Returns an active SQLite database connection with foreign keys enabled."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def execute_sql_file(self, conn: sqlite3.Connection, sql_file_path: Path):
        """Executes a SQL script file against the database connection."""
        if not sql_file_path.exists():
            raise FileNotFoundError(f"SQL file not found at {sql_file_path}")

        logger.info(f"Executing SQL script: {sql_file_path.name}...")
        with open(sql_file_path, "r", encoding="utf-8") as f:
            sql_script = f.read()

        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()

    def build_schema(self, conn: sqlite3.Connection):
        """Builds database schema and performance indexes."""
        schema_dir = self.config.sql_schema_dir
        ddl_tables = schema_dir / "01_create_tables.sql"
        ddl_indexes = schema_dir / "02_create_indexes.sql"

        self.execute_sql_file(conn, ddl_tables)
        self.execute_sql_file(conn, ddl_indexes)
        logger.info("Database schema and indexes deployed successfully.")

    def load_processed_data(self, conn: sqlite3.Connection, processed_dir: Path = None) -> Dict[str, int]:
        """
        Loads cleaned CSV data from processed directory into SQLite tables.
        """
        processed_dir = processed_dir or self.config.processed_data_dir
        logger.info(f"Loading cleaned CSV files from {processed_dir} into SQLite database...")

        # Ingestion order: parent entity 'customers' first
        tables_in_order = [
            "customers", "income", "expenses",
            "savings", "debt", "credit",
            "transactions", "financial_products"
        ]

        row_counts = {}

        for table in tables_in_order:
            csv_path = processed_dir / f"{table}.csv"
            if not csv_path.exists():
                logger.warning(f"CSV file for table '{table}' not found at {csv_path}. Skipping.")
                continue

            df = pd.read_csv(csv_path)

            # Clear existing data in table
            conn.execute(f"DELETE FROM {table};")
            conn.commit()

            # Append new clean data
            df.to_sql(table, conn, if_exists="append", index=False)
            conn.commit()

            count = conn.execute(f"SELECT COUNT(*) FROM {table};").fetchone()[0]
            row_counts[table] = count
            logger.info(f"Loaded {count:,} rows into table '{table}'.")

        return row_counts

    def setup_and_load(self, processed_dir: Path = None) -> Dict[str, int]:
        """
        Full database setup workflow: connect, build schema, and ingest data.
        """
        conn = self.get_connection()
        try:
            self.build_schema(conn)
            counts = self.load_processed_data(conn, processed_dir)
            logger.info(f"[SUCCESS] SQLite database setup completed at: {self.db_path}")
            return counts
        finally:
            conn.close()


if __name__ == "__main__":
    loader = DatabaseLoader()
    loader.setup_and_load()
