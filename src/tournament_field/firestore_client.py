"""
Firestore Client

Handles storing tournament field data in Firestore.
Maintains historical records of tournament fields with timestamps.
"""

from google.cloud import firestore
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

def store_tournament_field(
    db: firestore.Client,
    tournament_id: str,
    field_data: Dict[str, Any]
) -> Optional[bool]:
    """
    Store tournament field data in Firestore.
    
    Args:
        db: Initialized Firestore client
        tournament_id: Tournament identifier
        field_data: Field data from SportContent API
        
    Returns:
        True if successful, None if failed
    """
    logger.info(f"Storing tournament field for tournament {tournament_id}")
    
    try:
        doc_ref = db.collection("tournament_fields").document(tournament_id)
        doc_ref.set({
            "field": field_data,
            "last_updated": datetime.now(timezone.utc),
            "data_source": "sportcontent_api"
        })
        return True
        
    except Exception as e:
        logger.error(f"Error storing tournament field in Firestore: {str(e)}")
        return None
    
    
    

def get_tournament_field(db: firestore.Client,tournament_id: str) -> Optional [Dict[str, Any]]:
    """
    Retrieve tournament field data from Firestore.  Not currently used, but could be useful in the future.
    
    Args:
        db: Initialized Firestore client
        tournament_id: Tournament identifier
        
    Returns:
        Tournament field data or None if not found
    """
    logger.info(f"Retrieving tournament field for tournament {tournament_id}")
    
    try:
        doc_ref = db.collection("tournament_fields").document(tournament_id)
        doc = doc_ref.get()
        
        if doc.exists:
            return doc.to_dict()
        return None
        
    except Exception as e:
        logger.error(f"Error retrieving tournament field from Firestore: {str(e)}")
        return None
