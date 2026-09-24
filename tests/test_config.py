from src.utils.config_loader import load_config


def test_load_config():
    config = load_config()
    assert "base_url" in config
    assert config["timeout"] == 10
    assert config["auth"]["username"] == "admin"