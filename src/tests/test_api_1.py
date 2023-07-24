import unittest

from bson import ObjectId
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.routers.post_router import router, db
import uuid
from datetime import datetime, timedelta

client = TestClient(app=router)


class TestPostsRouter(unittest.TestCase):

    def setUp(self):
        # Mock the database collection
        self.collection_mock = MagicMock()
        db.get_collection = MagicMock(return_value=self.collection_mock)

    def test_get_posts(self):
        # Mock the database find method to return some sample posts

        response = client.get("/posts/")
        # Check if data is returned
        self.assertTrue(response.json())
        # Check if data is returned as a list
        self.assertIsInstance(response.json(), list)
        # Define the expected keys
        expected_keys = {"_id", "title", "short_description", "description", "tags", "created_at", "updated_at"}
        for post in response.json():
            self.assertEqual(post.keys(), expected_keys)
        self.assertEqual(response.status_code, 200)

    def test_get_post(self):
        # Define the sample post id
        sample_post_id = "64bbbc9dcca5d9d0b6c2ef6f"

        response = client.get(f"/posts/{sample_post_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "string2")

    def test_get_post_invalid_id(self):
        pass

    def test_get_post_not_found(self):
        pass

    def test_add_post(self):
        pass

    def test_update_post_full(self):
        pass

    def test_update_post_full_invalid_id(self):
        pass

    def test_update_post_full_not_found(self):
        pass

    def test_delete_post(self):
        pass

    def test_delete_post_invalid_id(self):
        pass

    def test_delete_post_not_found(self):
        pass


if __name__ == "__main__":
    unittest.main()
