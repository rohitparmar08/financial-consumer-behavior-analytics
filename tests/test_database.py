"""
Integration tests for SQLite Database Loader.
"""
import pytest
import sqlite3
import pandas as pd
from pathlib import Path

from src.config import Config
from src.database.db_loader import DatabaseLoader


@pytest.fixture
def tmp_db_loader(tmp_path):
    cfg = Config()
    cfg.database_path = tmp_path / "test_financial.db"
    return DatabaseLoader(config=cfg)


def test_database_schema_creation_and_fk_enforcement(tmp_db_loader):
    conn = tmp_db_loader.get_connection()
    try:
        tmp_db_loader.build_schema(conn)

        # Verify tables exist
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        table_names = [t[0] for t in tables]
        assert "customers" in table_names
        assert "income" in table_names

        # Foreign Key Test: Inserting income without customer should fail
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO income VALUES ('INC-999', 'NON_EXISTENT_CUST', 1000.0, 12000.0, 'Salary', 'High');"
            )
    finally:
        conn.close()
