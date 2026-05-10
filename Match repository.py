"""
match_repository.py — In-Memory MatchRecord Repository
Traces to FR-05, FR-07 and US-005, US-007.
"""
from typing import Optional, List, Dict
from repositories.interfaces import MatchRecordRepository
from src.match_record import MatchRecord
from src.enums import MatchStatus


class InMemoryMatchRecordRepository(MatchRecordRepository):

    def __init__(self):
        self._storage: Dict[str, MatchRecord] = {}

    def save(self, entity: MatchRecord) -> None:
        self._storage[entity.match_id] = entity

    def find_by_id(self, entity_id: str) -> Optional[MatchRecord]:
        return self._storage.get(entity_id)

    def find_all(self) -> List[MatchRecord]:
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

    def find_by_lost_report_id(self, lost_report_id: str) -> List[MatchRecord]:
        return [m for m in self._storage.values() if m.lost_report_id == lost_report_id]

    def find_by_found_report_id(self, found_report_id: str) -> List[MatchRecord]:
        return [m for m in self._storage.values() if m.found_report_id == found_report_id]

    def find_by_status(self, status: MatchStatus) -> List[MatchRecord]:
        return [m for m in self._storage.values() if m.status == status]

    def find_pending_for_admin(self) -> List[MatchRecord]:
        """Return NOTIFIED and PENDING_REVIEW matches sorted by confidence (highest first)."""
        pending_statuses = {MatchStatus.NOTIFIED, MatchStatus.PENDING_REVIEW}
        results = [m for m in self._storage.values() if m.status in pending_statuses]
        return sorted(results, key=lambda m: m.confidence_score, reverse=True)

    def find_above_threshold(self, threshold: float) -> List[MatchRecord]:
        return [m for m in self._storage.values() if m.confidence_score >= threshold]