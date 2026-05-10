"""
database_repository.py — Database Repository Stubs
====================================================
FUTURE IMPLEMENTATION: PostgreSQL persistence using psycopg2 or SQLAlchemy.

These stubs show exactly what would need to be implemented to connect
CampusFind to a real PostgreSQL database. The SQL schema from the domain
model (Assignment 9) maps directly to the repository methods here.

To fully implement:
1. Install: pip install psycopg2-binary sqlalchemy
2. Replace NotImplementedError with SQL queries.
3. Add connection pooling (use the DatabaseConnectionPool Singleton
   from Assignment 10's singleton.py).
4. Add transaction management (commit/rollback).

Traces to: Assignment 11 Task 4 — Future-Proofing.
"""
from typing import Optional, List
from repositories.interfaces import UserRepository, ReportRepository
from src.user import User
from src.report import Report
from src.enums import ReportType, ReportStatus


class DatabaseUserRepository(UserRepository):
    """
    STUB — PostgreSQL implementation of UserRepository.

    SQL Schema (users table):
        CREATE TABLE users (
            user_id UUID PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL DEFAULT 'STUDENT',
            is_verified BOOLEAN NOT NULL DEFAULT FALSE,
            email_notifications_enabled BOOLEAN NOT NULL DEFAULT TRUE,
            consent_timestamp TIMESTAMPTZ,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        CREATE INDEX idx_users_email ON users(email);
        CREATE INDEX idx_users_role ON users(role);
    """

    def __init__(self, dsn: str):
        self._dsn = dsn
        # TODO: self._conn = psycopg2.connect(dsn)
        # TODO: or use SQLAlchemy: self._engine = create_engine(dsn)

    def save(self, entity: User) -> None:
        raise NotImplementedError(
            "DatabaseUserRepository.save() — TODO: "
            "INSERT INTO users ... ON CONFLICT (user_id) DO UPDATE SET ..."
        )

    def find_by_id(self, entity_id: str) -> Optional[User]:
        raise NotImplementedError(
            "DatabaseUserRepository.find_by_id() — TODO: "
            "SELECT * FROM users WHERE user_id = %s"
        )

    def find_all(self) -> List[User]:
        raise NotImplementedError(
            "DatabaseUserRepository.find_all() — TODO: "
            "SELECT * FROM users ORDER BY created_at DESC"
        )

    def delete(self, entity_id: str) -> bool:
        raise NotImplementedError(
            "DatabaseUserRepository.delete() — TODO: "
            "DELETE FROM users WHERE user_id = %s RETURNING user_id"
        )

    def exists(self, entity_id: str) -> bool:
        raise NotImplementedError(
            "TODO: SELECT EXISTS(SELECT 1 FROM users WHERE user_id = %s)"
        )

    def count(self) -> int:
        raise NotImplementedError("TODO: SELECT COUNT(*) FROM users")

    def find_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError(
            "DatabaseUserRepository.find_by_email() — TODO: "
            "SELECT * FROM users WHERE email = %s  [uses idx_users_email index]"
        )

    def find_by_role(self, role) -> List[User]:
        raise NotImplementedError(
            "TODO: SELECT * FROM users WHERE role = %s"
        )

    def find_unverified(self) -> List[User]:
        raise NotImplementedError(
            "TODO: SELECT * FROM users WHERE is_verified = FALSE"
        )


class DatabaseReportRepository(ReportRepository):
    """
    STUB — PostgreSQL implementation of ReportRepository.

    SQL Schema (reports table):
        CREATE TABLE reports (
            report_id UUID PRIMARY KEY,
            user_id UUID NOT NULL REFERENCES users(user_id),
            type VARCHAR(10) NOT NULL CHECK (type IN ('LOST','FOUND')),
            item_name VARCHAR(255) NOT NULL,
            category VARCHAR(20) NOT NULL,
            description TEXT NOT NULL,
            location VARCHAR(255) NOT NULL,
            date_lost_or_found DATE NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'OPEN',
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        CREATE INDEX idx_reports_user_id ON reports(user_id);
        CREATE INDEX idx_reports_type_status ON reports(type, status);
        CREATE INDEX idx_reports_status ON reports(status);
    """

    def __init__(self, dsn: str):
        self._dsn = dsn

    def save(self, entity: Report) -> None:
        raise NotImplementedError(
            "DatabaseReportRepository.save() — TODO: "
            "INSERT INTO reports ... ON CONFLICT (report_id) DO UPDATE SET ..."
        )

    def find_by_id(self, entity_id: str) -> Optional[Report]:
        raise NotImplementedError(
            "TODO: SELECT * FROM reports WHERE report_id = %s"
        )

    def find_all(self) -> List[Report]:
        raise NotImplementedError(
            "TODO: SELECT * FROM reports ORDER BY created_at DESC"
        )

    def delete(self, entity_id: str) -> bool:
        raise NotImplementedError(
            "TODO: DELETE FROM reports WHERE report_id = %s RETURNING report_id"
        )

    def exists(self, entity_id: str) -> bool:
        raise NotImplementedError("TODO")

    def count(self) -> int:
        raise NotImplementedError("TODO")

    def find_by_user_id(self, user_id: str) -> List[Report]:
        raise NotImplementedError(
            "TODO: SELECT * FROM reports WHERE user_id = %s  [uses idx_reports_user_id]"
        )

    def find_by_type_and_status(self, report_type, status) -> List[Report]:
        raise NotImplementedError(
            "TODO: SELECT * FROM reports WHERE type = %s AND status = %s "
            "[uses idx_reports_type_status]"
        )

    def find_open_by_type(self, report_type) -> List[Report]:
        raise NotImplementedError("TODO: find_by_type_and_status(type, 'OPEN')")

    def find_by_status(self, status) -> List[Report]:
        raise NotImplementedError(
            "TODO: SELECT * FROM reports WHERE status = %s  [uses idx_reports_status]"
        )

    def find_archived_older_than_days(self, days: int) -> List[Report]:
        raise NotImplementedError(
            f"TODO: SELECT * FROM reports WHERE status = 'ARCHIVED' "
            f"AND created_at < NOW() - INTERVAL '{days} days'"
        )