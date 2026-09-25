import pytest

from utils.client import APIClient

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def client() -> APIClient:
    """One session for the whole run — avoids re-handshaking per test."""
    return APIClient(base_url=BASE_URL)


@pytest.fixture(scope="session")
def existing_post(client):
    """Seed fixture: fetch a known post once, reuse across tests."""
    resp = client.get("/posts/1")
    assert resp.status_code == 200
    return resp.json()


@pytest.fixture
def new_post_payload():
    return {"title": "Test title", "body": "Test body", "userId": 1}
