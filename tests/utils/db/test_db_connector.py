import pytest
from unittest.mock import patch, Mock
from src.utils.db.db_connector import get_db_config, clean_env, get_db_connection


@pytest.fixture
def mock_sql_connector():
    with patch('src.utils.db.db_connector.sql_connector') as mock_sql_connector:
        yield mock_sql_connector
    
@pytest.fixture
def mock_env_vars(monkeypatch):
    env_vars = {
        'DB_USER': 'test_user',
        'DB_PASS': 'test_pass',
        'DB_NAME': 'test_db',
        'INSTANCE_CONNECTION_STRING_FULL': 'test-project:region:instance'
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars

#############################################################
#                           TESTS                           #
#############################################################
def test_clean_env_strips_quotes():
    """Ensure that quotes are stripped from environment variables"""
    assert clean_env('TEST','"value"') == 'value'
    assert clean_env('TEST',"'value'") == 'value'
    assert clean_env('TEST','     value    ') == 'value'
    
def test_db_config_loads_from_env(mock_env_vars):
    """Test that DB_CONFIG loads correctly from environment"""
    config = get_db_config()
    assert config['instance_connection_string'] == 'test-project:region:instance'
    assert config['user'] == 'test_user'
    assert config['password'] == 'test_pass'
    assert config['database'] == 'test_db'

    
@patch('sqlalchemy.create_engine')
def test_get_db_connection_success(mock_create_engine, mock_sql_connector, mock_env_vars):
    """Ensure that get_db_connection returns a connection object"""
    mock_engine = Mock()
    mock_create_engine.return_value = mock_engine
    mock_connection = Mock()
    mock_sql_connector.connect.return_value = mock_connection
    
    engine = get_db_connection()
    
    # Get the creator lambda from the create_engine call
    creator = mock_create_engine.call_args[1]['creator']
    # Execute the creator lambda
    connection = creator()
    
    assert engine is mock_engine
    assert connection is mock_connection
    mock_sql_connector.connect.assert_called_once_with(
        'test-project:region:instance',
        'pymysql',
        user='test_user',
        password='test_pass',
        db='test_db'
    )

@patch('sqlalchemy.create_engine')
def test_get_db_connection_failure(mock_create_engine, mock_sql_connector, mock_env_vars):
    """test db connection failure"""
    mock_sql_connector.connect.side_effect = Exception("Connection failed")
    mock_engine = Mock()
    mock_create_engine.return_value = mock_engine
    
    with pytest.raises(Exception) as exception:
        engine = get_db_connection()
        # Get the creator lambda from the create_engine call
        creator = mock_create_engine.call_args[1]['creator']
        # Execute the creator lambda
        creator()
    
    assert "Connection failed" in str(exception.value)