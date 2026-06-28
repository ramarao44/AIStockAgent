import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PYTHON_ROOT = PROJECT_ROOT / "Python"
if str(PYTHON_ROOT) not in sys.path:
    sys.path.insert(0, str(PYTHON_ROOT))

from fastapi.testclient import TestClient

from api.app import app


class ApiTests(unittest.TestCase):
    def test_health_endpoint(self):
        client = TestClient(app)
        response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_analyze_stock_endpoint(self):
        client = TestClient(app)
        response = client.post("/analyze-stock", json={"symbol": "RELIANCE.NS"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("symbol", response.json())
        self.assertIn("decision", response.json())


if __name__ == "__main__":
    unittest.main()
