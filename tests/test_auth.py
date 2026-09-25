# tests/test_auth.py
import pytest
import requests
from utils.client import APIClient

REQRES_BASE = "https://reqres.in/api"


class TestAuthHeaderPlumbing:
    """
    Verifies that APIClient correctly attaches Authorization headers.
    JSONPlaceholder ignores auth headers but still returns 200,
    so we can confirm the header is sent without needing a real auth flow.
    """


    @pytest.mark.smoke
    def test_client_attaches_bearer_token(self):
        client = APIClient(base_url="https://jsonplaceholder.typicode.com", token="fake-token")
        resp = client.get("/posts/1")
        assert resp.status_code == 200
        sent_header = resp.request.headers.get("Authorization")
        assert sent_header == "Bearer fake-token"

    def test_client_without_token_has_no_auth_header(self):
        client = APIClient(base_url="https://jsonplaceholder.typicode.com")
        resp = client.get("/posts/1")
        assert "Authorization" not in resp.request.headers


class TestRealAuthFlows:
    """
    Uses reqres.in which provides real auth endpoints.
    Good reference for testing login/register flows on a real API.
    """

    @pytest.mark.smoke
    def test_login_valid_credentials(self):
        resp = requests.post(f"{REQRES_BASE}/login", json={
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        })
        assert resp.status_code == 200
        body = resp.json()
        assert "token" in body
        assert isinstance(body["token"], str)
        assert len(body["token"]) > 0

    def test_login_missing_password_returns_400(self):
        resp = requests.post(f"{REQRES_BASE}/login", json={
            "email": "eve.holt@reqres.in"
            # password intentionally omitted
        })
        assert resp.status_code == 400
        assert "error" in resp.json()

    def test_login_unknown_user_returns_400(self):
        resp = requests.post(f"{REQRES_BASE}/login", json={
            "email": "nobody@example.com",
            "password": "doesntmatter"
        })
        assert resp.status_code == 400

    def test_register_valid(self):
        resp = requests.post(f"{REQRES_BASE}/register", json={
            "email": "eve.holt@reqres.in",
            "password": "pistol"
        })
        assert resp.status_code == 200
        body = resp.json()
        assert "token" in body
        assert "id" in body

    def test_register_missing_password_returns_400(self):
        resp = requests.post(f"{REQRES_BASE}/register", json={
            "email": "eve.holt@reqres.in"
        })
        assert resp.status_code == 400
        assert resp.json().get("error") == "Missing password"

    def test_token_can_be_used_in_client(self):
        """
        Full flow: login, extract token, attempt authenticated request.
        Note: reqres.in now requires an api-key header for most endpoints,
        so this test validates the token is extracted and attached correctly
        even though the request returns 401 without the API key.
        """
        login = requests.post(f"{REQRES_BASE}/login", json={
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        })
        assert login.status_code == 200
        token = login.json()["token"]
        assert token is not None

        # Confirm the client attaches the token correctly
        authed_client = APIClient(base_url=REQRES_BASE, token=token)
        resp = authed_client.get("/users/2")
        assert resp.request.headers["Authorization"] == f"Bearer {token}"
        # reqres.in returns 401 without an api-key header — token attachment is still verified above
        assert resp.status_code == 401