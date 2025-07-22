from pydantic import BaseModel
from typing import List, Optional


# Tracr API models
class Polished(BaseModel):
    carats: float
    clarity: Optional[str]
    colour: Optional[str]
    cut_grade: Optional[str]


class Rough(BaseModel):
    carats: float


class TracrDiamond(BaseModel):
    assurance_level: Optional[str]
    current_stage: Optional[str]
    diamond_id: str
    diamond_parent_id: Optional[str]
    lifecycle_state: Optional[str]
    polished: Polished
    rough: Rough


class ResultsProperty1(BaseModel):
    property1: List[TracrDiamond]
    property2: Optional[List] = []


class DiamondsProperty1(BaseModel):
    results: ResultsProperty1


class Diamonds(BaseModel):
    property1: DiamondsProperty1
    property2: Optional[dict] = {}


class Result(BaseModel):
    diamonds: Diamonds
    platform_id: Optional[str]
    status: Optional[str]


class TracrResponse(BaseModel):
    results: List[Result]


# internal API models
class Diamond(BaseModel):
    diamond_id: str


class DiamondDetail(BaseModel):
    diamond_id: str
    rough_carat: float
    polished_carat: float
    difference: float
    """Weight difference between rough and polished diamond."""


class Summary(BaseModel):
    total_diamonds: int
    mean_difference: float
    min_difference: float
    max_difference: float
    min_diff_diamond_ids: List[str]
    max_diff_diamond_ids: List[str]


class DiamondDetailsResponse(BaseModel):
    diamonds: List[DiamondDetail]
    summary: Summary
