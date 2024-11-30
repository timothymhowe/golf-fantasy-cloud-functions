"""
Database client for updating tournament results
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from sqlalchemy.orm import Session
from src.models import Tournament, Golfer, TournamentGolfer, TournamentGolferResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_team_event(
    session: Session, 
    tournament_id: int, 
    result: Dict[str, Any]
) -> List[TournamentGolfer]:
    """Process team event entry and return tournament golfers"""
    try:
        # Extract team member names
        first_name = result.get('first_name', '').strip().rstrip('/')
        last_name = result.get('last_name', '').strip()
        team_members = first_name.split('/')
        
        tournament_golfers = []
        for member in team_members:
            # Find or create golfer
            golfer = session.query(Golfer)\
                .filter_by(full_name=f"{member} {last_name}")\
                .first()
            
            if golfer:
                # Find tournament entry
                tournament_golfer = session.query(TournamentGolfer)\
                    .filter_by(
                        tournament_id=tournament_id,
                        golfer_id=golfer.id,
                        year=datetime.now().year,
                        is_most_recent=True
                    ).first()
                
                if tournament_golfer:
                    tournament_golfers.append(tournament_golfer)
        
        return tournament_golfers
    except Exception as e:
        logger.error(f"Error processing team event: {e}")
        return []

def update_tournament_results(session: Session, tournament_id: int, results_data: Dict[str, Any]) -> bool:
    """Update tournament results in database"""
    try:
        logger.info(f"Updating results for tournament {tournament_id}")
        
        for result in results_data["results"]["leaderboard"]:
            position = result.get('position')
            status = result.get('status', '').lower()
            score_to_par = result.get('total_to_par')
            
            # Clean up status
            clean_status = 'active'
            if status in ['cut', 'wd', 'dq']:
                clean_status = status
            
            # Check for team event
            first_name = result.get('first_name', '').strip()
            if first_name.endswith('/'):
                tournament_golfers = process_team_event(session, tournament_id, result)
                if not tournament_golfers:
                    logger.warning("Failed to process team entry")
                    continue
                
                # Create result entries for both team members
                for tournament_golfer in tournament_golfers:
                    new_result = TournamentGolferResult(
                        tournament_golfer_id=tournament_golfer.id,
                        result=position,
                        status=clean_status,
                        score_to_par=score_to_par
                    )
                    session.add(new_result)
                continue
            
            # Regular player - find their tournament entry
            player_id = result.get('player_id')
            if not player_id:
                logger.warning(f"Missing player_id in result: {result}")
                continue
            
            tournament_golfer = session.query(TournamentGolfer)\
                .join(Golfer)\
                .filter(
                    TournamentGolfer.tournament_id == tournament_id,
                    Golfer.sportcontent_api_id == player_id,
                    TournamentGolfer.year == datetime.now().year,
                    TournamentGolfer.is_most_recent == True
                ).first()
            
            if tournament_golfer:
                new_result = TournamentGolferResult(
                    tournament_golfer_id=tournament_golfer.id,
                    result=position,
                    status=clean_status,
                    score_to_par=score_to_par
                )
                session.add(new_result)
        
        session.commit()
        return True
        
    except Exception as e:
        logger.error(f"Error updating tournament results: {e}")
        session.rollback()
        return False

def get_most_recent_tournament(session: Session) -> Optional[Dict[str, Any]]:
    """Get most recent tournament from database
    
    Args:
        session: Database session
        
    Returns:
        Tournament details if found, None if not found
    """
    try:
        logger.info("Getting most recent tournament")
        
        # Query tournament with most recent end date
        tournament = session.query(Tournament)\
            .filter(Tournament.end_date < datetime.now())\
            .order_by(Tournament.end_date.desc())\
            .first()
            
        if not tournament:
            logger.warning("No completed tournaments found")
            return None
            
        return {
            "id": tournament.id,
            "sportcontent_api_id": tournament.sportcontent_api_id,
            "tournament_name": tournament.tournament_name,
            "tournament_format": tournament.tournament_format,
            "end_date": tournament.end_date.strftime('%Y-%m-%d'),
            "course_name": tournament.course_name,
            "location_raw": tournament.location_raw
        }
        
    except Exception as e:
        logger.error(f"Error getting most recent tournament: {e}")
        return None
