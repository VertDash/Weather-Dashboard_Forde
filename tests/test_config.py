import importlib
import sys
from unittest.mock import patch

"""Test that our API key loads correctly when it exists"""

def test_api_key_loaded(monkeypatch):
    # Set fake API key for test
    monkeypatch.setenv("OPENWEATHER_API_KEY", "dummykey")
    
    # Remove config from sys.modules to force reload
    if 'config' in sys.modules:
        del sys.modules['config']
    
    # Import and verify API key loaded
    import config
    assert config.OPENWEATHER_API_KEY == "dummykey"

"""Test code properly handles missing API key"""
def test_api_key_missing(monkeypatch):
    # Remove the API key from environment variables
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)
    
    # Remove config from sys.modules to force fresh import
    if 'config' in sys.modules:
        del sys.modules['config']
    
    # Mock load_dotenv to not load from .env file
    with patch('dotenv.load_dotenv'):
        # Now importing config should raise ValueError
        with pytest.raises(ValueError, match="No Openweather API key found"):
            import config