"""
Configuration persistence with default backup functionality.
Stores configuration in PostgreSQL with support for saving/restoring defaults.
"""
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
import psycopg2
from psycopg2.extras import Json
from config.runtime_config import DEFAULT_CONFIG, get, set_config, all_config

# Database connection parameters
DB_PARAMS = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "database": os.getenv("POSTGRES_DATABASE", "xavigate"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres")
}

def get_db_connection():
    """Get a database connection."""
    return psycopg2.connect(**DB_PARAMS)

def init_config_tables():
    """Initialize configuration tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Create runtime_config table for current configuration
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS runtime_config (
                id SERIAL PRIMARY KEY,
                config_data JSONB NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_by VARCHAR(255)
            )
        """)
        
        # Create config_backups table for storing defaults and backups
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS config_backups (
                id SERIAL PRIMARY KEY,
                backup_name VARCHAR(255) NOT NULL,
                config_data JSONB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by VARCHAR(255),
                is_default BOOLEAN DEFAULT FALSE,
                description TEXT
            )
        """)
        
        # Create index on backup_name for faster lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_config_backups_name 
            ON config_backups(backup_name)
        """)
        
        conn.commit()
        
        # Check if we have a current config, if not, insert defaults
        cursor.execute("SELECT COUNT(*) FROM runtime_config")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Insert default configuration
            cursor.execute("""
                INSERT INTO runtime_config (config_data, updated_by)
                VALUES (%s, %s)
            """, (Json(DEFAULT_CONFIG), 'system'))
            
            # Also save as the original default backup
            cursor.execute("""
                INSERT INTO config_backups (backup_name, config_data, created_by, is_default, description)
                VALUES (%s, %s, %s, %s, %s)
            """, ('original_defaults', Json(DEFAULT_CONFIG), 'system', True, 
                  'Original system default configuration'))
            
            conn.commit()
            
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def load_config_from_db():
    """Load configuration from database into runtime config."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get the most recent configuration
        cursor.execute("""
            SELECT config_data 
            FROM runtime_config 
            ORDER BY updated_at DESC 
            LIMIT 1
        """)
        
        result = cursor.fetchone()
        if result:
            config_data = result[0]
            # Update runtime config with database values
            for key, value in config_data.items():
                set_config(key, value)
            return True
        return False
        
    finally:
        cursor.close()
        conn.close()

def save_config_to_db(user_id: Optional[str] = None):
    """Save current runtime configuration to database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get current config
        current_config = all_config()
        
        # Check if we have existing config
        cursor.execute("SELECT id FROM runtime_config ORDER BY updated_at DESC LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            # Update existing config
            cursor.execute("""
                UPDATE runtime_config 
                SET config_data = %s, 
                    updated_at = CURRENT_TIMESTAMP,
                    updated_by = %s
                WHERE id = %s
            """, (Json(current_config), user_id or 'unknown', result[0]))
        else:
            # Insert new config
            cursor.execute("""
                INSERT INTO runtime_config (config_data, updated_by)
                VALUES (%s, %s)
            """, (Json(current_config), user_id or 'unknown'))
        
        conn.commit()
        return True
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def create_config_backup(backup_name: str, description: str = None, user_id: str = None):
    """Create a backup of the current configuration."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get current config
        current_config = all_config()
        
        # Save as backup
        cursor.execute("""
            INSERT INTO config_backups (backup_name, config_data, created_by, description)
            VALUES (%s, %s, %s, %s)
        """, (backup_name, Json(current_config), user_id or 'unknown', description))
        
        conn.commit()
        return True
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def restore_config_backup(backup_name: str, user_id: str = None):
    """Restore configuration from a backup."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get the backup
        cursor.execute("""
            SELECT config_data 
            FROM config_backups 
            WHERE backup_name = %s 
            ORDER BY created_at DESC 
            LIMIT 1
        """, (backup_name,))
        
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Backup '{backup_name}' not found")
        
        backup_config = result[0]
        
        # Update runtime config
        for key, value in backup_config.items():
            set_config(key, value)
        
        # Save to database
        save_config_to_db(user_id)
        
        return True
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def list_config_backups():
    """List all available configuration backups."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT backup_name, created_at, created_by, is_default, description
            FROM config_backups
            ORDER BY created_at DESC
        """)
        
        backups = []
        for row in cursor.fetchall():
            backups.append({
                "backup_name": row[0],
                "created_at": row[1].isoformat() if row[1] else None,
                "created_by": row[2],
                "is_default": row[3],
                "description": row[4]
            })
        
        return backups
        
    finally:
        cursor.close()
        conn.close()

def get_config_history(limit: int = 10):
    """Get configuration change history."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT config_data, updated_at, updated_by
            FROM runtime_config
            ORDER BY updated_at DESC
            LIMIT %s
        """, (limit,))
        
        history = []
        for row in cursor.fetchall():
            history.append({
                "config_data": row[0],
                "updated_at": row[1].isoformat() if row[1] else None,
                "updated_by": row[2]
            })
        
        return history
        
    finally:
        cursor.close()
        conn.close()

def compare_configs(config1: Dict[str, Any], config2: Dict[str, Any]) -> Dict[str, Any]:
    """Compare two configurations and return differences."""
    differences = {
        "added": {},
        "removed": {},
        "changed": {}
    }
    
    # Find added and changed keys
    for key, value in config2.items():
        if key not in config1:
            differences["added"][key] = value
        elif config1[key] != value:
            differences["changed"][key] = {
                "old": config1[key],
                "new": value
            }
    
    # Find removed keys
    for key in config1:
        if key not in config2:
            differences["removed"][key] = config1[key]
    
    return differences

# Initialize tables on module import
try:
    init_config_tables()
    # Load config from database on startup
    load_config_from_db()
except Exception as e:
    print(f"Warning: Could not initialize config persistence: {e}")
    # Continue running with in-memory config if database is not available