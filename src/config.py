"""
Centralized Configuration Loader for Financial Consumer Behavior Analytics.
"""
from pathlib import Path
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
from typing import Dict, Any

# Root project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_config(config_path: Path = None) -> Dict[str, Any]:
    """
    Loads YAML configuration or returns default settings.
    """
    if config_path is None:
        config_path = PROJECT_ROOT / "config" / "config.yaml"

    if config_path.exists() and HAS_YAML:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    else:
        # Default fallback
        config = {
            "project": {"name": "Financial Analytics", "random_seed": 42},
            "dataset": {
                "num_customers": 15000,
                "avg_transactions_per_customer": 5,
                "avg_products_per_customer": 1.8,
                "start_date": "2021-01-01",
                "end_date": "2025-12-31",
                "missing_value_rate": 0.02
            },
            "paths": {
                "raw_data_dir": "data/raw",
                "processed_data_dir": "data/processed",
                "exports_dir": "data/exports",
                "database_dir": "database",
                "database_path": "database/financial_analytics.db",
                "sql_schema_dir": "sql/schema",
                "sql_analysis_dir": "sql/analysis",
                "reports_dir": "reports"
            }
        }
    return config


class Config:
    """Convenience wrapper for configuration settings."""
    def __init__(self, config_dict: Dict[str, Any] = None):
        self._raw_config = config_dict or load_config()

        # Project
        self.project_name = self._raw_config.get("project", {}).get("name", "Financial Analytics")
        self.random_seed = self._raw_config.get("project", {}).get("random_seed", 42)

        # Dataset
        ds_cfg = self._raw_config.get("dataset", {})
        self.num_customers = ds_cfg.get("num_customers", 15000)
        self.avg_transactions_per_customer = ds_cfg.get("avg_transactions_per_customer", 5)
        self.avg_products_per_customer = ds_cfg.get("avg_products_per_customer", 1.8)
        self.start_date = ds_cfg.get("start_date", "2021-01-01")
        self.end_date = ds_cfg.get("end_date", "2025-12-31")
        self.missing_value_rate = ds_cfg.get("missing_value_rate", 0.02)

        # Paths resolved against PROJECT_ROOT
        paths_cfg = self._raw_config.get("paths", {})
        self.raw_data_dir = PROJECT_ROOT / paths_cfg.get("raw_data_dir", "data/raw")
        self.processed_data_dir = PROJECT_ROOT / paths_cfg.get("processed_data_dir", "data/processed")
        self.exports_dir = PROJECT_ROOT / paths_cfg.get("exports_dir", "data/exports")
        self.database_dir = PROJECT_ROOT / paths_cfg.get("database_dir", "database")
        self.database_path = PROJECT_ROOT / paths_cfg.get("database_path", "database/financial_analytics.db")
        self.sql_schema_dir = PROJECT_ROOT / paths_cfg.get("sql_schema_dir", "sql/schema")
        self.sql_analysis_dir = PROJECT_ROOT / paths_cfg.get("sql_analysis_dir", "sql/analysis")
        self.reports_dir = PROJECT_ROOT / paths_cfg.get("reports_dir", "reports")

    def ensure_directories(self):
        """Ensures all configured directory paths exist."""
        for path in [
            self.raw_data_dir,
            self.processed_data_dir,
            self.exports_dir,
            self.database_dir,
            self.sql_schema_dir,
            self.sql_analysis_dir,
            self.reports_dir,
        ]:
            path.mkdir(parents=True, exist_ok=True)
