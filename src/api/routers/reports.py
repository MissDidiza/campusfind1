"""
reports.py — Report API Router
================================
RESTful endpoints for lost and found report management.
Base path: /api/reports
"""
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import date
from api.schemas import (
    CreateReportRequest, UpdateReportRequest,
    ReportResponse, MessageResponse, ErrorResponse,
)
from api.dependencies import get_report_service
from services.report_service import ReportService
from services.exceptions import (
    ReportNotFoundException,
    ReportNotEditableException,
    ReportValidationException,
    UnauthorisedActionException,
)

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.post(
    "/",
    response_model=ReportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a lost or found item report",
    description=(
        "Creates a new report. report_type must be 'LOST' or 'FOUND'. "
        "BR-02: description must be at least 20 characters. "
        "AI matching is triggered automatically after submission."
    ),
    responses={
        201: {"description": "Report created"},
        400: {"model": ErrorResponse, "description": "Validation error"},
    },
)
def create_report(
    body: CreateReportRequest,
    svc: ReportService = Depends(get_report_service),
):
    try:
        report = svc.create_report(
            user_id=body.user_id,
            report_type=body.report_type,
            item_name=body.item_name,
            category=body.category,
            description=body.description,
            location=body.location,
            date_lost_or_found=body.date_lost_or_found,
        )
        return _to_response(report)
    except ReportValidationException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/",
    response_model=list[ReportResponse],
    summary="Get all reports",
    description="Returns all reports in the system. Admin use.",
)
def get_all_reports(svc: ReportService = Depends(get_report_service)):
    return [_to_response(r) for r in svc.get_all()]


@router.get(
    "/open/lost",
    response_model=list[ReportResponse],
    summary="Get all open lost reports",
    description="Returns all lost reports with status OPEN. Used by the AI matching engine.",
)
def get_open_lost(svc: ReportService = Depends(get_report_service)):
    return [_to_response(r) for r in svc.get_open_lost_reports()]


@router.get(
    "/open/found",
    response_model=list[ReportResponse],
    summary="Get all open found reports",
)
def get_open_found(svc: ReportService = Depends(get_report_service)):
    return [_to_response(r) for r in svc.get_open_found_reports()]


@router.get(
    "/user/{user_id}",
    response_model=list[ReportResponse],
    summary="Get all reports by a specific user",
    responses={200: {"description": "Reports found"}},
)
def get_by_user(user_id: str, svc: ReportService = Depends(get_report_service)):
    return [_to_response(r) for r in svc.get_by_user(user_id)]


@router.get(
    "/{report_id}",
    response_model=ReportResponse,
    summary="Get a report by ID",
    responses={
        200: {"description": "Report found"},
        404: {"model": ErrorResponse, "description": "Report not found"},
    },
)
def get_report(report_id: str, svc: ReportService = Depends(get_report_service)):
    try:
        return _to_response(svc.get_by_id(report_id))
    except ReportNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/{report_id}",
    response_model=ReportResponse,
    summary="Update a report",
    description=(
        "Update item_name, description, or location. "
        "BR-06: Cannot edit reports in MATCHED status or beyond."
    ),
    responses={
        200: {"description": "Report updated"},
        400: {"model": ErrorResponse, "description": "Validation error or report locked"},
        403: {"model": ErrorResponse, "description": "Not your report"},
        404: {"model": ErrorResponse, "description": "Report not found"},
    },
)
def update_report(
    report_id: str,
    body: UpdateReportRequest,
    svc: ReportService = Depends(get_report_service),
):
    try:
        report = svc.update_report(
            report_id=report_id,
            user_id=body.user_id,
            item_name=body.item_name,
            description=body.description,
            location=body.location,
        )
        return _to_response(report)
    except ReportNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UnauthorisedActionException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except (ReportNotEditableException, ReportValidationException) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/{report_id}",
    response_model=MessageResponse,
    summary="Delete (soft-delete) a report",
    responses={
        200: {"description": "Report deleted"},
        400: {"model": ErrorResponse, "description": "Report is locked"},
        403: {"model": ErrorResponse, "description": "Not your report"},
        404: {"model": ErrorResponse, "description": "Report not found"},
    },
)
def delete_report(
    report_id: str,
    user_id: str,
    svc: ReportService = Depends(get_report_service),
):
    try:
        svc.delete_report(report_id, user_id)
        return {"message": f"Report '{report_id}' has been deleted."}
    except ReportNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UnauthorisedActionException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ReportNotEditableException as e:
        raise HTTPException(status_code=400, detail=str(e))


def _to_response(report) -> dict:
    return {
        "report_id": report.report_id,
        "user_id": report.user_id,
        "report_type": report.report_type.value,
        "item_name": report.item_name,
        "category": report.category.value,
        "description": report.description,
        "location": report.location,
        "status": report.status.value,
    }
