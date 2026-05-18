"""
match_service.py — Match Service
===================================
Handles business logic for AI match record management.
In production the AI analysis would call the Python FastAPI
AI Matching microservice. Here we simulate the scoring so
the service layer can be tested without the AI service running.

Business rules enforced:
- BR-04: Only matches >= 70% confidence are persisted
- BR-05: confidence = text*0.6 + image*0.4
- Admin must provide a reason when dismissing a match

Traces to FR-05, FR-07 | US-005, US-007
"""
from typing import List
from src.match_record import MatchRecord
from src.enums import MatchStatus, ReportStatus
from repositories.interfaces import MatchRecordRepository, ReportRepository
from services.exceptions import (
    MatchNotFoundException,
    MatchAlreadyResolvedException,
    ReportNotFoundException,
    UnauthorisedActionException,
)

CONFIDENCE_THRESHOLD = 0.70


class MatchService:
    """Encapsulates all business logic for MatchRecord management."""

    def __init__(
        self,
        match_repository: MatchRecordRepository,
        report_repository: ReportRepository,
    ):
        self._match_repo = match_repository
        self._report_repo = report_repository

    # ── Create Match ──────────────────────────────────────────────

    def create_match(
        self,
        lost_report_id: str,
        found_report_id: str,
        text_similarity: float,
        image_similarity: float,
    ) -> MatchRecord:
        """
        Persist a new match record if confidence >= threshold (BR-04).
        In production this is called by the AI Matching microservice.
        """
        if self._report_repo.find_by_id(lost_report_id) is None:
            raise ReportNotFoundException(lost_report_id)
        if self._report_repo.find_by_id(found_report_id) is None:
            raise ReportNotFoundException(found_report_id)

        match = MatchRecord(
            lost_report_id=lost_report_id,
            found_report_id=found_report_id,
            text_similarity_score=text_similarity,
            image_similarity_score=image_similarity,
        )

        if not match.meets_threshold():
            raise ValueError(
                f"Confidence score {match.confidence_score:.0%} is below "
                f"the {CONFIDENCE_THRESHOLD:.0%} threshold. Match not persisted."
            )

        match.notify()
        self._match_repo.save(match)
        return match

    # ── Read ──────────────────────────────────────────────────────

    def get_by_id(self, match_id: str) -> MatchRecord:
        return self._get_or_raise(match_id)

    def get_all(self) -> List[MatchRecord]:
        return self._match_repo.find_all()

    def get_pending_for_admin(self) -> List[MatchRecord]:
        """Return all matches awaiting admin review, sorted by confidence."""
        return self._match_repo.find_pending_for_admin()

    def get_by_lost_report(self, lost_report_id: str) -> List[MatchRecord]:
        return self._match_repo.find_by_lost_report_id(lost_report_id)

    # ── Admin Actions ─────────────────────────────────────────────

    def confirm_match(self, match_id: str, admin_id: str) -> MatchRecord:
        """
        Admin confirms a match. Updates both associated reports to MATCHED.
        Raises if match is already resolved.
        """
        match = self._get_or_raise(match_id)
        if match.status in (MatchStatus.CONFIRMED, MatchStatus.DISMISSED):
            raise MatchAlreadyResolvedException(match_id)

        match.confirm(admin_id)
        self._match_repo.save(match)

        # Update both report statuses to MATCHED (BR-06 locks them)
        lost = self._report_repo.find_by_id(match.lost_report_id)
        found = self._report_repo.find_by_id(match.found_report_id)
        if lost:
            lost.update_status(ReportStatus.MATCHED)
            self._report_repo.save(lost)
        if found:
            found.update_status(ReportStatus.MATCHED)
            self._report_repo.save(found)

        return match

    def dismiss_match(
        self, match_id: str, admin_id: str, reason: str
    ) -> MatchRecord:
        """
        Admin dismisses a false match. Reason is required.
        Both reports revert to OPEN status.
        """
        if not reason or not reason.strip():
            raise ValueError("A dismissal reason is required.")

        match = self._get_or_raise(match_id)
        if match.status in (MatchStatus.CONFIRMED, MatchStatus.DISMISSED):
            raise MatchAlreadyResolvedException(match_id)

        match.dismiss(admin_id, reason)
        self._match_repo.save(match)

        # Revert both reports to OPEN
        lost = self._report_repo.find_by_id(match.lost_report_id)
        found = self._report_repo.find_by_id(match.found_report_id)
        if lost:
            lost.update_status(ReportStatus.OPEN)
            self._report_repo.save(lost)
        if found:
            found.update_status(ReportStatus.OPEN)
            self._report_repo.save(found)

        return match

    # ── Internal ──────────────────────────────────────────────────

    def _get_or_raise(self, match_id: str) -> MatchRecord:
        match = self._match_repo.find_by_id(match_id)
        if match is None:
            raise MatchNotFoundException(match_id)
        return match
