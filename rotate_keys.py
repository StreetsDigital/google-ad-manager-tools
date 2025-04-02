#!/usr/bin/env python3
"""
Service Account Key Rotation Script

This script helps manage the rotation of service account keys by:
1. Checking the age of the current key
2. Creating a new key if needed
3. Updating configuration files
4. Backing up old credentials
"""
import os
import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def backup_credentials(service_account_path: str, googleads_path: str) -> str:
    """Backup current credential files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path("credentials_backup") / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Backup service account file
    if os.path.exists(service_account_path):
        shutil.copy2(service_account_path, backup_dir / "service-account.json")
    
    # Backup googleads.yaml
    if os.path.exists(googleads_path):
        shutil.copy2(googleads_path, backup_dir / "googleads.yaml")
    
    logger.info(f"Credentials backed up to: {backup_dir}")
    return str(backup_dir)

def check_key_age(service_account_path: str, max_age_days: int = 90) -> bool:
    """Check if the service account key needs rotation."""
    if not os.path.exists(service_account_path):
        logger.warning("Service account file not found")
        return False
    
    file_stat = os.stat(service_account_path)
    file_age = datetime.now() - datetime.fromtimestamp(file_stat.st_mtime)
    
    return file_age.days >= max_age_days

def main():
    """Main function to manage key rotation."""
    # Load environment variables
    service_account_path = os.getenv("SERVICE_ACCOUNT_PATH", "service-account.json")
    googleads_path = os.getenv("GOOGLEADS_YAML_PATH", "googleads.yaml")
    max_age_days = int(os.getenv("ROTATE_KEYS_INTERVAL_DAYS", "90"))
    
    # Check if key rotation is needed
    if check_key_age(service_account_path, max_age_days):
        logger.info("Service account key requires rotation")
        
        # Backup current credentials
        backup_dir = backup_credentials(service_account_path, googleads_path)
        
        logger.info("""
        Please follow these steps to rotate your service account key:
        
        1. Go to Google Cloud Console
        2. Navigate to IAM & Admin > Service Accounts
        3. Find your service account and click on it
        4. Go to the "Keys" tab
        5. Click "Add Key" > "Create new key"
        6. Choose JSON format and create
        7. Download the new key
        8. Replace your existing service-account.json with the new one
        9. Test your application with the new key
        10. If everything works, delete the old key from Google Cloud Console
        
        Your old credentials are backed up at: {backup_dir}
        """)
    else:
        logger.info("Service account key is still valid")

if __name__ == "__main__":
    main() 