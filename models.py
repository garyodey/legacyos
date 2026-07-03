from pydantic import BaseModel, Field
from typing import Optional, List


class Person(BaseModel):
    name: str
    birth_date: Optional[str] = None
    generation: Optional[int] = None
    role: Optional[str] = None
    location: Optional[str] = None


class Land(BaseModel):
    location: str
    acreage: Optional[str] = None
    survey_status: Optional[str] = None
    ownership_branch: Optional[str] = None
    notes: Optional[str] = None


class MemoryRecord(BaseModel):
    elder: str
    topic: str
    recorded: bool = False
    urgency: str = "Medium"
    notes: Optional[str] = None


class Risk(BaseModel):
    risk_type: str
    severity: str = "Medium"
    description: str
    affected_area: Optional[str] = None


class Remittance(BaseModel):
    sender: str
    receiver: str
    amount: float
    currency: str = "USD"
    exchange_rate: Optional[float] = None
    purpose: Optional[str] = None


class ContinuityScore(BaseModel):
    memory_score: float
    adaptive_score: float
    erosion_score: float
    continuity_index: float
    state: str


class Intervention(BaseModel):
    priority: str
    action: str
    reason: str
