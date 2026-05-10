"""
user.py — User domain entity.
Maps to the User class in CLASS_DIAGRAM.md (Assignment 9).
Traces to FR-01, FR-02, FR-12 and US-001, US-002, US-012.
"""
import uuid
import hashlib
from datetime import datetime
from typing import Optional
from src.enums import UserRole


class User:
    """Represents a registered person in the CampusFind system."""

    VALID_EMAIL_DOMAIN = "@university.ac.za"

    def __init__(
        self,
        full_name: str,
        email: str,
        password_hash: str,
        role: UserRole = UserRole.STUDENT,
    ):
        self._user_id: str = str(uuid.uuid4())
        self._full_name: str = full_name
        self._email: str = email
        self._password_hash: str = password_hash
        self._role: UserRole = role
        self._is_verified: bool = False
        self._email_notifications_enabled: bool = True
        self._consent_timestamp: Optional[datetime] = None
        self._created_at: datetime = datetime.utcnow()
        self._updated_at: datetime = datetime.utcnow()

    # ── Properties ────────────────────────────────────────────────

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def email(self) -> str:
        return self._email

    @property
    def role(self) -> UserRole:
        return self._role

    @role.setter
    def role(self, value: UserRole):
        self._role = value
        self._updated_at = datetime.utcnow()

    @property
    def is_verified(self) -> bool:
        return self._is_verified

    @property
    def email_notifications_enabled(self) -> bool:
        return self._email_notifications_enabled

    @email_notifications_enabled.setter
    def email_notifications_enabled(self, value: bool):
        self._email_notifications_enabled = value

    @property
    def created_at(self) -> datetime:
        return self._created_at

    # ── Methods ───────────────────────────────────────────────────

    @staticmethod
    def validate_email_domain(email: str) -> bool:
        """BR-01: Email must match university domain."""
        return email.endswith(User.VALID_EMAIL_DOMAIN)

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """Simulate bcrypt hashing (using sha256 for test portability)."""
        return hashlib.sha256(plain_password.encode()).hexdigest()

    @staticmethod
    def check_password(plain_password: str, password_hash: str) -> bool:
        return hashlib.sha256(plain_password.encode()).hexdigest() == password_hash

    def verify_email(self) -> bool:
        """Activate account after email verification."""
        self._is_verified = True
        self._consent_timestamp = datetime.utcnow()
        self._updated_at = datetime.utcnow()
        return True

    def is_admin(self) -> bool:
        return self._role in (UserRole.ADMIN, UserRole.SUPER_ADMIN)

    def is_super_admin(self) -> bool:
        return self._role == UserRole.SUPER_ADMIN

    def update_profile(self, full_name: Optional[str] = None) -> "User":
        if full_name:
            self._full_name = full_name
        self._updated_at = datetime.utcnow()
        return self

    def deactivate(self) -> None:
        """Schedule account for POPIA deletion pipeline."""
        self._is_verified = False
        self._updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"User(id={self._user_id[:8]}, email={self._email}, role={self._role.value})"