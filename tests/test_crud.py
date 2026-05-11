import pytest

class TestPostsCRUD:

    def test_list_posts_returns_100(self, client):
        resp = client.get("/posts")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 100

    def test_get_post_by_id(self, client, existing_post):
        assert existing_post["id"] == 1
        assert "title" in existing_post
        assert "body" in existing_post
        assert "userId" in existing_post

    def test_create_post(self, client, new_post_payload):
        resp = client.post("/posts", json=new_post_payload)
        assert resp.status_code == 201
        body = resp.json()
        assert body["title"] == new_post_payload["title"]
        assert "id" in body  # server assigns an ID

    def test_update_post(self, client):
        resp = client.put("/posts/1", json={
            "id": 1, "title": "updated", "body": "updated body", "userId": 1
        })
        assert resp.status_code == 200
        assert resp.json()["title"] == "updated"

    def test_delete_post(self, client):
        resp = client.delete("/posts/1")
        assert resp.status_code == 200  # JSONPlaceholder returns 200 not 204