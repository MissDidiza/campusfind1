"""
reports.py — Report API Router
================================
RESTful endpoints for lost and found report management.
Base path: /api/reports
"""
import csv
from io import StringIO
from fastapi import APIRouter, Depends, HTTPException, status, Response
from datetime import date
from typing import Optional
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


@router.get(
    "/export/csv",
    response_class=Response,
    summary="Export reports as CSV",
    description=(
        "Exports reports in CSV format with optional filtering. "
        "Query parameters: user_id (filter by user), status (filter by status), "
        "report_type (filter by LOST or FOUND). CSV file is returned for download."
    ),
    responses={
        200: {
            "content": {"text/csv": {}},
            "description": "CSV file containing reports",
        },
    },
)
def export_reports_csv(
    user_id: Optional[str] = None,
    status: Optional[str] = None,
    report_type: Optional[str] = None,
    svc: ReportService = Depends(get_report_service),
):
    """
    Export reports as CSV file with optional filtering.
    
    Query parameters:
    - user_id: Filter by specific user
    - status: Filter by report status (e.g., OPEN, MATCHED)
    - report_type: Filter by report type (LOST or FOUND)
    """
    try:
        # Get all reports first
        reports = svc.get_all()
        
        # Apply filters
        if user_id:
            reports = [r for r in reports if r.user_id == user_id]
        if status:
            reports = [r for r in reports if r.status.value == status.upper()]
        if report_type:
            reports = [r for r in reports if r.report_type.value == report_type.upper()]
        
        # Create CSV content
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            "Report ID",
            "User ID",
            "Report Type",
            "Item Name",
            "Category",
            "Description",
            "Location",
            "Status",
            "Created At",
        ])
        
        # Write data rows
        for report in reports:
            writer.writerow([
                report.report_id,
                report.user_id,
                report.report_type.value,
                report.item_name,
                report.category.value,
                report.description,
                report.location,
                report.status.value,
                report.created_at.isoformat(),
            ])
        
        csv_content = output.getvalue()
        
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=reports.csv"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error exporting CSV: {str(e)}"
        )


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
