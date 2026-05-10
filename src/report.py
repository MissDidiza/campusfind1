"""
report.py — Report domain entity.
Maps to Report class in CLASS_DIAGRAM.md.
Traces to FR-03, FR-04, FR-05 and US-003, US-004, US-005.
"""
import uuid
from datetime import datetime, date
from typing import List, Optional
from src.enums import ReportType, ReportStatus, ItemCategory
from src.photo import Photo

MAX_PHOTOS = 3
MIN_DESCRIPTION_LENGTH = 20

# States where a report can no longer be edited (BR-06)
LOCKED_STATUSES = {
    ReportStatus.MATCHED,
    ReportStatus.HANDOVER_PENDING,
    ReportStatus.RESOLVED,
    ReportStatus.ESCALATED,
    ReportStatus.UNCLAIMED,
    ReportStatus.ARCHIVED,
}


class Report:
    """Central entity — represents a lost or found item report."""

    def __init__(
        self,
        user_id: str,
        report_type: ReportType,
        item_name: str,
        category: ItemCategory,
        description: str,
        location: str,
        date_lost_or_found: date,
    ):
        self._report_id: str = str(uuid.uuid4())
        self._user_id: str = user_id
        self._type: ReportType = report_type
        self._item_name: str = item_name
        self._category: ItemCategory = category
        self._description: str = description
        self._location: str = location
        self._date_lost_or_found: date = date_lost_or_found
        self._status: ReportStatus = ReportStatus.OPEN
        self._photos: List[Photo] = []
        self._created_at: datetime = datetime.utcnow()
        self._updated_at: datetime = datetime.utcnow()

    # ── Properties ────────────────────────────────────────────────

    @property
    def report_id(self) -> str:
        return self._report_id

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def report_type(self) -> ReportType:
        return self._type

    @property
    def item_name(self) -> str:
        return self._item_name

    @property
    def category(self) -> ItemCategory:
        return self._category

    @property
    def description(self) -> str:
        return self._description

    @property
    def location(self) -> str:
        return self._location

    @property
    def status(self) -> ReportStatus:
        return self._status

    @property
    def photos(self) -> List[Photo]:
        return list(self._photos)

    @property
    def created_at(self) -> datetime:
        return self._created_at

    # ── Methods ───────────────────────────────────────────────────

    def validate(self) -> bool:
        """BR-02: Description must be at least 20 characters."""
        if not self._item_name or not self._item_name.strip():
            raise ValueError("Item name is required.")
        if len(self._description) < MIN_DESCRIPTION_LENGTH:
            raise ValueError(
                f"Description must be at least {MIN_DESCRIPTION_LENGTH} characters."
            )
        if not self._location or not self._location.strip():
            raise ValueError("Location is required.")
        return True

    def add_photo(self, photo: Photo) -> None:
        """BR-03: Maximum 3 photos per report."""
        if len(self._photos) >= MAX_PHOTOS:
            raise ValueError(f"A report can have a maximum of {MAX_PHOTOS} photos.")
        self._photos.append(photo)

    def update_status(self, new_status: ReportStatus) -> None:
        self._status = new_status
        self._updated_at = datetime.utcnow()

    def is_editable(self) -> bool:
        """BR-06: Cannot be edited once MATCHED or beyond."""
        return self._status not in LOCKED_STATUSES

    def trigger_matching(self) -> None:
        """Signal that AI matching should run for this report."""
        if self._status == ReportStatus.OPEN:
            self.update_status(ReportStatus.MATCHING)

    def archive(self) -> None:
        self.update_status(ReportStatus.ARCHIVED)

    def soft_delete(self) -> None:
        if not self.is_editable():
            raise RuntimeError("Cannot delete a report that is matched or resolved.")
        self._status = ReportStatus.ARCHIVED

    def to_match_payload(self) -> dict:
        """Serialize report data for the AI Matching Service."""
        return {
            "report_id": self._report_id,
            "type": self._type.value,
            "item_name": self._item_name,
            "category": self._category.value,
            "description": self._description,
            "location": self._location,
            "photo_urls": [p.fetch_for_analysis() for p in self._photos if not p.is_deleted],
        }

    def __repr__(self) -> str:
        return (
            f"Report(id={self._report_id[:8]}, type={self._type.value}, "
            f"item='{self._item_name}', status={self._status.value})"
        )