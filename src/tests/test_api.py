import unittest
import datetime
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src import main
from pymongo import MongoClient


class TestPostsAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app=main.post_router.router)
        self.post_data = {
            "_id": "11bqxc9dcca5d9d0b6c2ef6f",
            "title": "Test Post",
            "short_description": "This is a short description of post",
            "description": "This is a description of post",
            "tags": ["this is a tag"],
            "created_at": datetime.datetime.utcnow() + datetime.timedelta(hours=3),
            "updated_at": datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        }

    @patch('pymongo.MongoClient')
    def test_get_posts(self, mock_find):
        mock_find_instance = MagicMock()
        mock_find.return_value = mock_find_instance

        # mock_find.return_value = [{"_id": "11bqxc9dcca5d9d0b6c2ef6f",
        #                            "title": "Test Post",
        #                            "short_description": "This is a short description of post",
        #                            "description": "This is a description of post",
        #                            "tags": ["this is a tag"],
        #                            "created_at": datetime.datetime.utcnow() + datetime.timedelta(hours=3),
        #                            "updated_at": datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        #                            }]

        response = self.client.get("/posts/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)

    @patch.object(MongoClient, '__init__', return_value=None)
    @patch('src.routers.posts.collection.find_one')
    def test_get_post(self, mock_find_one):
        mock_find_one.return_value = {"_id": "11bqxc9dcca5d9d0b6c2ef6f",
                                      "title": "Test Post",
                                      "short_description": "This is a short description of post",
                                      "description": "This is a description of post",
                                      "tags": ["this is a tag"],
                                      "created_at": datetime.datetime.utcnow() + datetime.timedelta(hours=3),
                                      "updated_at": datetime.datetime.utcnow() + datetime.timedelta(hours=3)
                                      }

        response = self.client.get("/posts/dummy_id")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Test Post")


    @patch.object(MongoClient, '__init__', return_value=None)
    @patch('src.routers.posts.collection.insert_one')
    def test_add_post(self):
        response = self.client.post("/posts/add", json=self.post_data)
        self.assertEqual(response.status_code, 200)

    @patch.object(MongoClient, '__init__', return_value=None)
    @patch('src.routers.posts.collection.find_one_and_update')
    def test_update_post_full(self, mock_find_one_and_update):
        mock_find_one_and_update.return_value = {"_id": "11bqxc9dcca5d9d0b6c2ef6f",
                                                 "title": "Test Post",
                                                 "short_description": "This is a short description of post",
                                                 "description": "This is a description of post",
                                                 "tags": ["this is a tag"],
                                                 "created_at": datetime.datetime.utcnow() + datetime.timedelta(hours=3),
                                                 "updated_at": datetime.datetime.utcnow() + datetime.timedelta(hours=3)
                                                 }

        updated_data = {
            "title": "Updated Post",
            "content": "Updated content"
        }
        response = self.client.put("/posts/full-update/dummy_id", json=updated_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Updated Post")

    @patch.object(MongoClient, '__init__', return_value=None)
    @patch('src.routers.posts.collection.update_one')
    def test_update_post_partial(self, mock_update_one):
        # Set the return value for the mocked function
        mock_update_one.return_value = {"_id": "11bqxc9dcca5d9d0b6c2ef6f",
                                        "title": "Test Post",
                                        "short_description": "This is a short description of post",
                                        "description": "This is a description of post",
                                        "tags": ["this is a tag"],
                                        "created_at": datetime.datetime.utcnow() + datetime.timedelta(hours=3),
                                        "updated_at": datetime.datetime.utcnow() + datetime.timedelta(hours=3)
                                        }

        updated_data = {
            "title": "Updated Post"
        }
        response = self.client.patch("/posts/partial-update/dummy_id", json=updated_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Updated Post")

    @patch.object(MongoClient, '__init__', return_value=None)
    @patch('src.routers.posts.collection.find_one_and_delete')
    def test_delete_post(self, mock_find_one_and_delete):
        # Set the return value for the mocked function
        mock_find_one_and_delete.return_value = {"_id": "11bqxc9dcca5d9d0b6c2ef6f",
                                                 "title": "Test Post",
                                                 "short_description": "This is a short description of post",
                                                 "description": "This is a description of post",
                                                 "tags": ["this is a tag"],
                                                 "created_at": datetime.datetime.utcnow() + datetime.timedelta(hours=3),
                                                 "updated_at": datetime.datetime.utcnow() + datetime.timedelta(hours=3)
                                                 }

        response = self.client.delete("/posts/delete/dummy_id")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["status"])
