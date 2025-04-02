"""
Test script for Google Ad Manager campaign management.
"""
import logging
from datetime import datetime

from mcp_tools.campaign_management import (
    get_ad_manager_client,
    create_order,
    create_line_item,
    create_creative
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Test campaign management functionality."""
    try:
        # Initialize client
        logger.info("Initializing Ad Manager client...")
        client = get_ad_manager_client()

        # Generate a unique order name using timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        order_name = f"Test_Order_{timestamp}"

        # Create order
        logger.info(f"Creating order '{order_name}'...")
        order = create_order(client, order_name)
        logger.info(f"Created order with ID: {order['id']}")

        # Create line item
        logger.info("Creating line item...")
        line_item = create_line_item(client, order['id'])
        logger.info(f"Created line item with ID: {line_item['id']}")

        # Create creative
        logger.info("Creating creative...")
        creative = create_creative(client, order['advertiserId'])
        logger.info(f"Created creative with ID: {creative['id']}")

        logger.info("Test completed successfully!")

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main() 