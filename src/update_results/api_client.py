import requests
import logging
from typing import Dict, Any, Optional

from src.utils.headers.headers import sportcontentapi_headers

# configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_tournament_results(tournament_id: int) -> Optional[Dict[str, Any]]:
    """Fetch tournament results from SportContent API
    
    Args:
        tournament_id: Tournament ID in our database
    """
    try:
        logger.info(f"Fetching tournament results for {tournament_id}")
        url = f"https://golf-leaderboard-data.p.rapidapi.com/leaderboard/{tournament_id}"
        
        headers = sportcontentapi_headers
        
        response = requests.get(url, headers=headers)
        
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching tournament results: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching tournament results: {e}")
        return None
