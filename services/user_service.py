"""
user_service.py — User Service
================================
Handles all business logic for user registration, authentication,
and profile management. Uses UserRepository (Assignment 11) for persistence.

Business rules enforced:
- BR-01: Email must match university domain
- POPIA: consent timestamp logged at registration
- Passwords never stored in plain text

Traces to FR-01, FR-02, FR-12 | US-001, US-002, US-012
"""
from typing import Optional, List
from src.user import User
from src.enums import UserRole
from repositories.interfaces import UserRepository
from services.exceptions import (
    EmailAlreadyRegisteredException,
    InvalidEmailDomainException,
    InvalidCredentialsException,
    AccountNotVerifiedException,
    UserNotFoundException,
    UnauthorisedActionException,
)


class UserService:
    """Encapsulates all business logic for User management."""

    def __init__(self, user_repository: UserRepository):
        self._repo = user_repository

    # ── Registration ──────────────────────────────────────────────

    def register(self, full_name: str, email: str, password: str) -> User:
        """
        Register a new student account.
        BR-01: Validates university email domain.
        Raises EmailAlreadyRegisteredException if email is taken.
        """
        if not full_name or not full_name.strip():
            raise ValueError("Full name is required.")
        if not User.validate_email_domain(email):
            raise InvalidEmailDomainException(email)
        if self._repo.find_by_email(email) is not None:
            raise EmailAlreadyRegisteredException(email)
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters.")

        password_hash = User.hash_password(password)
        user = User(full_name.strip(), email.lower(), password_hash)
        self._repo.save(user)
        return user

    def verify_email(self, user_id: str) -> User:
        """Activate a user account after email verification."""
        user = self._get_or_raise(user_id)
        user.verify_email()
        self._repo.save(user)
        return user

    # ── Authentication ────────────────────────────────────────────

    def login(self, email: str, password: str) -> User:
        """
        Authenticate a user.
        Returns the User on success.
        Raises generic InvalidCredentialsException (never reveals which field is wrong).
        """
        user = self._repo.find_by_email(email.lower())
        if user is None:
            raise InvalidCredentialsException()
        if not User.check_password(password, user._password_hash):
            raise InvalidCredentialsException()
        if not user.is_verified:
            raise AccountNotVerifiedException()
        return user

    # ── Profile Management ────────────────────────────────────────

    def get_by_id(self, user_id: str) -> User:
        return self._get_or_raise(user_id)

    def get_all(self) -> List[User]:
        return self._repo.find_all()

    def update_profile(self, user_id: str, full_name: str) -> User:
        user = self._get_or_raise(user_id)
        user.update_profile(full_name)
        self._repo.save(user)
        return user

    def update_role(
        self, requester_id: str, target_user_id: str, new_role: UserRole
    ) -> User:
        """Only super admins can change roles (FR-12)."""
        requester = self._get_or_raise(requester_id)
        if not requester.is_super_admin():
            raise UnauthorisedActionException("Only super admins can change user roles.")
        target = self._get_or_raise(target_user_id)
        target.role = new_role
        self._repo.save(target)
        return target

    def deactivate(self, user_id: str) -> None:
        user = self._get_or_raise(user_id)
        user.deactivate()
        self._repo.save(user)

    def get_by_email(self, email: str) -> Optional[User]:
        return self._repo.find_by_email(email.lower())

    # ── Internal ──────────────────────────────────────────────────

    def _get_or_raise(self, user_id: str) -> User:
        user = self._repo.find_by_id(user_id)
        if user is None:
            raise UserNotFoundException(user_id)
        return user
