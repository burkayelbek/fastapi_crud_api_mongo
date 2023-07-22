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
        try:
            self.database = settings.mongodb_db
            self.user = settings.mongodb_user
            self.password = settings.mongodb_password
            self.port = settings.mongodb_port
            self.host = settings.mongodb_host
        except AttributeError as e:
            raise AttributeError("Database settings are not properly configured.", e)

        self.DB_URL = self._create_db_url()
        self.client = None
        self.connected = False

    def get_connection(self):
        if self.connected:
            return self.client

        self.client = MongoClient(self.DB_URL)
        try:
            self.client[settings.mongodb_db].command('ping')
            print("Successfully connected to MongoDB")
            self.connected = True
        except ConnectionFailure as e:
            print("Connection to MongoDB failed:", e)

        return self.client

    @property
    def database_instance(self):
        if self.database is None:
            return None
        database_instance = self.get_connection()[self.database]
        return database_instance

    def get_collection(self, collection_name=None):
        if collection_name is None:
            return None
        if not self.connected:
            try:
                self.get_connection()
            except ConnectionFailure as e:
                print("Error occured while trying to connect database:", e)

        collection_names = self.client[self.database].list_collection_names()

        matched = next((cn for cn in collection_names if collection_name == cn), None)
        if not matched:
            raise ValueError(f"Collection '{matched}' not found.")
        return self.database_instance[collection_name]

    def _create_db_url(self):
        return f"mongodb://{self.user}:" \
               f"{self.password}@" \
               f"{self.host}:" \
               f"{self.port}/?authMechanism=DEFAULT&authSource={self.database}"
