"""
notification_repository.py — In-Memory Notification Repository
Traces to FR-06 and US-006.
"""
from typing import Optional, List, Dict
from repositories.interfaces import NotificationRepository
from src.notification import Notification
from src.enums import NotificationStatus


class InMemoryNotificationRepository(NotificationRepository):

    def __init__(self):
        self._storage: Dict[str, Notification] = {}

    def save(self, entity: Notification) -> None:
        self._storage[entity.notification_id] = entity

    def find_by_id(self, entity_id: str) -> Optional[Notification]:
        return self._storage.get(entity_id)

    def find_all(self) -> List[Notification]:
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

    def find_by_user_id(self, user_id: str) -> List[Notification]:
        return [n for n in self._storage.values() if n.user_id == user_id]

    def find_unread_by_user_id(self, user_id: str) -> List[Notification]:
        return [
            n for n in self._storage.values()
            if n.user_id == user_id and not n.is_read
        ]

    def find_failed(self) -> List[Notification]:
        return [
            n for n in self._storage.values()
            if n.status == NotificationStatus.FAILED
        ]

    def mark_all_read_for_user(self, user_id: str) -> int:
        notifications = self.find_unread_by_user_id(user_id)
        for n in notifications:
            n.mark_read()
        return len(notifications)