"""
handover.py — Handover domain entity.
Maps to Handover class in CLASS_DIAGRAM.md.
Traces to FR-08 and US-008.
"""
import uuid
from datetime import datetime
from typing import Optional
from src.enums import HandoverStatus


class Handover:
    """Represents the physical return of a found item to its owner."""

    def __init__(
        self,
        match_id: str,
        lost_report_id: str,
        found_report_id: str,
        admin_id: str,
        student_id: str,
    ):
        self._handover_id: str = str(uuid.uuid4())
        self._match_id: str = match_id
        self._lost_report_id: str = lost_report_id
        self._found_report_id: str = found_report_id
        self._admin_id: str = admin_id
        self._student_id: str = student_id
        self._pickup_location: Optional[str] = None
        self._pickup_window_start: Optional[datetime] = None
        self._pickup_window_end: Optional[datetime] = None
        self._status: HandoverStatus = HandoverStatus.INITIATED
        self._confirmed_at: Optional[datetime] = None
        self._is_manual_override: bool = False
        self._override_reason: Optional[str] = None
        self._created_at: datetime = datetime.utcnow()
        self._days_since_initiated: int = 0

    # ── Properties ────────────────────────────────────────────────

    @property
    def handover_id(self) -> str:
        return self._handover_id

    @property
    def status(self) -> HandoverStatus:
        return self._status

    @property
    def admin_id(self) -> str:
        return self._admin_id

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def pickup_location(self) -> Optional[str]:
        return self._pickup_location

    @property
    def is_manual_override(self) -> bool:
        return self._is_manual_override

    # ── Methods ───────────────────────────────────────────────────

    def notify_student(self, location: str, window_start: datetime, window_end: datetime) -> None:
        self._pickup_location = location
        self._pickup_window_start = window_start
        self._pickup_window_end = window_end
        self._status = HandoverStatus.AWAITING_COLLECTION

    def send_reminder(self, reminder_number: int) -> None:
        if reminder_number == 1:
            self._status = HandoverStatus.REMINDER_1_SENT
        elif reminder_number == 2:
            self._status = HandoverStatus.REMINDER_2_SENT
        else:
            raise ValueError("reminder_number must be 1 or 2.")

    def record_collection(self) -> None:
        self._confirmed_at = datetime.utcnow()
        self._status = HandoverStatus.COLLECTED

    def record_manual_override(self, reason: str) -> None:
        if not reason or not reason.strip():
            raise ValueError("Override reason is required.")
        self._is_manual_override = True
        self._override_reason = reason
        self._confirmed_at = datetime.utcnow()
        self._status = HandoverStatus.COLLECTED

    def escalate(self) -> None:
        self._status = HandoverStatus.ESCALATED

    def mark_unclaimed(self) -> None:
        self._status = HandoverStatus.UNCLAIMED

    def close(self) -> None:
        self._status = HandoverStatus.CLOSED

    def get_days_since_initiated(self) -> int:
        return (datetime.utcnow() - self._created_at).days

    def __repr__(self) -> str:
        return (
            f"Handover(id={self._handover_id[:8]}, "
            f"status={self._status.value}, admin={self._admin_id[:8]})"
        )