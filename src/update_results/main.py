"""
Tournament Results Update Controller

Cloud Function that coordinates updating tournament results:
1. Gets tournament results from SportContent API
2. Updates SQL database with results
3. Handles special cases (TOUR Championship, team events)
"""

import functions_framework
from datetime import datetime
import logging
from typing import Dict, Any, Tuple
from utils.db import get_db_connection
from .api_client import fetch_tournament_results
from .db_client import update_tournament_results

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_tournament_results_data() -> Tuple[Dict[str, Any], int]:
    """Main function to coordinate tournament results update"""
    try:
        # Get database session
        session = get_db_connection()
        if not session:
            return {"error": "Could not connect to database"}, 500

        # Get tournament results from API
        results = fetch_tournament_results(tournament_id)
        if not results:
            return {"error": "Could not fetch tournament results"}, 500

        # Update database with results
        success = update_tournament_results(session, tournament_id, results)
        if not success:
            return {"error": "Failed to update tournament results"}, 500

        return {"message": "Tournament results updated successfully"}, 200

    except Exception as e:
        logger.error(f"Error updating tournament results: {e}")
        return {"error": str(e)}, 500

@functions_framework.http
def update_tournament_results(request) -> Tuple[Dict[str, Any], int]:
    """Cloud Function entry point for updating tournament results"""
    response, status_code = update_tournament_results_data()
    return response, status_code
