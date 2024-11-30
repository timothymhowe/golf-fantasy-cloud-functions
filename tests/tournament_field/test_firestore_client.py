"""
Tests for Firestore client functionality
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timezone
from google.cloud import firestore
from src.tournament_field.firestore_client import store_tournament_field, get_tournament_field

# Test data
MOCK_TOURNAMENT_ID = "659"
MOCK_FIELD_DATA = {
    "results": {
        "tournament": {
            "id": 659,
            "type": "Stroke Play",
            "name": "Charles Schwab Challenge",
        },
        "entry_list": [
            {
                "player_id": 100240,
                "first_name": "Tyson",
                "last_name": "Alexander",
                "country": "USA"
            }
        ]
    }
}

@pytest.fixture
def mock_db():
    """Create a mock Firestore client"""
    mock_client = Mock(spec=firestore.Client)
    mock_collection = Mock(spec=firestore.CollectionReference)
    mock_doc = Mock(spec=firestore.DocumentReference)
    
    # Setup the chain of calls
    mock_client.collection.return_value = mock_collection
    mock_collection.document.return_value = mock_doc
    
    return mock_client, mock_doc

def test_store_tournament_field_success(mock_db):
    """Test successful storage of tournament field data"""
    mock_client, mock_doc = mock_db
    
    result = store_tournament_field(mock_client, MOCK_TOURNAMENT_ID, MOCK_FIELD_DATA)
    
    assert result is True
    mock_client.collection.assert_called_once_with("tournament_fields")
    mock_client.collection().document.assert_called_once_with(MOCK_TOURNAMENT_ID)
    
    # Verify the data being stored
    call_args = mock_doc.set.call_args[0][0]
    assert call_args["field"] == MOCK_FIELD_DATA
    assert call_args["data_source"] == "sportcontent_api"
    assert isinstance(call_args["last_updated"], datetime)

def test_store_tournament_field_error(mock_db):
    """Test error handling when storing tournament field data"""
    mock_client, mock_doc = mock_db
    mock_doc.set.side_effect = Exception("Firestore error")
    
    result = store_tournament_field(mock_client, MOCK_TOURNAMENT_ID, MOCK_FIELD_DATA)
    
    assert result is None

def test_get_tournament_field_success(mock_db):
    """Test successful retrieval of tournament field data"""
    mock_client, mock_doc = mock_db
    mock_doc.get.return_value.exists = True
    mock_doc.get.return_value.to_dict.return_value = {
        "field": MOCK_FIELD_DATA,
        "last_updated": datetime.now(timezone.utc),
        "data_source": "sportcontent_api"
    }
    
    result = get_tournament_field(mock_client, MOCK_TOURNAMENT_ID)
    
    assert result["field"] == MOCK_FIELD_DATA
    mock_client.collection.assert_called_once_with("tournament_fields")
    mock_client.collection().document.assert_called_once_with(MOCK_TOURNAMENT_ID)

def test_get_tournament_field_not_found(mock_db):
    """Test handling of non-existent tournament field data"""
    mock_client, mock_doc = mock_db
    mock_doc.get.return_value.exists = False
    
    result = get_tournament_field(mock_client, MOCK_TOURNAMENT_ID)
    
    assert result is None

def test_get_tournament_field_error(mock_db):
    """Test error handling when retrieving tournament field data"""
    mock_client, mock_doc = mock_db
    mock_doc.get.side_effect = Exception("Firestore error")
    
    result = get_tournament_field(mock_client, MOCK_TOURNAMENT_ID)
    
    assert result is None