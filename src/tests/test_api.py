import unittest
from fastapi.testclient import TestClient
from src import main


class APITestService(unittest.TestCase):

    def setUp(self):
        self.api_client = TestClient(app=main.app)
