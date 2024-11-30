import pytest
import os
from dotenv import load_dotenv

@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    """Load test environment variables for all tests"""
    load_dotenv('.env.test')