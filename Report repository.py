"""
report_repository.py — In-Memory Report Repository
===================================================
HashMap-based implementation of ReportRepository.
Traces to FR-03, FR-04, FR-05, FR-11 and US-003–US-005, US-011.
"""
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from repositories.interfaces import ReportRepository
from src.report import Report
from src.enums import ReportType, ReportStatus


class InMemoryReportRepository(ReportRepository):
    """In-memory HashMap implementation of ReportRepository."""

    def __init__(self):
        self._storage: Dict[str, Report] = {}

    # ── Generic CRUD ──────────────────────────────────────────────

    def save(self, entity: Report) -> None:
        self._storage[entity.report_id] = entity

    def find_by_id(self, entity_id: str) -> Optional[Report]:
        return self._storage.get(entity_id)

    def find_all(self) -> List[Report]:
        return list(self._storage.values())

    def delete(self, entity_id: str) -> bool:
        if entity_id in self._storage:
            del self._storage[entity_id]
            return True
        return False

    def exists(self, entity_id: str) -> bool:
        return entity_id in self._storage

    def count(self) -> int:
        return len(self._storage)

    # ── Domain-Specific Queries ───────────────────────────────────

    def find_by_user_id(self, user_id: str) -> List[Report]:
        return [r for r in self._storage.values() if r.user_id == user_id]

    def find_by_type_and_status(
        self, report_type: ReportType, status: ReportStatus
    ) -> List[Report]:
        return [
            r for r in self._storage.values()
            if r.report_type == report_type and r.status == status
        ]

    def find_open_by_type(self, report_type: ReportType) -> List[Report]:
        return self.find_by_type_and_status(report_type, ReportStatus.OPEN)

    def find_by_status(self, status: ReportStatus) -> List[Report]:
        return [r for r in self._storage.values() if r.status == status]

    def find_archived_older_than_days(self, days: int) -> List[Report]:
        """Used by the POPIA nightly deletion job (FR-11)."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        return [
            r for r in self._storage.values()
            if r.status == ReportStatus.ARCHIVED and r.created_at < cutoff
        ]