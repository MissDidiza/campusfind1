"""
schemas.py — Pydantic Request/Response Schemas
================================================
These schemas define the shape of API request bodies and responses.
Pydantic validates all incoming data automatically.
FastAPI uses these to generate the OpenAPI/Swagger documentation.
"""
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import date
from enum import Enum


# ── Request Schemas ───────────────────────────────────────────────

class RegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters.")
        return v

    model_config = {"json_schema_extra": {
        "example": {
            "full_name": "Iminathi Didiza",
            "email": "iminathi@university.ac.za",
            "password": "SecurePass123"
        }
    }}


class LoginRequest(BaseModel):
    email: str
    password: str

    model_config = {"json_schema_extra": {
        "example": {
            "email": "iminathi@university.ac.za",
            "password": "SecurePass123"
        }
    }}


class UpdateProfileRequest(BaseModel):
    full_name: str


class UpdateRoleRequest(BaseModel):
    new_role: str  # STUDENT, ADMIN, SUPER_ADMIN


class CreateReportRequest(BaseModel):
    user_id: str
    report_type: str        # LOST or FOUND
    item_name: str
    category: str           # ELECTRONICS, CLOTHING, etc.
    description: str
    location: str
    date_lost_or_found: date

    model_config = {"json_schema_extra": {
        "example": {
            "user_id": "abc-123",
            "report_type": "LOST",
            "item_name": "Black Nike Backpack",
            "category": "ACCESSORIES",
            "description": "Black Nike backpack with broken zip on left pocket and UCT keyring attached",
            "location": "Library Second Floor",
            "date_lost_or_found": "2026-03-10"
        }
    }}


class UpdateReportRequest(BaseModel):
    user_id: str
    item_name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None


class CreateMatchRequest(BaseModel):
    lost_report_id: str
    found_report_id: str
    text_similarity: float
    image_similarity: float

    model_config = {"json_schema_extra": {
        "example": {
            "lost_report_id": "lost-uuid-here",
            "found_report_id": "found-uuid-here",
            "text_similarity": 0.88,
            "image_similarity": 0.75
        }
    }}


class ConfirmMatchRequest(BaseModel):
    admin_id: str


class DismissMatchRequest(BaseModel):
    admin_id: str
    reason: str


# ── Response Schemas ──────────────────────────────────────────────

class UserResponse(BaseModel):
    user_id: str
    full_name: str
    email: str
    role: str
    is_verified: bool

    model_config = {"from_attributes": True}


class ReportResponse(BaseModel):
    report_id: str
    user_id: str
    report_type: str
    item_name: str
    category: str
    description: str
    location: str
    status: str

    model_config = {"from_attributes": True}


class MatchResponse(BaseModel):
    match_id: str
    lost_report_id: str
    found_report_id: str
    confidence_score: float
    text_similarity_score: float
    image_similarity_score: float
    status: str

    model_config = {"from_attributes": True}


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    detail: str
