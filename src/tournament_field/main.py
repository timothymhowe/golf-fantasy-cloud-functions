"""
Tournament Field Update Controller

Cloud Function that coordinates updating tournament field data:
1. Fetches upcoming tournament info
2. Gets field data from SportContent API
3. Stores field data in Firestore
4. Updates SQL database entries
"""

import functions_framework
from google.cloud import firestore
from datetime import datetime, timezone
import logging
from typing import Dict, Any, Tuple
from utils.db import get_db_connection
from .api_client import fetch_tournament_field
from .firestore_client import store_tournament_field
from .db_client import get_upcoming_tournament, update_tournament_entries

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_tournament_field_data() -> Tuple[Dict[str, Any], int]:
    """
    Main controller function for updating tournament field data.
    
    Returns:
        Tuple of (response_dict, status_code)
    """
    try:
        logger.info("Starting tournament field update")
        
        # Initialize clients
        db = firestore.Client()
        db_engine = get_db_connection()
        
        # Get active tournament
        tournament = get_upcoming_tournament(db_engine)
        if not tournament:
            return {
                'status': 'error',
                'message': 'No upcoming tournament found'
            }, 404
            
        # Fetch field data from SportContent API
        field_data = fetch_tournament_field(tournament["sportcontent_api_id"])
        if not field_data:
            return {
                'status': 'error',
                'message': 'Failed to fetch tournament field data'
            }, 500
        
        # Store in Firestore
        if not store_tournament_field(db, tournament["sportcontent_api_id"], field_data):
            return {
                'status': 'error',
                'message': 'Failed to store tournament field in Firestore'
            }, 500
        
        # Update SQL database
        if not update_tournament_entries(db_engine, tournament["id"], field_data):
            return {
                'status': 'error',
                'message': 'Failed to update tournament entries in database'
            }, 500
        
        return {
            'status': 'success',
            'message': f'Tournament field updated for {tournament["tournament_name"]}',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }, 200

    except Exception as e:
        logger.error(f"Error updating tournament field: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }, 500

@functions_framework.http
def update_tournament_field(request) -> Tuple[Dict[str, Any], int]:
    """Cloud Function entry point for updating tournament field data"""
    response, status_code = update_tournament_field_data()
    return response, status_code