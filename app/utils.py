from typing import List
from app.models import (
    DiamondDetail,
    Summary,
    TracrResponse,
)
from statistics import mean


def extract_diamond_data(tracr_response: dict) -> List[DiamondDetail]:
    diamonds: List[DiamondDetail] = []
    tracr_data = TracrResponse.parse_obj(tracr_response)

    for result in tracr_data.results:
        diamond_list = result.diamonds.property1.results.property1

        for diamond in diamond_list:
            diamond_id = diamond.diamond_id
            rough_carat = diamond.rough.carats if diamond.rough else 0.0
            polished_carat = diamond.polished.carats if diamond.polished else 0.0
            difference = round(rough_carat - polished_carat, 4)

            diamonds.append(DiamondDetail(
                diamond_id=diamond_id,
                rough_carat=rough_carat,
                polished_carat=polished_carat,
                difference=difference
            ))

    return diamonds


def build_summary(diamonds: List[DiamondDetail]) -> Summary:
    if not diamonds:
        return Summary(
            total_diamonds=0,
            mean_difference=0.0,
            min_difference=0.0,
            max_difference=0.0,
            min_diff_diamond_ids=[],
            max_diff_diamond_ids=[],
        )

    diffs = [d.difference for d in diamonds]
    min_diff = min(diffs)
    max_diff = max(diffs)

    return Summary(
        total_diamonds=len(diamonds),
        mean_difference=round(mean(diffs), 4),
        min_difference=round(min_diff, 4),
        max_difference=round(max_diff, 4),
        min_diff_diamond_ids=[d.diamond_id for d in diamonds if d.difference == min_diff],
        max_diff_diamond_ids=[d.diamond_id for d in diamonds if d.difference == max_diff],
    )
