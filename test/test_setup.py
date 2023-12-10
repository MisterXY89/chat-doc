import pytest


def test_config():
    from chat_doc.config import config

    required_keys = ["logging", "app"]
    for key in required_keys:
        assert key in config


if __name__ == "__main__":
    pytest.main()
