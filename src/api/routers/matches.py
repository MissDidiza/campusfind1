"""
matches.py — Match Record API Router
======================================
RESTful endpoints for AI match record management.
Base path: /api/matches
"""
from fastapi import APIRouter, Depends, HTTPException, status
from api.schemas import (
    CreateMatchRequest, ConfirmMatchRequest, DismissMatchRequest,
    MatchResponse, MessageResponse, ErrorResponse,
)
from api.dependencies import get_match_service
from services.match_service import MatchService
from services.exceptions import (
    MatchNotFoundException,
    MatchAlreadyResolvedException,
    ReportNotFoundException,
)

router = APIRouter(prefix="/api/matches", tags=["Matches"])


@router.post(
    "/",
    response_model=MatchResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new AI match record",
    description=(
        "Called by the AI Matching Service when a probable match is found. "
        "BR-04: Only matches with confidence >= 70% are persisted. "
        "BR-05: confidence = text_similarity*0.6 + image_similarity*0.4."
    ),
    responses={
        201: {"description": "Match created"},
        400: {"model": ErrorResponse, "description": "Below confidence threshold"},
        404: {"model": ErrorResponse, "description": "Report not found"},
    },
)
def create_match(
    body: CreateMatchRequest,
    svc: MatchService = Depends(get_match_service),
):
    try:
        match = svc.create_match(
            lost_report_id=body.lost_report_id,
            found_report_id=body.found_report_id,
            text_similarity=body.text_similarity,
            image_similarity=body.image_similarity,
        )
        return _to_response(match)
    except ReportNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/",
    response_model=list[MatchResponse],
    summary="Get all match records",
)
def get_all(svc: MatchService = Depends(get_match_service)):
    return [_to_response(m) for m in svc.get_all()]


@router.get(
    "/pending",
    response_model=list[MatchResponse],
    summary="Get all pending matches for admin review",
    description="Returns NOTIFIED and PENDING_REVIEW matches sorted by confidence score (highest first).",
)
def get_pending(svc: MatchService = Depends(get_match_service)):
    return [_to_response(m) for m in svc.get_pending_for_admin()]


@router.get(
    "/{match_id}",
    response_model=MatchResponse,
    summary="Get a match record by ID",
    responses={
        200: {"description": "Match found"},
        404: {"model": ErrorResponse, "description": "Match not found"},
    },
)
def get_match(match_id: str, svc: MatchService = Depends(get_match_service)):
    try:
        return _to_response(svc.get_by_id(match_id))
    except MatchNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post(
    "/{match_id}/confirm",
    response_model=MatchResponse,
    summary="Admin confirms a match",
    description=(
        "Marks the match as CONFIRMED and updates both associated reports to MATCHED status. "
        "Reports are locked from editing (BR-06)."
    ),
    responses={
        200: {"description": "Match confirmed"},
        400: {"model": ErrorResponse, "description": "Match already resolved"},
        404: {"model": ErrorResponse, "description": "Match not found"},
    },
)
def confirm_match(
    match_id: str,
    body: ConfirmMatchRequest,
    svc: MatchService = Depends(get_match_service),
):
    try:
        match = svc.confirm_match(match_id, body.admin_id)
        return _to_response(match)
    except MatchNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except MatchAlreadyResolvedException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/{match_id}/dismiss",
    response_model=MatchResponse,
    summary="Admin dismisses a false match",
    description=(
        "Marks the match as DISMISSED. Reason is required. "
        "Both reports revert to OPEN status."
    ),
    responses={
        200: {"description": "Match dismissed"},
        400: {"model": ErrorResponse, "description": "Missing reason or already resolved"},
        404: {"model": ErrorResponse, "description": "Match not found"},
    },
)
def dismiss_match(
    match_id: str,
    body: DismissMatchRequest,
    svc: MatchService = Depends(get_match_service),
):
    try:
        match = svc.dismiss_match(match_id, body.admin_id, body.reason)
        return _to_response(match)
    except MatchNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except MatchAlreadyResolvedException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def _to_response(match) -> dict:
    return {
        "match_id": match.match_id,
        "lost_report_id": match.lost_report_id,
        "found_report_id": match.found_report_id,
        "confidence_score": match.confidence_score,
        "text_similarity_score": match.text_similarity_score,
        "image_similarity_score": match.image_similarity_score,
        "status": match.status.value,
    }
