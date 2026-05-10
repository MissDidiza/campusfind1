"""
base.py — Generic Repository Interface
=======================================
Defines the generic Repository interface that all entity-specific
repositories must implement. Using Python's ABC (Abstract Base Class)
and Generics ensures type safety and prevents duplication across entities.

Design Decision:
- Generic T (entity type) and ID (identifier type) avoid copy-paste
  of the same CRUD signatures across every entity repository.
- All concrete implementations (InMemory, FileSystem, Database) must
  implement every method — the interface acts as a contract.

Traces to: Assignment 11 Task 1 — Repository Interface Design.
"""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List

T = TypeVar("T")   # Entity type  e.g. User, Report
ID = TypeVar("ID") # Identifier type  e.g. str (UUID)


class Repository(ABC, Generic[T, ID]):
    """
    Generic repository interface — defines standard CRUD operations.
    All entity-specific repositories extend this interface.
    """

    @abstractmethod
    def save(self, entity: T) -> None:
        """Create or update an entity in the store."""
        pass

    @abstractmethod
    def find_by_id(self, entity_id: ID) -> Optional[T]:
        """Return the entity with the given ID, or None if not found."""
        pass

    @abstractmethod
    def find_all(self) -> List[T]:
        """Return all entities in the store."""
        pass

    @abstractmethod
    def delete(self, entity_id: ID) -> bool:
        """
        Delete the entity with the given ID.
        Returns True if deleted, False if not found.
        """
        pass

    @abstractmethod
    def exists(self, entity_id: ID) -> bool:
        """Return True if an entity with the given ID exists."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Return the total number of entities in the store."""
        pass