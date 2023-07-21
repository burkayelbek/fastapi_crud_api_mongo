from pymongo.mongo_client import MongoClient
from pymongo.errors import ConnectionFailure
from src.config.settings import settings


class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        self.DB_URL = self._create_db_url()
        self.client = None
        self.connected = False

    def get_connection(self) -> dict:
        if self.connected:
            return {"client": self.client, "collection_names": self.client[settings.mongodb_db].list_collection_names()}

        self.client = MongoClient(self.DB_URL)
        try:
            self.client[settings.mongodb_db].command('ping')
            print("Successfully connected to MongoDB")
            self.connected = True
        except ConnectionFailure as e:
            print("Connection to MongoDB failed:", e)
        return {"client": self.client, "collection_names": self.client[settings.mongodb_db].list_collection_names()}

    def get_collection(self, collection_name=None):
        if collection_name is None:
            return None
        collection_info = self.get_connection()
        collection_names = collection_info.get("collection_names")

        matched = next((cn for cn in collection_names if collection_name == cn), None)
        if not matched:
            raise ValueError(f"Collection '{matched}' not found.")
        return matched

    def _create_db_url(self):
        return f"mongodb://{settings.mongodb_user}:" \
               f"{settings.mongodb_password}@" \
               f"{settings.mongodb_host}:" \
               f"{settings.mongodb_port}/?authMechanism=DEFAULT&authSource={settings.mongodb_db}"