"""
Tests for tournament results API client
"""

import pytest
from unittest.mock import patch, Mock
from src.update_results.api_client import fetch_tournament_results

# Test data
MOCK_RESULTS_DATA = {
    "meta": {
        "title": "Golf Leaderboard - Masters Tournament",
        "description": "Golf Leaderboard including current leaderboard and round scores",
        "fields": {
            "tournament_object": {
                "id": "Integer",
                "type": "String - Stroke Play or Match Play - determines how to display leaderboard results.",
                "tour_id": "Integer",
                "name": "String",
                "country": "String",
                "course": "String",
                "start_date": "String",
                "end_date": "String",
                "timezone": "String",
                "prize_fund": "String",
                "fund_currency": "String",
                "live_details": {
                    "status": "String - pre, inprogress, endofday, completed",
                    "current_round": "Integer",
                    "total_rounds": "Integer - total number of rounds in competition",
                    "players": "Integer - number of active players",
                    "updated": "Timestamp - ISO UTC 2020-08-13T05:45:03+00:00",
                },
            },
            "leaderboard_array": {
                "position": "Integer - ignore if 0, position in tournament",
                "player_id": "Integer - unique player_id",
                "first_name": "String",
                "last_name": "String",
                "country": "String",
                "holes_played": "Integer - 0=Not Started, >0 In Play, 18=Finished",
                "current_round": "Integer - player current round",
                "status": "String - active, cut, retired, wd=withdrawn, dsq=disqualified",
                "strokes": "Integer - total strokes across all rounds - updated on completion of each round, default = 0",
                "updated": "Timestamp - Format ISO UTC 2020-08-13T05:45:03+00:00",
                "prize_money": "String - player winnings",
                "ranking_points": "String - ranking points won for this competition",
                "total_to_par": "String - player score over all rounds completed",
                "rounds_array": {
                    "round_number": "Integer",
                    "course_number": "Integer - course to which round relates",
                    "position_round": "Integer - position within this round",
                    "tee_time_local": "String - tee time in tournament timezone",
                    "total_to_par": "String - score this round",
                    "strokes": "Integer - strokes this round",
                    "updated": "Timestamp - Format ISO UTC 2020-08-13T05:45:03+00:00",
                },
            },
        },
    },
    "results": {
        "tournament": {
            "id": 651,
            "type": "Stroke Play",
            "tour_id": 2,
            "name": "Masters Tournament",
            "country": "Augusta, USA",
            "course": "Augusta National Golf Club",
            "start_date": "2024-04-11 00:00:00",
            "end_date": "2024-04-14 00:00:00",
            "timezone": "America\/New_York",
            "prize_fund": "18,000,000",
            "fund_currency": "USD",
            "live_details": {
                "status": "endofday",
                "current_round": 4,
                "total_rounds": 4,
                "players": 89,
                "cut_value": None,
                "updated": "2024-04-15T02:38:09+00:00",
            },
        },
        "leaderboard": [
            {
                "position": 1,
                "player_id": 138154,
                "first_name": "Scottie",
                "last_name": "Scheffler",
                "country": "USA",
                "holes_played": 18,
                "current_round": 4,
                "status": "active",
                "strokes": 277,
                "updated": "2024-04-27T20:06:10+00:00",
                "prize_money": "3600000",
                "ranking_points": "750",
                "total_to_par": -11,
                "rounds": [
                    {
                        "round_number": 1,
                        "course_number": 1,
                        "position_round": 2,
                        "tee_time_local": "14:35",
                        "total_to_par": -6,
                        "strokes": 66,
                        "updated": "2024-04-09T23:00:08+00:00",
                    },
                    {
                        "round_number": 2,
                        "course_number": 1,
                        "position_round": 9,
                        "tee_time_local": "14:35",
                        "total_to_par": 0,
                        "strokes": 72,
                        "updated": "2024-04-09T23:00:08+00:00",
                    },
                    {
                        "round_number": 3,
                        "course_number": 1,
                        "position_round": 7,
                        "tee_time_local": "14:35",
                        "total_to_par": -1,
                        "strokes": 71,
                        "updated": "2024-04-09T23:00:08+00:00",
                    },
                    {
                        "round_number": 4,
                        "course_number": 1,
                        "position_round": 2,
                        "tee_time_local": "14:35",
                        "total_to_par": -4,
                        "strokes": 68,
                        "updated": "2024-04-09T23:00:08+00:00",
                    },
                ],
            },
            {
                "position": 2,
                "player_id": 158881,
                "first_name": "Ludvig",
                "last_name": "\u00c5berg",
                "country": "SWE",
                "holes_played": 18,
                "current_round": 4,
                "status": "active",
                "strokes": 281,
                "updated": "2024-04-27T20:06:11+00:00",
                "prize_money": "2160000",
                "ranking_points": "400",
                "total_to_par": -7,
                "rounds": [
                    {
                        "round_number": 1,
                        "course_number": 1,
                        "position_round": 35,
                        "tee_time_local": "14:25",
                        "total_to_par": 1,
                        "strokes": 73,
                        "updated": "2024-04-09T23:00:13+00:00",
                    },
                    {
                        "round_number": 2,
                        "course_number": 1,
                        "position_round": 1,
                        "tee_time_local": "14:25",
                        "total_to_par": -3,
                        "strokes": 69,
                        "updated": "2024-04-09T23:00:13+00:00",
                    },
                    {
                        "round_number": 3,
                        "course_number": 1,
                        "position_round": 3,
                        "tee_time_local": "14:25",
                        "total_to_par": -2,
                        "strokes": 70,
                        "updated": "2024-04-09T23:00:13+00:00",
                    },
                    {
                        "round_number": 4,
                        "course_number": 1,
                        "position_round": 4,
                        "tee_time_local": "14:25",
                        "total_to_par": -3,
                        "strokes": 69,
                        "updated": "2024-04-09T23:00:13+00:00",
                    },
                ],
            },
            {
                "position": 89,
                "player_id": 94954,
                "first_name": "Emiliano",
                "last_name": "Grillo",
                "country": "ARG",
                "holes_played": 0,
                "current_round": 4,
                "status": "cut",
                "strokes": 159,
                "updated": "2024-04-15T02:38:09+00:00",
                "prize_money": "",
                "ranking_points": "",
                "total_to_par": 15,
                "rounds": [
                    {
                        "round_number": 1,
                        "course_number": 1,
                        "position_round": 68,
                        "tee_time_local": "08:36",
                        "total_to_par": 4,
                        "strokes": 76,
                        "updated": "2024-04-09T23:00:10+00:00",
                    },
                    {
                        "round_number": 2,
                        "course_number": 1,
                        "position_round": 89,
                        "tee_time_local": "08:36",
                        "total_to_par": 11,
                        "strokes": 83,
                        "updated": "2024-04-09T23:00:10+00:00",
                    },
                    {
                        "round_number": 3,
                        "course_number": 1,
                        "position_round": 13,
                        "tee_time_local": "08:36",
                        "total_to_par": 0,
                        "strokes": 0,
                        "updated": "2024-04-09T23:00:10+00:00",
                    },
                    {
                        "round_number": 4,
                        "course_number": 1,
                        "position_round": 21,
                        "tee_time_local": "08:36",
                        "total_to_par": 0,
                        "strokes": 0,
                        "updated": "2024-04-09T23:00:10+00:00",
                    },
                ],
            },
        ],
    },
}


def test_fetch_tournament_results_success():
    """Test successful API call"""
    with patch("requests.get") as mock_get:
        # Configure mock
        mock_response = Mock()
        mock_response.json.return_value = MOCK_RESULTS_DATA
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Call function
        result = fetch_tournament_results(12345)

        # Verify results
        assert result is not None
        assert result == MOCK_RESULTS_DATA
        assert result["results"]["tournament"]["id"] == 651

        # Verify API was called correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "leaderboard/12345" in args[0]


def test_fetch_tournament_results_error():
    """Test API error handling"""
    with patch("requests.get") as mock_get:
        # Configure mock to raise an error
        mock_get.side_effect = Exception("API Error")

        # Call function
        result = fetch_tournament_results(12345)

        # Verify error handling
        assert result is None

        # Verify API was called
        mock_get.assert_called_once()


def test_fetch_tournament_results_missing_key():
    """Test handling of missing data in API response"""
    with patch("requests.get") as mock_get:
        # Configure mock to return error response
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception(
            "401 Client Error: Unauthorized"
        )
        mock_get.return_value = mock_response

        # Call function
        result = fetch_tournament_results(12345)

        # Verify error handling
        assert result is None

        # Verify API was called
        mock_get.assert_called_once()
