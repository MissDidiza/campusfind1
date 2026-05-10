"""
user_repository.py — In-Memory User Repository
================================================
HashMap-based implementation of UserRepository.
Stores User objects in a Python dict keyed by user_id.

Used in tests and development — no external dependencies required.
Traces to FR-01, FR-02, FR-12 and US-001, US-002, US-012.
"""
from typing import Optional, List, Dict
from repositories.interfaces import UserRepository
from src.user import User
from src.enums import UserRole


class InMemoryUserRepository(UserRepository):
    """In-memory HashMap implementation of UserRepository."""

    def __init__(self):
        self._storage: Dict[str, User] = {}

    # ── Generic CRUD ──────────────────────────────────────────────

    def save(self, entity: User) -> None:
        """Insert or update a User in the store."""
        self._storage[entity.user_id] = entity

    def find_by_id(self, entity_id: str) -> Optional[User]:
        return self._storage.get(entity_id)

    def find_all(self) -> List[User]:
        return list(self._storage.values())

    def delete(self, entity_id: str) -> bool:
        if entity_id in self._storage:
            del self._storage[entity_id]
            return True
        return False

    def exists(self, entity_id: str) -> bool:
        return entity_id in self._storage

    def count(self) -> int:
        return len(self._storage)

    # ── Domain-Specific Queries ───────────────────────────────────

    def find_by_email(self, email: str) -> Optional[User]:
        """Linear scan — acceptable for in-memory; a real DB would use an index."""
        for user in self._storage.values():
            if user.email.lower() == email.lower():
                return user
        return None

    def find_by_role(self, role: UserRole) -> List[User]:
        return [u for u in self._storage.values() if u.role == role]

    def find_unverified(self) -> List[User]:
        return [u for u in self._storage.values() if not u.is_verified]