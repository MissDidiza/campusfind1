"""
interfaces.py — Entity-Specific Repository Interfaces
======================================================
Each interface extends the generic Repository with domain-specific
query methods that make sense only for that entity.

For example:
- UserRepository adds find_by_email() because email is a unique lookup key.
- ReportRepository adds find_by_user_id() and find_by_type_and_status().
- MatchRecordRepository adds find_pending_for_admin().

These extra methods capture the domain's query requirements without
polluting the generic interface.

Traces to: Assignment 11 Task 1 and FR-01 through FR-12 (Assignment 4).
"""
from abc import abstractmethod
from typing import List, Optional
from repositories.base import Repository
from src.enums import ReportType, ReportStatus, MatchStatus, HandoverStatus


# ── User Repository Interface ─────────────────────────────────────

class UserRepository(Repository):
    """Repository interface for User entities."""

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[object]:
        """Find a user by their unique email address. Used during login and registration."""
        pass

    @abstractmethod
    def find_by_role(self, role: object) -> List[object]:
        """Return all users with a specific role (e.g., all admins)."""
        pass

    @abstractmethod
    def find_unverified(self) -> List[object]:
        """Return all users whose email has not yet been verified."""
        pass


# ── Report Repository Interface ───────────────────────────────────

class ReportRepository(Repository):
    """Repository interface for Report entities."""

    @abstractmethod
    def find_by_user_id(self, user_id: str) -> List[object]:
        """Return all reports submitted by a specific user."""
        pass

    @abstractmethod
    def find_by_type_and_status(
        self, report_type: ReportType, status: ReportStatus
    ) -> List[object]:
        """
        Return all reports of a given type and status.
        Used by the AI matching engine to fetch open lost/found reports.
        """
        pass

    @abstractmethod
    def find_open_by_type(self, report_type: ReportType) -> List[object]:
        """Shortcut: return all OPEN reports of a given type."""
        pass

    @abstractmethod
    def find_by_status(self, status: ReportStatus) -> List[object]:
        """Return all reports with a specific status."""
        pass

    @abstractmethod
    def find_archived_older_than_days(self, days: int) -> List[object]:
        """Return archived reports older than N days — used by POPIA deletion job."""
        pass


# ── Photo Repository Interface ────────────────────────────────────

class PhotoRepository(Repository):
    """Repository interface for Photo entities."""

    @abstractmethod
    def find_by_report_id(self, report_id: str) -> List[object]:
        """Return all photos associated with a specific report."""
        pass

    @abstractmethod
    def find_active_by_report_id(self, report_id: str) -> List[object]:
        """Return only non-deleted photos for a report."""
        pass

    @abstractmethod
    def delete_by_report_id(self, report_id: str) -> int:
        """Delete all photos for a report. Returns number of photos deleted."""
        pass


# ── MatchRecord Repository Interface ─────────────────────────────

class MatchRecordRepository(Repository):
    """Repository interface for MatchRecord entities."""

    @abstractmethod
    def find_by_lost_report_id(self, lost_report_id: str) -> List[object]:
        """Return all match records for a given lost report."""
        pass

    @abstractmethod
    def find_by_found_report_id(self, found_report_id: str) -> List[object]:
        """Return all match records for a given found report."""
        pass

    @abstractmethod
    def find_by_status(self, status: MatchStatus) -> List[object]:
        """Return all match records with a given status (e.g., PENDING_REVIEW)."""
        pass

    @abstractmethod
    def find_pending_for_admin(self) -> List[object]:
        """Return all NOTIFIED or PENDING_REVIEW matches for the admin queue."""
        pass

    @abstractmethod
    def find_above_threshold(self, threshold: float) -> List[object]:
        """Return all match records with confidence score above the given threshold."""
        pass


# ── Handover Repository Interface ─────────────────────────────────

class HandoverRepository(Repository):
    """Repository interface for Handover entities."""

    @abstractmethod
    def find_by_student_id(self, student_id: str) -> List[object]:
        """Return all handovers for a specific student."""
        pass

    @abstractmethod
    def find_by_admin_id(self, admin_id: str) -> List[object]:
        """Return all handovers managed by a specific admin."""
        pass

    @abstractmethod
    def find_by_status(self, status: HandoverStatus) -> List[object]:
        """Return all handovers in a given status."""
        pass

    @abstractmethod
    def find_awaiting_collection_older_than_days(self, days: int) -> List[object]:
        """Return handovers awaiting collection for more than N days — for escalation."""
        pass


# ── Notification Repository Interface ─────────────────────────────

class NotificationRepository(Repository):
    """Repository interface for Notification entities."""

    @abstractmethod
    def find_by_user_id(self, user_id: str) -> List[object]:
        """Return all notifications for a specific user."""
        pass

    @abstractmethod
    def find_unread_by_user_id(self, user_id: str) -> List[object]:
        """Return all unread notifications for a user."""
        pass

    @abstractmethod
    def find_failed(self) -> List[object]:
        """Return all notifications that failed delivery — for retry job."""
        pass

    @abstractmethod
    def mark_all_read_for_user(self, user_id: str) -> int:
        """Mark all notifications as read for a user. Returns count updated."""
        pass