import json
from pathlib import Path
import pytest

from app.models import (
    DiamondDetail,
    Summary,
)
from app.utils import (
    build_summary,
    extract_diamond_data,
)


@pytest.mark.parametrize(
    "mock_response_path, expected_output",
    [
        (
            Path(__file__).parent.parent / "test_data" / "mock_tracr_response.json",
            [
                DiamondDetail(diamond_id="diamond_1_id", rough_carat=1.2, polished_carat=1.0, difference=0.2),
                DiamondDetail(diamond_id="diamond_2_id", rough_carat=1.0, polished_carat=0.75, difference=0.25),
                DiamondDetail(diamond_id="diamond_3_id", rough_carat=1.8, polished_carat=1.5, difference=0.3),
            ]
        )
    ]
)
def test_extract_diamond_data_from_file(mock_response_path, expected_output):
    with open(mock_response_path, "r") as f:
        tracr_response = json.load(f)
    result = extract_diamond_data(tracr_response)
    assert result == expected_output


@pytest.mark.parametrize(
    "diamonds, expected_summary",
    [
        (
            [
                DiamondDetail(diamond_id="diamond_1_id", rough_carat=1.2, polished_carat=1.0, difference=0.2),
                DiamondDetail(diamond_id="diamond_2_id", rough_carat=1.0, polished_carat=0.75, difference=0.25),
                DiamondDetail(diamond_id="diamond_3_id", rough_carat=1.8, polished_carat=1.5, difference=0.3),
            ],
            Summary(
                total_diamonds=3,
                mean_difference=0.25,
                min_difference=0.2,
                max_difference=0.3,
                min_diff_diamond_ids=["diamond_1_id"],
                max_diff_diamond_ids=["diamond_3_id"],
            ),
        )
    ]
)
def test_build_summary(diamonds, expected_summary):
    result = build_summary(diamonds)
    assert result == expected_summary
