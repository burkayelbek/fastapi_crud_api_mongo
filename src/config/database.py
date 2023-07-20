from pymongo.mongo_client import MongoClient
from pymongo.errors import ConnectionFailure
from src.config.settings import settings


class DatabaseConnection:
    def __init__(self):
        self.DB_URL = self._create_db_url()

    def connection(self):
        client = MongoClient(self.DB_URL)
        try:
            client[settings.mongodb_db].command('ping')
            print("Pinged your deployment, You successfully connected to MongoDB")
        except ConnectionFailure as e:
            print("Connection to MongoDB failed:", e)

    def _create_db_url(self):
        return f"mongodb://{settings.mongodb_user}:" \
               f"{settings.mongodb_password}@" \
               f"{settings.mongodb_host}:" \
               f"{settings.mongodb_port}/?authMechanism=DEFAULT&authSource={settings.mongodb_db}"
