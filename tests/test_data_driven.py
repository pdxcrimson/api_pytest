import pytest

VALID_POST_IDS = [1, 25, 50, 75, 100]
VALID_USER_IDS = [1, 2, 5, 10]

@pytest.mark.parametrize("post_id", VALID_POST_IDS)
def test_post_ids_all_return_valid_schema(client, post_id):
    from utils.validators import assert_schema
    resp = client.get(f"/posts/{post_id}")
    assert resp.status_code == 200
    assert_schema(resp.json(), "post")

@pytest.mark.parametrize("user_id", VALID_USER_IDS)
def test_filter_posts_by_user(client, user_id):
    resp = client.get("/posts", params={"userId": user_id})
    assert resp.status_code == 200
    posts = resp.json()
    assert len(posts) > 0
    # Assert the filter actually worked
    assert all(p["userId"] == user_id for p in posts)

@pytest.mark.parametrize("field,value,expected_count", [
    ("userId", 1, 10),
    ("userId", 2, 10),
])
def test_filter_returns_expected_count(client, field, value, expected_count):
    resp = client.get("/posts", params={field: value})
    assert len(resp.json()) == expected_count