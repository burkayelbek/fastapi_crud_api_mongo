import unittest
from pymongo.errors import ConnectionFailure
from unittest.mock import MagicMock, patch
from src.config.database import DatabaseConnection
from src.config.settings import settings
from src import main


class DatabaseTestService(unittest.TestCase):

    def setUp(self):
        self.database_service = DatabaseConnection()

    def tearDown(self) -> None:
        self.database_service.connected = False

    @patch('pymongo.MongoClient')
    def test_get_connection_successful(self, mock_mongo_client):
        self.database_service.connected = False
        mock_mongo_client.return_value = MagicMock()

        connection = self.database_service.get_connection()

        self.assertTrue(self.database_service.connected)
        self.assertEqual(connection, self.database_service.client)

    @patch('pymongo.MongoClient')
    def test_get_collection_existing_collection(self, mock_mongo_client):
        self.database_service.connected = False
        mock_client_instance = MagicMock()
        mock_mongo_client.return_value = mock_client_instance

        mock_mongo_client.return_value = MagicMock()
        self.database_service.get_connection()

        self.database_service.get_connection()

        collection_name = "posts"
        mock_client_instance[self.database_service.database].list_collection_names.return_value = [
            collection_name]

        collection = self.database_service.get_collection(collection_name=collection_name)

        self.assertEqual(collection, self.database_service.database_instance[collection_name])

    def test_create_db_url(self):
        self.database_service.user = "user"
        self.database_service.password = "password"
        self.database_service.host = "localhost"
        self.database_service.port = 27017
        self.database_service.database = "mydb"

        db_url = self.database_service._create_db_url()

        expected_url = "mongodb://user:password@localhost:27017/?authMechanism=DEFAULT&authSource=mydb"
        self.assertEqual(db_url, expected_url)