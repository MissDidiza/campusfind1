"""
file_repository.py — FileSystem Repository Stubs
=================================================
FUTURE IMPLEMENTATION: JSON file-based persistence.

These stubs demonstrate how the repository interfaces make it trivial
to add a new storage backend. The service layer and tests require
zero changes — only the concrete implementation changes.

To fully implement:
1. Replace NotImplementedError with JSON read/write logic.
2. Handle file locking for concurrent access.
3. Add serialisation/deserialisation for each entity type.

Traces to: Assignment 11 Task 4 — Future-Proofing.
"""
import json
import os
from typing import Optional, List
from repositories.interfaces import UserRepository, ReportRepository
from src.user import User
from src.report import Report
from src.enums import ReportType, ReportStatus


class FileSystemUserRepository(UserRepository):
    """
    STUB — FileSystem implementation of UserRepository.
    Serialises User objects to a JSON file for simple persistence
    across application restarts (useful for demo deployments).
    """

    def __init__(self, file_path: str = "data/users.json"):
        self._file_path = file_path
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def save(self, entity: User) -> None:
        raise NotImplementedError(
            "FileSystemUserRepository.save() — TODO: Serialise User to JSON file. "
            "Hint: use entity.__dict__ and json.dump(). "
            "Handle concurrent writes with file locking (fcntl on Unix)."
        )

    def find_by_id(self, entity_id: str) -> Optional[User]:
        raise NotImplementedError(
            "FileSystemUserRepository.find_by_id() — TODO: Load JSON, deserialise User."
        )

    def find_all(self) -> List[User]:
        raise NotImplementedError(
            "FileSystemUserRepository.find_all() — TODO: Load all users from JSON file."
        )

    def delete(self, entity_id: str) -> bool:
        raise NotImplementedError(
            "FileSystemUserRepository.delete() — TODO: Remove user entry from JSON file."
        )

    def exists(self, entity_id: str) -> bool:
        raise NotImplementedError("TODO")

    def count(self) -> int:
        raise NotImplementedError("TODO")

    def find_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError(
            "FileSystemUserRepository.find_by_email() — TODO: Linear scan of JSON file."
        )

    def find_by_role(self, role) -> List[User]:
        raise NotImplementedError("TODO")

    def find_unverified(self) -> List[User]:
        raise NotImplementedError("TODO")


class FileSystemReportRepository(ReportRepository):
    """
    STUB — FileSystem implementation of ReportRepository.
    Serialises Report objects (including photo URLs) to JSON.
    """

    def __init__(self, file_path: str = "data/reports.json"):
        self._file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def save(self, entity: Report) -> None:
        raise NotImplementedError(
            "FileSystemReportRepository.save() — TODO: Serialise Report to JSON. "
            "Note: photo_urls must be extracted separately (composition relationship)."
        )

    def find_by_id(self, entity_id: str) -> Optional[Report]:
        raise NotImplementedError("TODO")

    def find_all(self) -> List[Report]:
        raise NotImplementedError("TODO")

    def delete(self, entity_id: str) -> bool:
        raise NotImplementedError("TODO")

    def exists(self, entity_id: str) -> bool:
        raise NotImplementedError("TODO")

    def count(self) -> int:
        raise NotImplementedError("TODO")

    def find_by_user_id(self, user_id: str) -> List[Report]:
        raise NotImplementedError("TODO")

    def find_by_type_and_status(self, report_type, status) -> List[Report]:
        raise NotImplementedError("TODO")

    def find_open_by_type(self, report_type) -> List[Report]:
        raise NotImplementedError("TODO")

    def find_by_status(self, status) -> List[Report]:
        raise NotImplementedError("TODO")

    def find_archived_older_than_days(self, days: int) -> List[Report]:
        raise NotImplementedError("TODO")