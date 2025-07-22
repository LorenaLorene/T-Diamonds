from fastapi import APIRouter, HTTPException
from app.models import Diamond, DiamondDetailsResponse
from app.config import settings
from app.errors import TRACR_ERROR
from typing import List
import requests


from app.utils import (
    build_summary,
    extract_diamond_data,
)

router = APIRouter()


@router.post("/diamond_details", response_model=DiamondDetailsResponse)
def get_diamond_details(diamonds: List[Diamond]):
    headers = {
        "Authorization": f"Bearer {settings.BEARER_TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    tracr_request_payload = {
        "data": [
            {
                "diamonds": diamonds,
                "modified_since": "1970-01-01T00:00:00",
                "platform_id": settings.PLATFORM_ID
            }
        ]
    }

    try:
        resp = requests.post(
            settings.TRACR_BULK_URL,
            json=tracr_request_payload,
            headers=headers
        )
        resp.raise_for_status()
    except requests.RequestException:
        raise HTTPException(status_code=502, detail=TRACR_ERROR)

    tracr_data = resp.json()
    diamonds = extract_diamond_data(tracr_data)
    summary_data = build_summary(diamonds)

    return DiamondDetailsResponse(
        diamonds=diamonds,
        summary=summary_data
    )
