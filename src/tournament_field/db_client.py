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

def update_tournament_entries(
    session,
    tournament_id: int,
    field_data: Dict[str, Any]
) -> Optional[bool]:
    """
    Update tournament entries in SQL database.
    
    Args:
        session: SQLAlchemy session
        tournament_id: Tournament ID in our database
        field_data: Field data from SportContent API
        
    Returns:
        True if successful, None if failed
    """
    logger.info(f"Updating entries for tournament {tournament_id}")
    year = str(datetime.now().year)
    
    try:
        # Mark existing entries as not most recent
        (session.query(TournamentGolfer)
         .filter(and_(
             TournamentGolfer.tournament_id == tournament_id,
             TournamentGolfer.year == year
         ))
         .update({"is_most_recent": False}))
        
        # Get golfer mapping
        golfers = {
            g.sportcontent_api_id: g.id 
            for g in session.query(Golfer)
            .filter(Golfer.sportcontent_api_id.isnot(None))
            .all()
        }
        
        # Add new entries
        for player in field_data.get("field", []):
            player_id = str(player.get("player_id"))
            if player_id in golfers:
                entry = TournamentGolfer(
                    tournament_id=tournament_id,
                    golfer_id=golfers[player_id],
                    year=year,
                    is_most_recent=True,
                    is_active=True
                )
                session.add(entry)
            else:
                logger.warning(f"Golfer with SportContent ID {player_id} not found in database")
        
        session.commit()
        return True
        
    except Exception as e:
        logger.error(f"Error updating tournament entries: {str(e)}")
        session.rollback()
        return None
