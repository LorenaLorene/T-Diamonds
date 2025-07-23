from fastapi import APIRouter, HTTPException
from app.models import Diamond, DiamondDetailsResponse
from app.config import settings
from app.errors import (
    FORBIDDEN_ERROR,
    TRACR_ERROR,
    UNAUTHORIZED_ERROR,
    VALIDATION_ERROR,
)
from typing import List
import requests
import logging


from app.utils import (
    build_summary,
    extract_diamond_data,
)

router = APIRouter()
logger = logging.getLogger(__name__)


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
            headers=headers,
            timeout=10
        )
    except requests.RequestException as e:
        logger.error(TRACR_ERROR + f": {e}")
        raise HTTPException(status_code=502, detail=TRACR_ERROR)

    if resp.status_code == 401:
        logger.warning(UNAUTHORIZED_ERROR)
        raise HTTPException(status_code=502, detail=UNAUTHORIZED_ERROR)
    elif resp.status_code == 403:
        logger.warning(FORBIDDEN_ERROR)
        raise HTTPException(status_code=502, detail=FORBIDDEN_ERROR)
    elif resp.status_code == 422:
        error_body = resp.json()
        logger.warning(VALIDATION_ERROR + f": {error_body}")
        raise HTTPException(
            status_code=502,
            detail=error_body.get("detail", VALIDATION_ERROR)
        )
    elif resp.status_code != 200:
        logger.error(f"Unexpected Tracr error {resp.status_code}: {resp.text}")
        raise HTTPException(
            status_code=502,
            detail=f"Unexpected error from Tracr API (status {resp.status_code})"
        )

    try:
        tracr_data = resp.json()
    except ValueError as e:
        logger.error(f"Invalid JSON response from Tracr: {e}")
        raise HTTPException(status_code=502, detail="Invalid response from Tracr API.")

    diamonds = extract_diamond_data(tracr_data)
    summary_data = build_summary(diamonds)

    return DiamondDetailsResponse(
        diamonds=diamonds,
        summary=summary_data
    )
