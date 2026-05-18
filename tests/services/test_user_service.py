"""
test_user_service.py — Unit Tests for UserService
"""
import pytest
from repositories.inmemory.user_repository import InMemoryUserRepository
from services.user_service import UserService
from services.exceptions import (
    EmailAlreadyRegisteredException,
    InvalidEmailDomainException,
    InvalidCredentialsException,
    AccountNotVerifiedException,
    UserNotFoundException,
    UnauthorisedActionException,
)
from src.enums import UserRole


@pytest.fixture
def svc():
    return UserService(InMemoryUserRepository())


@pytest.fixture
def registered_user(svc):
    user = svc.register("Iminathi Didiza", "iminathi@university.ac.za", "Password123!")
    svc.verify_email(user.user_id)
    return user


class TestUserServiceRegister:

    def test_register_valid_user(self, svc):
        user = svc.register("Test User", "test@university.ac.za", "Password123!")
        assert user.email == "test@university.ac.za"
        assert user.full_name == "Test User"
        assert user.is_verified is False  # not yet verified

    def test_register_invalid_domain_raises(self, svc):
        with pytest.raises(InvalidEmailDomainException):
            svc.register("Test", "test@gmail.com", "Password123!")

    def test_register_duplicate_email_raises(self, svc):
        svc.register("User A", "dup@university.ac.za", "Password123!")
        with pytest.raises(EmailAlreadyRegisteredException):
            svc.register("User B", "dup@university.ac.za", "Password123!")

    def test_register_short_password_raises(self, svc):
        with pytest.raises(ValueError, match="8 characters"):
            svc.register("User", "u@university.ac.za", "short")

    def test_register_empty_name_raises(self, svc):
        with pytest.raises(ValueError):
            svc.register("", "u@university.ac.za", "Password123!")


class TestUserServiceLogin:

    def test_login_valid_credentials(self, svc, registered_user):
        user = svc.login("iminathi@university.ac.za", "Password123!")
        assert user.user_id == registered_user.user_id

    def test_login_wrong_password_raises(self, svc, registered_user):
        with pytest.raises(InvalidCredentialsException):
            svc.login("iminathi@university.ac.za", "WrongPassword!")

    def test_login_unknown_email_raises(self, svc):
        with pytest.raises(InvalidCredentialsException):
            svc.login("nobody@university.ac.za", "Password123!")

    def test_login_unverified_account_raises(self, svc):
        svc.register("Unverified", "unv@university.ac.za", "Password123!")
        with pytest.raises(AccountNotVerifiedException):
            svc.login("unv@university.ac.za", "Password123!")


class TestUserServiceProfile:

    def test_get_by_id_found(self, svc, registered_user):
        user = svc.get_by_id(registered_user.user_id)
        assert user.user_id == registered_user.user_id

    def test_get_by_id_not_found_raises(self, svc):
        with pytest.raises(UserNotFoundException):
            svc.get_by_id("nonexistent-id")

    def test_update_profile(self, svc, registered_user):
        updated = svc.update_profile(registered_user.user_id, "New Name")
        assert updated.full_name == "New Name"

    def test_deactivate_user(self, svc, registered_user):
        svc.deactivate(registered_user.user_id)
        user = svc.get_by_id(registered_user.user_id)
        assert user.is_verified is False

    def test_update_role_by_super_admin(self, svc):
        from src.user import User
        pw = User.hash_password("pass")
        sa = User("SA", "sa@university.ac.za", pw, UserRole.SUPER_ADMIN)
        sa.verify_email()
        svc._repo.save(sa)
        target = svc.register("Student", "s@university.ac.za", "Password123!")
        svc.verify_email(target.user_id)
        updated = svc.update_role(sa.user_id, target.user_id, UserRole.ADMIN)
        assert updated.role == UserRole.ADMIN

    def test_update_role_by_student_raises(self, svc, registered_user):
        target = svc.register("Other", "other@university.ac.za", "Password123!")
        with pytest.raises(UnauthorisedActionException):
            svc.update_role(registered_user.user_id, target.user_id, UserRole.ADMIN)
