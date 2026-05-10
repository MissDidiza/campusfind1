from typing import Optional, List, Dict
from datetime import datetime, timedelta
from repositories.interfaces import HandoverRepository
from src.handover import Handover
from src.enums import HandoverStatus


class InMemoryHandoverRepository(HandoverRepository):

    def __init__(self):
        self._storage: Dict[str, Handover] = {}

    def save(self, entity: Handover) -> None:
        self._storage[entity.handover_id] = entity

    def find_by_id(self, entity_id: str) -> Optional[Handover]:
        return self._storage.get(entity_id)

    def find_all(self) -> List[Handover]:
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

    def find_by_student_id(self, student_id: str) -> List[Handover]:
        return [h for h in self._storage.values() if h.student_id == student_id]

    def find_by_admin_id(self, admin_id: str) -> List[Handover]:
        return [h for h in self._storage.values() if h.admin_id == admin_id]

    def find_by_status(self, status: HandoverStatus) -> List[Handover]:
        return [h for h in self._storage.values() if h.status == status]

    def find_awaiting_collection_older_than_days(self, days: int) -> List[Handover]:
        cutoff = datetime.utcnow() - timedelta(days=days)
        return [
            h for h in self._storage.values()
            if h.status == HandoverStatus.AWAITING_COLLECTION and h.created_at < cutoff
        ]
