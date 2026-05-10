"""
notification.py — Notification domain entity.
Maps to Notification class in CLASS_DIAGRAM.md.
Traces to FR-06 and US-006.
"""
import uuid
from datetime import datetime
from typing import Optional
from src.enums import NotificationType, NotificationChannel, NotificationStatus

MAX_RETRIES = 3


class Notification:
    """Represents a message sent to a User — email or in-app."""

    def __init__(
        self,
        user_id: str,
        notification_type: NotificationType,
        channel: NotificationChannel,
        subject: str,
        body: str,
        related_entity_id: Optional[str] = None,
    ):
        self._notification_id: str = str(uuid.uuid4())
        self._user_id: str = user_id
        self._type: NotificationType = notification_type
        self._channel: NotificationChannel = channel
        self._subject: str = subject
        self._body: str = body
        self._related_entity_id: Optional[str] = related_entity_id
        self._is_read: bool = False
        self._status: NotificationStatus = NotificationStatus.QUEUED
        self._retry_count: int = 0
        self._created_at: datetime = datetime.utcnow()
        self._read_at: Optional[datetime] = None

    # ── Properties ────────────────────────────────────────────────

    @property
    def notification_id(self) -> str:
        return self._notification_id

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def status(self) -> NotificationStatus:
        return self._status

    @property
    def is_read(self) -> bool:
        return self._is_read

    @property
    def retry_count(self) -> int:
        return self._retry_count

    @property
    def subject(self) -> str:
        return self._subject

    @property
    def channel(self) -> NotificationChannel:
        return self._channel

    # ── Methods ───────────────────────────────────────────────────

    def send(self) -> None:
        self._status = NotificationStatus.SENDING

    def mark_delivered(self) -> None:
        self._status = NotificationStatus.DELIVERED

    def mark_partially_delivered(self) -> None:
        self._status = NotificationStatus.PARTIALLY_DELIVERED

    def can_retry(self) -> bool:
        return self._retry_count < MAX_RETRIES

    def retry(self) -> None:
        if not self.can_retry():
            raise RuntimeError(f"Maximum retries ({MAX_RETRIES}) exceeded.")
        self._retry_count += 1
        self._status = NotificationStatus.SENDING

    def log_failure(self, error: str) -> None:
        self._status = NotificationStatus.FAILED

    def mark_read(self) -> None:
        self._is_read = True
        self._status = NotificationStatus.READ
        self._read_at = datetime.utcnow()

    def mark_expired(self) -> None:
        self._status = NotificationStatus.EXPIRED

    def __repr__(self) -> str:
        return (
            f"Notification(id={self._notification_id[:8]}, "
            f"type={self._type.value}, status={self._status.value})"
        )