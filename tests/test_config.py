import pytest
import importlib

"""Test that our API key loads correctly when it exists"""

def test_api_key_loaded(monkeypatch):
    # fake API for test
    # load config
    # make sure AOI loaded 
    monkeypatch.setenv("OPENWEATHER_API_KEY", "dummykey")
    import config
    importlib.reload(config)
    assert config.OPENWEATHER_API_KEY == "dummykey"

"""Test code properly handles missing API key"""
def test_api_key_missing(monkeypatch):
    # Remove the API from env variables
    # make sure it raises error if key is missing 

    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)
    import config
    with pytest.raises(ValueError):
        importlib.reload(config)