import pytest
import importlib

def test_api_key_loaded(monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "dummykey")
    import config
    importlib.reload(config)
    assert config.OPENWEATHER_API_KEY == "dummykey"

def test_api_key_missing(monkeypatch):
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)
    import config
    with pytest.raises(ValueError):
        importlib.reload(config)