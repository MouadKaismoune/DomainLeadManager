"""Application paths and settings."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "app.db"
SCHEMA_PATH = PROJECT_ROOT / "schema.sql"
APP_TITLE = "Domain Lead Manager"
APP_VERSION = "26.10"
