import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from src.main import app


mock_post_data = [
    {
        "_id": "1",
        "title": "Post 1",
        "short_description": "Short description of Post 1",
        "description": "Description of Post 1",
        "tags": ["tag1", "tag2"],
        "created_at": "2023-07-26T12:00:00.000Z",
        "updated_at": "2023-07-26T12:30:00.000Z",
    },
    {
        "_id": "2",
        "title": "Post 2",
        "short_description": "Short description of Post 2",
        "description": "Description of Post 2",
        "tags": ["tag3", "tag4"],
        "created_at": "2023-07-26T13:00:00.000Z",
        "updated_at": "2023-07-26T13:30:00.000Z",
    },
]

# Expected keys for each API response
expected_keys_get_posts = {"_id", "title", "short_description", "description", "tags", "created_at", "updated_at"}
expected_keys_get_post = {"_id", "title", "short_description", "description", "tags", "created_at", "updated_at"}
expected_keys_add_post = {"title", "short_description", "description", "tags", "created_at", "updated_at"}
expected_keys_update_post_full = { "title", "short_description", "description", "tags", "created_at", "updated_at"}
expected_keys_update_post_partial = {"title", "short_description", "description", "tags", "created_at", "updated_at"}
expected_keys_delete_post = {"_id", "title", "short_description", "description", "tags", "created_at", "updated_at"}


class TestAPIRoutes(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app=app)
        self.valid_post_id = "11bqxc9dcca5d9d0b6c2ef6f"

    @patch("src.services.post_service.PostService.get_all_posts")
    def test_get_posts(self, mock_get_all_posts):
        mock_get_all_posts.return_value = mock_post_data

        response = self.client.get("/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

        for post in response.json():
            self.assertSetEqual(set(post.keys()), expected_keys_get_posts)

    @patch("src.services.post_service.PostService.get_post_by_id")
    def test_get_post(self, mock_get_post_by_id):
        mock_get_post_by_id.return_value = mock_post_data[0]

        # Assuming you have a valid post ID, replace 'valid_post_id' with a real ID
        response = self.client.get("/posts/valid_post_id")
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(set(response.json().keys()), expected_keys_get_post)

    @patch("src.services.post_service.PostService.delete_post_by_id")
    def test_delete_post(self, mock_delete_post_by_id):
        mock_delete_post_by_id.return_value = mock_post_data[0]

        response = self.client.delete(f"/posts/delete/{self.valid_post_id}")
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(set(response.json().keys()), expected_keys_delete_post)

    @patch("src.services.post_service.PostService.update_post_full_data")
    def test_update_post_full(self, mock_update_post_full_data):
        mock_update_post_full_data.return_value = mock_post_data[0]

        # Assuming you have a valid post ID, replace 'valid_post_id' with a real ID
        response = self.client.put(f"/posts/full-update/{self.valid_post_id}", json=mock_post_data[0])
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(set(response.json().keys()), expected_keys_update_post_full)

    @patch("src.services.post_service.PostService.update_post_partial_data")
    def test_update_post_partial(self, mock_update_post_partial_data):
        mock_update_post_partial_data.return_value = mock_post_data[0]

        # Assuming you have a valid post ID, replace 'valid_post_id' with a real ID
        partial_data = {"title": "Updated Title"}
        response = self.client.patch(f"/posts/partial-update/{self.valid_post_id}", json=partial_data)
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(set(response.json().keys()), expected_keys_update_post_partial)

    @patch("src.services.post_service.PostService.add_new_post")
    def test_add_post(self, mock_add_new_post):
        new_post_data = {
            "title": "New Post",
            "short_description": "Short description of New Post",
            "description": "Description of New Post",
            "tags": ["tag5", "tag6"],
            "created_at": "2023-07-26T14:00:00.000Z",
            "updated_at": "2023-07-26T14:30:00.000Z",
        }
        mock_add_new_post.return_value = new_post_data

        response = self.client.post("/posts/add", json=new_post_data)
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(set(response.json().keys()), expected_keys_add_post)
