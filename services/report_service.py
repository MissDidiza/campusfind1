"""
report_service.py — Report Service
=====================================
Handles all business logic for lost and found report submission,
retrieval, updates, and deletion.

Business rules enforced:
- BR-02: Description >= 20 characters
- BR-03: Max 3 photos per report
- BR-06: Reports cannot be edited once MATCHED or beyond
- FR-03/04: AI matching job triggered on submission

Traces to FR-03, FR-04, FR-05 | US-003, US-004, US-005
"""
from datetime import date
from typing import List, Optional
from src.report import Report
from src.photo import Photo
from src.enums import ReportType, ReportStatus, ItemCategory
from repositories.interfaces import ReportRepository, PhotoRepository
from services.exceptions import (
    ReportNotFoundException,
    ReportNotEditableException,
    ReportValidationException,
    UnauthorisedActionException,
)


class ReportService:
    """Encapsulates all business logic for Report management."""

    def __init__(
        self,
        report_repository: ReportRepository,
        photo_repository: PhotoRepository,
    ):
        self._report_repo = report_repository
        self._photo_repo = photo_repository

    # ── Create ────────────────────────────────────────────────────

    def create_report(
        self,
        user_id: str,
        report_type: str,
        item_name: str,
        category: str,
        description: str,
        location: str,
        date_lost_or_found: date,
    ) -> Report:
        """
        Create and persist a new lost or found report.
        Validates all fields before saving.
        Triggers AI matching status on save.
        """
        try:
            rtype = ReportType[report_type.upper()]
        except KeyError:
            raise ReportValidationException(
                f"Invalid report type '{report_type}'. Must be LOST or FOUND."
            )
        try:
            cat = ItemCategory[category.upper()]
        except KeyError:
            raise ReportValidationException(
                f"Invalid category '{category}'. "
                f"Valid: {[c.value for c in ItemCategory]}"
            )

        report = Report(
            user_id=user_id,
            report_type=rtype,
            item_name=item_name.strip(),
            category=cat,
            description=description.strip(),
            location=location.strip(),
            date_lost_or_found=date_lost_or_found,
        )

        try:
            report.validate()
        except ValueError as e:
            raise ReportValidationException(str(e))

        self._report_repo.save(report)
        return report

    def add_photo_to_report(
        self,
        report_id: str,
        user_id: str,
        cloudinary_url: str,
        cloudinary_public_id: str,
        file_size_kb: int,
        mime_type: str,
    ) -> Photo:
        """Add a photo to an existing report. Max 3 photos enforced."""
        report = self._get_or_raise(report_id)

        if report.user_id != user_id:
            raise UnauthorisedActionException(
                "You can only add photos to your own reports."
            )
        if not report.is_editable():
            raise ReportNotEditableException(report_id, report.status.value)

        try:
            Photo.validate(file_size_kb, mime_type)
        except ValueError as e:
            raise ReportValidationException(str(e))

        existing = self._photo_repo.find_active_by_report_id(report_id)
        if len(existing) >= 3:
            raise ReportValidationException(
                "A report can have a maximum of 3 photos."
            )

        photo = Photo(
            report_id=report_id,
            cloudinary_url=cloudinary_url,
            cloudinary_public_id=cloudinary_public_id,
            file_size_kb=file_size_kb,
            mime_type=mime_type,
        )
        self._photo_repo.save(photo)
        report.add_photo(photo)
        self._report_repo.save(report)
        return photo

    # ── Read ──────────────────────────────────────────────────────

    def get_by_id(self, report_id: str) -> Report:
        return self._get_or_raise(report_id)

    def get_all(self) -> List[Report]:
        return self._report_repo.find_all()

    def get_by_user(self, user_id: str) -> List[Report]:
        return self._report_repo.find_by_user_id(user_id)

    def get_open_lost_reports(self) -> List[Report]:
        return self._report_repo.find_open_by_type(ReportType.LOST)

    def get_open_found_reports(self) -> List[Report]:
        return self._report_repo.find_open_by_type(ReportType.FOUND)

    def get_by_status(self, status: str) -> List[Report]:
        try:
            s = ReportStatus[status.upper()]
        except KeyError:
            raise ReportValidationException(f"Invalid status '{status}'.")
        return self._report_repo.find_by_status(s)

    # ── Update ────────────────────────────────────────────────────

    def update_report(
        self,
        report_id: str,
        user_id: str,
        item_name: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
    ) -> Report:
        """Update editable fields. Enforces BR-06 — locked if MATCHED or beyond."""
        report = self._get_or_raise(report_id)

        if report.user_id != user_id:
            raise UnauthorisedActionException(
                "You can only edit your own reports."
            )
        if not report.is_editable():
            raise ReportNotEditableException(report_id, report.status.value)

        if item_name:
            report._item_name = item_name.strip()
        if description:
            if len(description.strip()) < 20:
                raise ReportValidationException(
                    "Description must be at least 20 characters."
                )
            report._description = description.strip()
        if location:
            report._location = location.strip()

        self._report_repo.save(report)
        return report

    # ── Delete ────────────────────────────────────────────────────

    def delete_report(self, report_id: str, user_id: str) -> None:
        """Soft-delete a report. Only owner can delete. Cannot delete if locked."""
        report = self._get_or_raise(report_id)
        if report.user_id != user_id:
            raise UnauthorisedActionException(
                "You can only delete your own reports."
            )
        if not report.is_editable():
            raise ReportNotEditableException(report_id, report.status.value)
        report.soft_delete()
        self._report_repo.save(report)

    # ── Internal ──────────────────────────────────────────────────

    def _get_or_raise(self, report_id: str) -> Report:
        report = self._report_repo.find_by_id(report_id)
        if report is None:
            raise ReportNotFoundException(report_id)
        return report
