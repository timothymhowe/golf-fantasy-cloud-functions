"""
Firestore client for storing tournament results
"""

import logging
from typing import Dict, Any, Optional
from google.cloud import firestore
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def store_tournament_results(
    db: firestore.Client,
    tournament_id: int,
    results_data: Dict[str, Any]
) -> Optional[str]:
    """Store tournament results in Firestore
    
    Args:
        db: Firestore client
        tournament_id: Tournament ID
        results_data: Results data from SportContent API
        
    Returns:
        Document ID if successful, None if error
    """
    try:
        logger.info(f"Storing results for tournament {tournament_id}")
        
        # Add metadata
        document_data = {
            "tournament_id": tournament_id,
            "updated_at": datetime.utcnow(),
            "results": results_data
        }
        
        # Store in Firestore
        doc_ref = db.collection("tournament_results").document(str(tournament_id))
        doc_ref.set(document_data)
        
        return str(tournament_id)
        
    except Exception as e:
        logger.error(f"Error storing tournament results: {e}")
        return None

def get_tournament_results(
    db: firestore.Client,
    tournament_id: int
) -> Optional[Dict[str, Any]]:
    """Get tournament results from Firestore
    
    Args:
        db: Firestore client
        tournament_id: Tournament ID
        
    Returns:
        Results data if found, None if not found or error
    """
    try:
        logger.info(f"Getting results for tournament {tournament_id}")
        
        doc_ref = db.collection("tournament_results").document(str(tournament_id))
        doc = doc_ref.get()
        
        if doc.exists:
            return doc.to_dict()
        return None
        
    except Exception as e:
        logger.error(f"Error getting tournament results: {e}")
        return None
