"""
dependencies.py — FastAPI Dependency Injection
================================================
Provides shared service instances to all route handlers
via FastAPI's dependency injection system.

The DIContainer (Assignment 11) is created once at startup
with the MEMORY backend. Swapping to DATABASE only requires
changing the storage_type string here.
"""
from factories.repository_factory import DIContainer
from services.user_service import UserService
from services.report_service import ReportService
from services.match_service import MatchService

# Single container instance — shared across all requests
_container = DIContainer(storage_type="MEMORY")

# Service singletons built from the container
_user_service = UserService(_container.user_repo)
_report_service = ReportService(_container.report_repo, _container.photo_repo)
_match_service = MatchService(_container.match_repo, _container.report_repo)


def get_user_service() -> UserService:
    return _user_service


def get_report_service() -> ReportService:
    return _report_service


def get_match_service() -> MatchService:
    return _match_service
