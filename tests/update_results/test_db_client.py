"""
Tests for tournament results database client
"""

import pytest
from unittest.mock import Mock
from datetime import datetime
from src.models import Tournament, Golfer, TournamentGolfer, TournamentGolferResult
from src.update_results.db_client import update_tournament_results, process_team_event

# Test data
MOCK_RESULTS_DATA = {
    "results": {
        "leaderboard": [
            {
                "position": 1,
                "player_id": 138154,
                "first_name": "Scottie",
                "last_name": "Scheffler",
                "status": "active",
                "total_to_par": -11
            },
            {
                "position": "T89",
                "player_id": 94954,
                "first_name": "Emiliano",
                "last_name": "Grillo",
                "status": "cut",
                "total_to_par": 15
            },
            {
                "position": "T3",
                "player_id": None,
                "first_name": "Cameron/Patrick",
                "last_name": "Smith",
                "status": "active",
                "total_to_par": -8
            }
        ]
    }
}

def test_update_tournament_results_success(db_session):
    """Test successful update of tournament results"""
    # Create test golfers
    golfer1 = Golfer(
        sportcontent_api_id=138154,
        full_name="Scottie Scheffler"
    )
    golfer2 = Golfer(
        sportcontent_api_id=94954,
        full_name="Emiliano Grillo"
    )
    db_session.add_all([golfer1, golfer2])
    db_session.commit()

    # Create tournament entries
    entry1 = TournamentGolfer(
        tournament_id=1,
        golfer_id=golfer1.id,
        year=datetime.now().year,
        is_most_recent=True,
        is_active=True
    )
    entry2 = TournamentGolfer(
        tournament_id=1,
        golfer_id=golfer2.id,
        year=datetime.now().year,
        is_most_recent=True,
        is_active=True
    )
    db_session.add_all([entry1, entry2])
    db_session.commit()

    # Update results
    result = update_tournament_results(db_session, 1, MOCK_RESULTS_DATA)
    assert result is True

    # Verify results were created
    results = db_session.query(TournamentGolferResult).all()
    assert len(results) == 2

    # Verify specific result details
    scheffler_result = next(r for r in results if r.tournament_golfer_id == entry1.id)
    assert scheffler_result.result == 1
    assert scheffler_result.status == "active"
    assert scheffler_result.score_to_par == -11

    grillo_result = next(r for r in results if r.tournament_golfer_id == entry2.id)
    assert grillo_result.result == "T89"
    assert grillo_result.status == "cut"
    assert grillo_result.score_to_par == 15

def test_process_team_event(db_session):
    """Test processing of team event entries"""
    # Create test golfers
    golfer1 = Golfer(
        full_name="Cameron Smith"
    )
    golfer2 = Golfer(
        full_name="Patrick Smith"
    )
    db_session.add_all([golfer1, golfer2])
    db_session.commit()

    # Create tournament entries
    entry1 = TournamentGolfer(
        tournament_id=1,
        golfer_id=golfer1.id,
        year=datetime.now().year,
        is_most_recent=True,
        is_active=True
    )
    entry2 = TournamentGolfer(
        tournament_id=1,
        golfer_id=golfer2.id,
        year=datetime.now().year,
        is_most_recent=True,
        is_active=True
    )
    db_session.add_all([entry1, entry2])
    db_session.commit()

    # Process team event entries
    process_team_event(db_session, 1)

    # Verify team event entries were created
    team_event_entries = db_session.query(TournamentGolfer).filter(TournamentGolfer.tournament_id == 1).all()
    assert len(team_event_entries) == 2

    # Verify specific team event details
    team_event_entry1 = next(te for te in team_event_entries if te.golfer_id == golfer1.id)
    assert team_event_entry1.is_team_event is True

    team_event_entry2 = next(te for te in team_event_entries if te.golfer_id == golfer2.id)
    assert team_event_entry2.is_team_event is True 