"""
Database Client

Handles SQL database operations for tournament fields using SQLAlchemy ORM.
Ports functionality from golf-fantasy-backend.
"""

from sqlalchemy import and_
from datetime import datetime
from typing import Dict, Any, Optional
import logging
from src.models import Tournament, TournamentGolfer, Golfer

logger = logging.getLogger(__name__)

def get_upcoming_tournament(session) -> Optional[Dict[str, Any]]:
    """
    Get the next upcoming tournament from SQL database.
    
    Args:
        session: SQLAlchemy session
        
    Returns:
        Tournament info dict or None if not found
    """
    logger.info("Fetching upcoming tournament")
    
    try:
        tournament = (
            session.query(Tournament)
            .filter(Tournament.start_date > datetime.now())
            .order_by(Tournament.start_date)
            .first()
        )
        
        if not tournament:
            logger.warning("No upcoming tournament found")
            return None
            
        return {
            "id": tournament.id,
            "sportcontent_api_id": tournament.sportcontent_api_id,
            "tournament_name": tournament.tournament_name
        }
            
    except Exception as e:
        logger.error(f"Error fetching upcoming tournament: {str(e)}")
        return None

def update_tournament_entries(session, tournament_id, field_data):
    """
    Update tournament entries in SQL database.
    
    Args:
        session: SQLAlchemy session
        tournament_id: Tournament ID in our database
        field_data: Field data from SportContent 
    """
    try:
        logger.info(f"Updating entries for tournament {tournament_id}")
        
        # Deactivate existing entries
        existing_entries = session.query(TournamentGolfer)\
            .filter_by(
                tournament_id=tournament_id,
                year=datetime.now().year,
                is_most_recent=True
            ).all()
        
        for entry in existing_entries:
            entry.is_most_recent = False
        
        # Add new entries
        for player in field_data["results"]["entry_list"]:
            player_id = player["player_id"]
            logger.debug(f"Looking for golfer with sportcontent_api_id: {player_id}")
            
            golfer = session.query(Golfer)\
                .filter_by(sportcontent_api_id=player_id)\
                .first()
            
            if golfer:
                logger.debug(f"Found golfer: {golfer.full_name}")
                new_entry = TournamentGolfer(
                    tournament_id=tournament_id,
                    golfer_id=golfer.id,
                    year=datetime.now().year,
                    is_most_recent=True,
                    is_active=True
                )
                session.add(new_entry)
            else:
                logger.warning(f"Golfer not found with sportcontent_api_id: {player_id}")
        
        session.commit()
        return True
    except Exception as e:
        logger.error(f"Error updating tournament entries: {e}")
        session.rollback()
        return None
