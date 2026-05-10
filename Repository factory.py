"""
repository_factory.py — Repository Factory
===========================================
USE CASE:
CampusFind needs to support multiple storage backends:
  - MEMORY  : InMemory HashMap (development and testing)
  - FILE    : JSON file storage (stub — future implementation)
  - DATABASE: PostgreSQL (stub — future implementation)

The RepositoryFactory centralises the selection of the correct
implementation, so that all service classes receive the right
repository without knowing which backend is active.

Design Decision — Factory over Dependency Injection (DI):
A Factory was chosen over a full DI container (e.g., Python's
injector library) because:
1. The project is managed by a single developer — a lightweight factory
   is simpler to understand, debug, and extend.
2. Storage backend is selected at application startup via an environment
   variable (STORAGE_BACKEND), not at runtime per-request.
3. A Factory still achieves the key goal: service classes depend on
   interfaces, not concrete implementations.

If the project grows to a team size requiring a full IoC container,
migrating from Factory to DI is straightforward — only this file changes.

Traces to: Assignment 11 Task 3 — Storage Abstraction Mechanism.
"""
from repositories.interfaces import (
    UserRepository, ReportRepository, PhotoRepository,
    MatchRecordRepository, HandoverRepository, NotificationRepository,
)
from repositories.inmemory.user_repository import InMemoryUserRepository
from repositories.inmemory.report_repository import InMemoryReportRepository
from repositories.inmemory.photo_repository import InMemoryPhotoRepository
from repositories.inmemory.match_repository import InMemoryMatchRecordRepository
from repositories.inmemory.handover_repository import InMemoryHandoverRepository
from repositories.inmemory.notification_repository import InMemoryNotificationRepository

# Stub imports — implementations are in repositories/stubs/
from repositories.stubs.file_repository import (
    FileSystemUserRepository,
    FileSystemReportRepository,
)
from repositories.stubs.database_repository import (
    DatabaseUserRepository,
    DatabaseReportRepository,
)

SUPPORTED_BACKENDS = {"MEMORY", "FILE", "DATABASE"}


class RepositoryFactory:
    """
    Factory — returns the correct repository implementation for the
    configured storage backend. All service classes call this factory
    at startup to get their repository instances.

    Usage:
        factory = RepositoryFactory(storage_type="MEMORY")
        user_repo = factory.get_user_repository()
        report_repo = factory.get_report_repository()
    """

    def __init__(self, storage_type: str = "MEMORY"):
        storage_type = storage_type.upper()
        if storage_type not in SUPPORTED_BACKENDS:
            raise ValueError(
                f"Unsupported storage type '{storage_type}'. "
                f"Supported: {SUPPORTED_BACKENDS}"
            )
        self._storage_type = storage_type

    def get_user_repository(self) -> UserRepository:
        if self._storage_type == "MEMORY":
            return InMemoryUserRepository()
        elif self._storage_type == "FILE":
            return FileSystemUserRepository(file_path="data/users.json")
        elif self._storage_type == "DATABASE":
            return DatabaseUserRepository(dsn="postgresql://localhost/campusfind")

    def get_report_repository(self) -> ReportRepository:
        if self._storage_type == "MEMORY":
            return InMemoryReportRepository()
        elif self._storage_type == "FILE":
            return FileSystemReportRepository(file_path="data/reports.json")
        elif self._storage_type == "DATABASE":
            return DatabaseReportRepository(dsn="postgresql://localhost/campusfind")

    def get_photo_repository(self) -> PhotoRepository:
        if self._storage_type == "MEMORY":
            return InMemoryPhotoRepository()
        raise NotImplementedError(
            f"PhotoRepository not yet implemented for backend '{self._storage_type}'"
        )

    def get_match_repository(self) -> MatchRecordRepository:
        if self._storage_type == "MEMORY":
            return InMemoryMatchRecordRepository()
        raise NotImplementedError(
            f"MatchRecordRepository not yet implemented for backend '{self._storage_type}'"
        )

    def get_handover_repository(self) -> HandoverRepository:
        if self._storage_type == "MEMORY":
            return InMemoryHandoverRepository()
        raise NotImplementedError(
            f"HandoverRepository not yet implemented for backend '{self._storage_type}'"
        )

    def get_notification_repository(self) -> NotificationRepository:
        if self._storage_type == "MEMORY":
            return InMemoryNotificationRepository()
        raise NotImplementedError(
            f"NotificationRepository not yet implemented for backend '{self._storage_type}'"
        )

    def __repr__(self) -> str:
        return f"RepositoryFactory(backend={self._storage_type})"


# ── Dependency Injection Container ────────────────────────────────

class DIContainer:
    """
    Lightweight DI container — holds a single RepositoryFactory and
    provides pre-built repository instances to service classes.

    Service classes declare their repository dependencies in __init__
    and receive them via this container at application startup.

    This ensures services depend on interfaces (UserRepository),
    not concrete classes (InMemoryUserRepository).

    Usage:
        container = DIContainer(storage_type="MEMORY")
        user_service = UserService(container.user_repo, container.notification_repo)
    """

    def __init__(self, storage_type: str = "MEMORY"):
        factory = RepositoryFactory(storage_type)
        self.user_repo: UserRepository = factory.get_user_repository()
        self.report_repo: ReportRepository = factory.get_report_repository()
        self.photo_repo: PhotoRepository = factory.get_photo_repository()
        self.match_repo: MatchRecordRepository = factory.get_match_repository()
        self.handover_repo: HandoverRepository = factory.get_handover_repository()
        self.notification_repo: NotificationRepository = factory.get_notification_repository()

    def __repr__(self) -> str:
        return f"DIContainer(repos={list(vars(self).keys())})"