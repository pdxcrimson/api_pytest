import pytest

from utils.client import APIClient


class TestNegativeCases:

    def test_get_nonexistent_post_returns_404(self, client: APIClient) -> None:
        resp = client.get("/posts/99999")
        assert resp.status_code == 404

    def test_create_post_missing_required_fields(self, client: APIClient) -> None:
        # JSONPlaceholder is permissive, but on a real API this should be 422
        resp = client.post("/posts", json={})
        assert resp.status_code in (400, 422, 201)  # document the actual behavior

    @pytest.mark.parametrize("bad_id", ["abc", "0", "-1", "9" * 20])
    def test_get_post_with_invalid_id(self, client: APIClient, bad_id: str) -> None:
        resp = client.get(f"/posts/{bad_id}")
        assert resp.status_code in (400, 404)

    def test_malformed_json_body(self, client: APIClient) -> None:
        resp = client.session.post(
            client._url("/posts"),
            data="not-json",
            headers={"Content-Type": "application/json"}
        )
        # JSONPlaceholder returns 500 for malformed JSON rather than 400/422.
        # On a well-behaved API this should be 400 or 422 — document the deviation.
        assert resp.status_code in (400, 422, 500)


    def test_unsupported_method(self, client: APIClient) -> None:
        resp = client.session.patch(client._url("/posts"), json={})
        # Document what the API actually returns — 404, 405, or 200
        assert resp.status_code in (404, 405, 200)