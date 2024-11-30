"""
SportContent API Client

Handles fetching tournament field data from the SportContent Golf API.
Maintains consistent error handling and logging patterns with the existing codebase.
"""
import os
import requests
import logging
from typing import Dict, Any
from src.utils.headers.headers import sportcontentapi_headers

logger = logging.getLogger(__name__)

# API Configuration
SPORTCONTENTAPI_URL = "https://golf-leaderboard-data.p.rapidapi.com/entry-list"
HEADERS = sportcontentapi_headers

def fetch_tournament_field(tournament_id: str) -> Dict[str, Any]:
    """
    Fetch tournament field data from SportContent API.
    
    Args:
        tournament_id: SportContent API tournament identifier
        
    Returns:
        Dict containing tournament field data or None if request fails
        
    Raises:
        requests.exceptions.RequestException: If API request fails
    """
    logger.info(f"Fetching tournament field for tournament {tournament_id}")
    
    try:
        response = requests.get(
            SPORTCONTENTAPI_URL,
            headers=HEADERS,
            params={"tournamentId": tournament_id}
        )
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching tournament field: {str(e)}")
        raise