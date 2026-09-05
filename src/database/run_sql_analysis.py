"""
SQL Analysis Runner & Power BI Data Export Framework.
Executes analytical DDL views, analysis queries, and exports analytical datasets to data/exports/*.csv.
"""

from pathlib import Path
import sqlite3
import pandas as pd
from typing import Dict, List

from src.config import Config
from src.utils.logger import setup_logger

logger = setup_logger("sql_analysis_runner")


class SQLAnalysisRunner:
    """
    Deploys analytical SQL views, runs analytical query suites, and generates Power BI CSV exports.
    """

    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.db_path = self.config.database_path
        self.views_dir = self.config.sql_schema_dir.parent / "views"
        self.analysis_dir = self.config.sql_analysis_dir
        self.exports_dir = self.config.exports_dir

    def get_connection(self) -> sqlite3.Connection:
        """Connects to SQLite database with foreign keys enabled."""
        if not self.db_path.exists():
            raise FileNotFoundError(f"SQLite database not found at {self.db_path}. Build database first.")
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def deploy_views(self, conn: sqlite3.Connection) -> List[str]:
        """Deploys all SQL views from sql/views/ in order."""
        logger.info(f"Deploying analytical SQL views from {self.views_dir}...")
        if not self.views_dir.exists():
            raise FileNotFoundError(f"Views directory not found at {self.views_dir}")

        view_files = sorted(list(self.views_dir.glob("*.sql")))
        deployed = []

        cursor = conn.cursor()
        for v_file in view_files:
            logger.info(f"Deploying view file: {v_file.name}...")
            with open(v_file, "r", encoding="utf-8") as f:
                sql_script = f.read()
            cursor.executescript(sql_script)
            conn.commit()
            deployed.append(v_file.name)

        logger.info(f"[SUCCESS] Deployed {len(deployed)} analytical views.")
        return deployed

    def execute_analysis_scripts(self, conn: sqlite3.Connection) -> List[str]:
        """Executes all analysis SQL scripts from sql/analysis/."""
        logger.info(f"Executing analytical SQL scripts from {self.analysis_dir}...")
        if not self.analysis_dir.exists():
            raise FileNotFoundError(f"Analysis directory not found at {self.analysis_dir}")

        analysis_files = sorted(list(self.analysis_dir.glob("*.sql")))
        executed = []

        cursor = conn.cursor()
        for a_file in analysis_files:
            logger.info(f"Running analysis script: {a_file.name}...")
            with open(a_file, "r", encoding="utf-8") as f:
                sql_script = f.read()

            queries = [q.strip() for q in sql_script.split(";") if q.strip() and not q.strip().startswith("--")]
            for idx, q in enumerate(queries, start=1):
                try:
                    cursor.execute(q)
                except Exception as e:
                    logger.error(f"Error in {a_file.name} query #{idx}: {e}")
                    raise e
            executed.append(a_file.name)

        logger.info(f"[SUCCESS] Executed {len(executed)} analysis scripts.")
        return executed

    def export_analytical_tables(self, conn: sqlite3.Connection) -> Dict[str, int]:
        """Exports key analytical views to CSV files under data/exports/."""
        self.exports_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Exporting analytical datasets to {self.exports_dir}...")

        export_mapping = {
            "vw_customer_financial_profile": "customer_financial_profile.csv",
            "vw_customer_segments": "customer_segments.csv",
            "vw_rfm_segments": "rfm_segments.csv",
            "vw_monthly_transaction_summary": "monthly_transaction_summary.csv",
            "vw_product_adoption_summary": "product_adoption_summary.csv",
            "vw_financial_risk_summary": "financial_risk_summary.csv"
        }

        export_counts = {}
        for view_name, csv_filename in export_mapping.items():
            out_path = self.exports_dir / csv_filename
            df = pd.read_sql_query(f"SELECT * FROM {view_name};", conn)
            df.to_csv(out_path, index=False)
            export_counts[csv_filename] = len(df)
            logger.info(f"Exported {csv_filename} ({len(df):,} rows, {len(df.columns)} columns).")

        return export_counts

    def run_all(self) -> Dict[str, Any]:
        """Full execution workflow: deploy views, run analysis, export CSVs."""
        conn = self.get_connection()
        try:
            views = self.deploy_views(conn)
            scripts = self.execute_analysis_scripts(conn)
            exports = self.export_analytical_tables(conn)
            logger.info("[SUCCESS] Full SQL analytics workflow completed successfully.")
            return {
                "views_deployed": views,
                "scripts_executed": scripts,
                "exports_created": exports
            }
        finally:
            conn.close()


if __name__ == "__main__":
    runner = SQLAnalysisRunner()
    runner.run_all()
