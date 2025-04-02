"""
Campaign management functionality for Google Ad Manager.

This module provides functions for creating and managing orders, line items,
and creatives in Google Ad Manager.
"""
import logging
import uuid
import pytz
from datetime import datetime, timedelta
from typing import Dict

from googleads import ad_manager

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set API version
API_VERSION = 'v202402'

def get_ad_manager_client() -> ad_manager.AdManagerClient:
    """Initialize and return an Ad Manager client.
    
    Returns:
        ad_manager.AdManagerClient: Initialized Ad Manager client
    """
    return ad_manager.AdManagerClient.LoadFromStorage()

def get_current_user(client: ad_manager.AdManagerClient) -> Dict:
    """Get the current user's information."""
    user_service = client.GetService('UserService', version=API_VERSION)
    return user_service.getCurrentUser()

def get_company_id(client: ad_manager.AdManagerClient, company_name: str) -> str:
    """Get company ID by name or create if not exists."""
    company_service = client.GetService('CompanyService', version=API_VERSION)
    
    statement = {
        'query': f"WHERE name = '{company_name}' AND type = 'ADVERTISER'"
    }
    
    response = company_service.getCompaniesByStatement(statement)
    
    if response and response['results']:
        return response['results'][0]['id']
    
    company = {
        'name': company_name,
        'type': 'ADVERTISER'
    }
    result = company_service.createCompanies([company])
    return result[0]['id']

def create_order(client: ad_manager.AdManagerClient, name: str) -> Dict:
    """
    Create a new order in Google Ad Manager.

    Args:
        client: The Ad Manager client instance
        name: Name of the order

    Returns:
        Dict: The created order object
    """
    order_service = client.GetService('OrderService', version=API_VERSION)
    
    current_user = get_current_user(client)
    logging.info(f"Creating order as user: {current_user['id']}")
    
    advertiser_id = get_company_id(client, "Test Advertiser")
    logging.info(f"Using advertiser ID: {advertiser_id}")

    order = {
        'name': name,
        'advertiserId': advertiser_id,
        'traffickerId': current_user['id']
    }

    return order_service.createOrders([order])[0]

def create_line_item(client: ad_manager.AdManagerClient, order_id: str) -> Dict:
    """
    Create a line item for the specified order.

    Args:
        client: The Ad Manager client instance
        order_id: The ID of the order to create the line item for

    Returns:
        The created line item object
    """
    line_item_service = client.GetService('LineItemService', version=API_VERSION)
    network_service = client.GetService('NetworkService', version=API_VERSION)
    inventory_service = client.GetService('InventoryService', version=API_VERSION)
    
    current_network = network_service.getCurrentNetwork()
    currency_code = current_network['currencyCode']
    
    statement = {'query': 'WHERE parentId IS NULL LIMIT 1'}
    response = inventory_service.getAdUnitsByStatement(statement)
    root_ad_unit = response['results'][0] if response['results'] else None
    
    if not root_ad_unit:
        raise Exception('No root ad unit found')
    
    current_user = get_current_user(client)
    logging.info(f"Creating line item as user: {current_user['id']}")
    
    start_datetime = datetime.now(pytz.UTC)
    end_datetime = start_datetime + timedelta(days=365)
    
    line_item = {
        'name': f'Test_Line_Item_{uuid.uuid4().hex[:8]}',
        'orderId': order_id,
        'targeting': {
            'inventoryTargeting': {
                'targetedAdUnits': [{
                    'adUnitId': root_ad_unit['id'],
                    'includeDescendants': True
                }]
            },
            'geoTargeting': {
                'targetedLocations': []
            }
        },
        'startDateTime': start_datetime,
        'endDateTime': end_datetime,
        'lineItemType': 'STANDARD',
        'startDateTimeType': 'IMMEDIATELY',
        'costType': 'CPM',
        'costPerUnit': {'currencyCode': currency_code, 'microAmount': 2000000},
        'creativeRotationType': 'EVEN',
        'creativePlaceholders': [
            {
                'size': {
                    'width': 300,
                    'height': 250,
                    'isAspectRatio': False
                }
            }
        ],
        'environmentType': 'BROWSER',
        'companionDeliveryOption': 'OPTIONAL',
        'allowOverbook': True,
        'skipInventoryCheck': True,
        'reserveAtCreation': True,
        'stats': {'impressionsDelivered': 0},
        'deliveryRateType': 'EVENLY',
        'roadblockingType': 'ONE_OR_MORE',
        'primaryGoal': {
            'goalType': 'LIFETIME',
            'unitType': 'IMPRESSIONS',
            'units': 100000
        }
    }

    return line_item_service.createLineItems([line_item])[0]

def create_creative(client: ad_manager.AdManagerClient, advertiser_id: str) -> Dict:
    """
    Create a creative for the specified advertiser.

    Args:
        client: The Ad Manager client instance
        advertiser_id: The ID of the advertiser to create the creative for

    Returns:
        The created creative object
    """
    creative_service = client.GetService('CreativeService', version=API_VERSION)
    
    current_user = get_current_user(client)
    logging.info(f"Creating creative as user: {current_user['id']}")
    
    creative = {
        'xsi_type': 'ThirdPartyCreative',
        'name': f'Test_Creative_{uuid.uuid4().hex[:8]}',
        'advertiserId': advertiser_id,
        'size': {'width': 300, 'height': 250},
        'snippet': '<script>console.log("Third party creative");</script>',
        'isSafeFrameCompatible': True,
        'thirdPartyImpressionTrackingUrls': [],
        'previewUrl': 'https://example.com'
    }

    return creative_service.createCreatives([creative])[0] 