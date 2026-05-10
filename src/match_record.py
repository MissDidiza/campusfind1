"""
match_record.py — MatchRecord domain entity.
Maps to MatchRecord class in CLASS_DIAGRAM.md.
Traces to FR-05, FR-07 and US-005, US-007.
"""
import uuid
from datetime import datetime
from typing import Optional
from src.enums import MatchStatus

CONFIDENCE_THRESHOLD = 0.70
TEXT_WEIGHT = 0.6
IMAGE_WEIGHT = 0.4


class MatchRecord:
    """AI-generated suggestion that a lost and found report refer to the same item."""

    def __init__(
        self,
        lost_report_id: str,
        found_report_id: str,
        text_similarity_score: float,
        image_similarity_score: float,
    ):
        self._match_id: str = str(uuid.uuid4())
        self._lost_report_id: str = lost_report_id
        self._found_report_id: str = found_report_id
        self._text_similarity_score: float = text_similarity_score
        self._image_similarity_score: float = image_similarity_score
        self._confidence_score: float = self._calculate_confidence()
        self._status: MatchStatus = MatchStatus.GENERATED
        self._admin_id: Optional[str] = None
        self._dismissal_reason: Optional[str] = None
        self._created_at: datetime = datetime.utcnow()
        self._updated_at: datetime = datetime.utcnow()

    # ── Properties ────────────────────────────────────────────────

    @property
    def match_id(self) -> str:
        return self._match_id

    @property
    def lost_report_id(self) -> str:
        return self._lost_report_id

    @property
    def found_report_id(self) -> str:
        return self._found_report_id

    @property
    def confidence_score(self) -> float:
        return self._confidence_score

    @property
    def status(self) -> MatchStatus:
        return self._status

    @property
    def text_similarity_score(self) -> float:
        return self._text_similarity_score

    @property
    def image_similarity_score(self) -> float:
        return self._image_similarity_score

    # ── Methods ───────────────────────────────────────────────────

    def _calculate_confidence(self) -> float:
        """BR-05: confidence = text_score * 0.6 + image_score * 0.4"""
        return round(
            (self._text_similarity_score * TEXT_WEIGHT)
            + (self._image_similarity_score * IMAGE_WEIGHT),
            4,
        )

    def meets_threshold(self) -> bool:
        """BR-04: Only matches >= 70% are surfaced."""
        return self._confidence_score >= CONFIDENCE_THRESHOLD

    def notify(self) -> None:
        self._status = MatchStatus.NOTIFIED
        self._updated_at = datetime.utcnow()

    def confirm(self, admin_id: str) -> None:
        if self._status not in (MatchStatus.NOTIFIED, MatchStatus.PENDING_REVIEW):
            raise RuntimeError("Can only confirm a notified or pending match.")
        self._admin_id = admin_id
        self._status = MatchStatus.CONFIRMED
        self._updated_at = datetime.utcnow()

    def dismiss(self, admin_id: str, reason: str) -> None:
        if not reason or not reason.strip():
            raise ValueError("A dismissal reason is required.")
        self._admin_id = admin_id
        self._dismissal_reason = reason
        self._status = MatchStatus.DISMISSED
        self._updated_at = datetime.utcnow()

    def mark_stale(self) -> None:
        self._status = MatchStatus.STALE
        self._updated_at = datetime.utcnow()

    def close(self) -> None:
        self._status = MatchStatus.CLOSED
        self._updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return (
            f"MatchRecord(id={self._match_id[:8]}, "
            f"confidence={self._confidence_score:.0%}, status={self._status.value})"
        )