"""
Tests for SportContent API client functionality
"""

import pytest
from unittest.mock import patch
from src.tournament_field.api_client import fetch_tournament_field
import os
import requests
# Test data
MOCK_TOURNAMENT_ID = "12345"
MOCK_API_RESPONSE = {"meta":{"title":"Golf Entry List - Charles Schwab Challenge","description":"Golf Entry List for given tournament","fields":{"tournament_object":{"id":"Integer","type":"String - Stroke Play or Match Play - determines how to display leaderboard results.","tour_id":"Integer","name":"String","country":"String","course":"String","start_date":"String","end_date":"String","timezone":"String","prize_fund":"String","fund_currency":"String","live_details":{"status":"String - pre, inprogress, endofday, completed","current_round":"Integer","total_rounds":"Integer - total number of rounds in competition","players":"Integer - number of active players","updated":"Timestamp - ISO UTC 2020-08-13T05:45:03+00:00"}},"entry_list_array":{"player_id":"Integer - unique player_id","first_name":"String","last_name":"String","country":"String"}}},"results":{"tournament":{"id":659,"type":"Stroke Play","tour_id":2,"name":"Charles Schwab Challenge","country":"Fort Worth, USA","course":"Colonial Country Club","start_date":"2024-05-23 00:00:00","end_date":"2024-05-26 00:00:00","timezone":"America\/Chicago","prize_fund":"9,100,000","fund_currency":"USD"},"entry_list":[{"player_id":100240,"first_name":"Tyson","last_name":"Alexander","country":"USA"},{"player_id":103138,"first_name":"Erik","last_name":"Barnes","country":"USA"}]}}

@pytest.fixture
def mock_api_key(monkeypatch):
    """Set mock API key in environment"""
    monkeypatch.setenv("SPORTCONTENTAPI_KEY", "test_key")

@patch('requests.get')
def test_fetch_tournament_field_success(mock_get, mock_api_key):
    """Test successful API call"""
    # Setup mock response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = MOCK_API_RESPONSE
    
    result = fetch_tournament_field(MOCK_TOURNAMENT_ID)
    
    assert result == MOCK_API_RESPONSE
    mock_get.assert_called_once()

@patch('requests.get')
def test_fetch_tournament_field_error(mock_get, mock_api_key):
    """Test API error handling"""
    mock_get.side_effect = requests.exceptions.RequestException("API Error")
    
    with pytest.raises(requests.exceptions.RequestException):
        fetch_tournament_field(MOCK_TOURNAMENT_ID)

def test_fetch_tournament_field_missing_key():
    """Test handling of missing API key"""
    if "SPORTCONTENTAPI_KEY" in os.environ:
        del os.environ["SPORTCONTENTAPI_KEY"]
    
    with pytest.raises(requests.exceptions.HTTPError, match="401 Client Error: Unauthorized"):
        fetch_tournament_field(MOCK_TOURNAMENT_ID)