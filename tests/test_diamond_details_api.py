import json
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from pathlib import Path
from app.main import app
from app.config import settings

TRACR_BULK_URL = settings.TRACR_BULK_URL

client = TestClient(app)


@pytest.mark.parametrize(
    "request_payload, expected_response",
    [
        (
            [{"diamond_id": "diamond_1_id"},
             {"diamond_id": "diamond_2_id"},
             {"diamond_id": "diamond_3_id"}],
            {
              "diamonds": [
                {
                  "diamond_id": "diamond_1_id",
                  "rough_carat": 1.2,
                  "polished_carat": 1.0,
                  "difference": 0.2
                },
                {
                  "diamond_id": "diamond_2_id",
                  "rough_carat": 1.0,
                  "polished_carat": 0.75,
                  "difference": 0.25
                },
                {
                  "diamond_id": "diamond_3_id",
                  "rough_carat": 1.8,
                  "polished_carat": 1.5,
                  "difference": 0.3
                }
              ],
              "summary": {
                "total_diamonds": 3,
                "mean_difference": 0.25,
                "min_difference": 0.2,
                "max_difference": 0.3,
                "min_diff_diamond_ids": [
                  "diamond_1_id"
                ],
                "max_diff_diamond_ids": [
                  "diamond_3_id"
                ]
              }
            }
        ),
    ],
)
def test_diamond_details_endpoint(request_payload, expected_response):
    mock_file = Path(__file__).parent / "test_data" / "mock_tracr_response.json"
    mock_response = json.loads(mock_file.read_text())

    with patch("app.api.requests.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response
        mock_post.return_value = mock_resp

        response = client.post("/diamond_details", json=request_payload)

        assert response.status_code == 200
        assert response.json() == expected_response
