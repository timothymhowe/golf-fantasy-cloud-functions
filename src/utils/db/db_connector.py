from google.cloud.sql.connector import Connector
from google.cloud import firestore
import sqlalchemy
import os
import logging
from typing import Any, Dict
from dotenv import load_dotenv

# Set up logging
logger = logging.getLogger(__name__)

load_dotenv()

def clean_env(var_name: str, default: str = None) -> str:
    """Clean environment variable values"""
    value = os.getenv(var_name, default)
    return value.strip('"').strip("'").strip() if value else None

def get_db_config() -> Dict[str, str]:
    """Get database configuration from environment"""
    return {
        'user': clean_env('DB_USER'),
        'password': clean_env('DB_PASS'),
        'database': clean_env('DB_NAME'),
        'instance_connection_string': clean_env('INSTANCE_CONNECTION_STRING_FULL')
    }

# Initialize connectors
sql_connector = Connector()
firestore_db = firestore.Client()

def get_db_connection() -> Any:
    """Get SQLAlchemy database engine"""
    try:
        config = get_db_config()
        engine = sqlalchemy.create_engine(
            "mysql+pymysql://",
            creator=lambda: sql_connector.connect(
                config['instance_connection_string'],
                "pymysql",
                user=config['user'],
                password=config['password'],
                db=config['database']
            ),
            pool_size=5,
            max_overflow=2,
            pool_timeout=30,
            pool_recycle=1800
        )
        return engine
    except Exception as e:
        logger.error(f"Error creating database connection: {e}")
        raise

def cleanup():
    """Cleanup database connections"""
    try:
        sql_connector.close()
    except Exception as e:
        logger.error(f"Error cleaning up SQL connection: {e}")