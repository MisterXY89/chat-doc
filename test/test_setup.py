import pytest


def test_config():
    from chat_doc.config import config

    # "credentials" setup does not make sense as we set .env vars manually
    # --> see conftest.py

    required_keys = ["logging", "app"]
    for key in required_keys:
        assert key in config

    assert 1 == 1


if __name__ == "__main__":
    pytest.main()
