import pytest
from flask import Flask

# from chat_doc.app.app import App


@pytest.fixture
def client():
    app = Flask("test")
    app.config["TESTING"] = True  # Enable testing mode
    with app.test_client() as client:
        yield client


def test_app_starts(client):
    response = client.get("/")
    assert response.status_code == 200


def test_chat_loads(client):
    response = client.get("/chat")
    assert response.status_code == 200


def test_404(client):  # test 404 page --> prevent crashes
    response = client.get("/random-xyz")
    assert response.status_code == 404


if __name__ == "__main__":
    pytest.main()
