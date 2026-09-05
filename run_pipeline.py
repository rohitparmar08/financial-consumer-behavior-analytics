"""
End-to-End Orchestrator Pipeline for Financial Consumer Behavior Analytics.

Usage:
  python run_pipeline.py --all
  python run_pipeline.py --generate
  python run_pipeline.py --clean
  python run_pipeline.py --validate
  python run_pipeline.py --db
  python run_pipeline.py --query
  python run_pipeline.py --analytics
  python run_pipeline.py --export
"""

import argparse
import sys
import sqlite3
from pathlib import Path

from src.config import Config
from src.utils.logger import setup_logger
from src.data_generation.generator import SyntheticDataGenerator
from src.data_cleaning.cleaner import DataCleaner
from src.validation.validator import DataValidator, DataValidationError
from src.database.db_loader import DatabaseLoader
from src.database.run_sql_analysis import SQLAnalysisRunner

logger = setup_logger("pipeline_orchestrator")


def run_data_generation(config: Config):
    """Stage 1: Generate Synthetic Data."""
    logger.info("=== STAGE 1: SYNTHETIC DATA GENERATION ===")
    generator = SyntheticDataGenerator(config=config)
    generator.generate_all()
    logger.info("Stage 1 completed successfully.")


def run_data_cleaning(config: Config):
    """Stage 2: Clean and Standardize Data."""
    logger.info("=== STAGE 2: DATA CLEANING & TRANSFORMATION ===")
    cleaner = DataCleaner(config=config)
    cleaner.clean_all()
    logger.info("Stage 2 completed successfully.")


def run_data_validation(config: Config):
    """Stage 3: Data Quality & Referential Integrity Validation."""
    logger.info("=== STAGE 3: DATA QUALITY VALIDATION ===")
    cleaner = DataCleaner(config=config)
    processed_data = cleaner.clean_all()

    validator = DataValidator(config=config)
    is_valid, errors = validator.validate_all(processed_data)

    if not is_valid:
        raise DataValidationError(f"Pipeline halted due to {len(errors)} validation errors.")
    logger.info("Stage 3 completed successfully.")


def run_database_loading(config: Config):
    """Stage 4: Build SQLite Database & Ingest Processed Data."""
    logger.info("=== STAGE 4: SQLITE DATABASE INGESTION ===")
    loader = DatabaseLoader(config=config)
    counts = loader.setup_and_load()
    logger.info(f"Loaded records across tables: {counts}")
    logger.info("Stage 4 completed successfully.")


def run_sql_validation_queries(config: Config):
    """Stage 5: Execute Initial SQL Integrity Verification Queries."""
    logger.info("=== STAGE 5: SQL VALIDATION QUERIES ===")
    sql_file = config.sql_analysis_dir / "01_initial_validation_queries.sql"
    if not sql_file.exists():
        logger.error(f"SQL analysis script not found at {sql_file}")
        return

    with open(sql_file, "r", encoding="utf-8") as f:
        sql_content = f.read()

    queries = [q.strip() for q in sql_content.split(";") if q.strip() and not q.strip().startswith("--")]

    conn = sqlite3.connect(config.database_path)
    try:
        cursor = conn.cursor()
        for idx, query in enumerate(queries, start=1):
            logger.info(f"\n--- Query #{idx} ---")
            cursor.execute(query)
            rows = cursor.fetchall()
            col_names = [description[0] for description in cursor.description] if cursor.description else []

            if col_names:
                logger.info(" | ".join(col_names))
                logger.info("-" * 60)
            for row in rows[:10]:
                logger.info(" | ".join(str(val) for val in row))
            if len(rows) > 10:
                logger.info(f"... ({len(rows) - 10} more rows)")
        logger.info("Stage 5 SQL queries executed successfully.")
    finally:
        conn.close()


def run_sql_analytics_and_views(config: Config):
    """Stage 6: Deploy Analytical SQL Views & Execute Analytical Query Suite."""
    logger.info("=== STAGE 6: SQL ANALYTICAL VIEWS & QUERIES ===")
    runner = SQLAnalysisRunner(config=config)
    conn = runner.get_connection()
    try:
        runner.deploy_views(conn)
        runner.execute_analysis_scripts(conn)
        logger.info("Stage 6 analytical views & query suite completed successfully.")
    finally:
        conn.close()


from src.database.export_powerbi_tables import PowerBIExporter

def run_data_exports(config: Config):
    """Stage 7: Generate Analytical CSV Exports and Power BI Star Schema Tables."""
    logger.info("=== STAGE 7: POWER BI ANALYTICAL DATA EXPORTS ===")
    runner = SQLAnalysisRunner(config=config)
    conn = runner.get_connection()
    try:
        counts = runner.export_analytical_tables(conn)
        logger.info(f"Stage 7 analytical exports generated: {counts}")
        
        pbi_exporter = PowerBIExporter(config=config)
        pbi_counts = pbi_exporter.export_all()
        logger.info(f"Stage 7 Power BI star-schema exports generated: {pbi_counts}")
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Financial / Consumer Behavior Analytics Pipeline")
    parser.add_argument("--all", action="store_true", help="Run full end-to-end pipeline")
    parser.add_argument("--generate", action="store_true", help="Run synthetic data generation")
    parser.add_argument("--clean", action="store_true", help="Run data cleaning pipeline")
    parser.add_argument("--validate", action="store_true", help="Run data validation checks")
    parser.add_argument("--db", action="store_true", help="Build SQLite database and load data")
    parser.add_argument("--query", action="store_true", help="Execute SQL validation queries")
    parser.add_argument("--analytics", action="store_true", help="Deploy SQL analytical views & run analysis")
    parser.add_argument("--export", action="store_true", help="Export analytical datasets to data/exports/*.csv")

    args = parser.parse_args()
    config = Config()
    config.ensure_directories()

    # If no flags passed, default to --all
    if not any([args.all, args.generate, args.clean, args.validate, args.db, args.query, args.analytics, args.export]):
        args.all = True

    try:
        if args.all or args.generate:
            run_data_generation(config)
        if args.all or args.clean:
            run_data_cleaning(config)
        if args.all or args.validate:
            run_data_validation(config)
        if args.all or args.db:
            run_database_loading(config)
        if args.all or args.query:
            run_sql_validation_queries(config)
        if args.all or args.analytics:
            run_sql_analytics_and_views(config)
        if args.all or args.export:
            run_data_exports(config)

        logger.info("\n[COMPLETED] PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")

    except Exception as e:
        logger.exception(f"Pipeline execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
