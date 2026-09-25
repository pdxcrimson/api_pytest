import pytest

from utils.validators import assert_schema


class TestSchemaContracts:

    @pytest.mark.smoke
    def test_single_post_matches_schema(self, client):
        resp = client.get("/posts/1")
        assert resp.status_code == 200
        assert_schema(resp.json(), "post")

    def test_post_list_all_items_match_schema(self, client):
        resp = client.get("/posts")
        assert resp.status_code == 200
        # Validates every item in the list — not just the first one
        assert_schema(resp.json(), "post")

    def test_created_post_matches_schema(self, client, new_post_payload):
        resp = client.post("/posts", json=new_post_payload)
        assert resp.status_code == 201
        assert_schema(resp.json(), "post")

    def test_response_headers(self, client):
        """Contract test for headers — often overlooked."""
        resp = client.get("/posts/1")
        assert "application/json" in resp.headers.get("Content-Type", "")
        # JSONPlaceholder is served via Cloudflare which uses Brotli compression
        assert resp.headers.get("Content-Encoding") == "br"

    def test_response_time_sla(self, client):
        """Non-functional contract: p99 of a single call should be under 2s."""
        resp = client.get("/posts/1")
        assert resp.elapsed.total_seconds() < 2.0, (
            f"Response took {resp.elapsed.total_seconds():.2f}s — SLA is 2s"
        )