from fastapi.testclient import TestClient
from src import main
import unittest


class TestService(unittest.TestCase):
    def setUp(self) -> None:
        self.api_client = TestClient(app=main.app)

    def test_health_check(self):
        response = self.api_client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Health Check!")
