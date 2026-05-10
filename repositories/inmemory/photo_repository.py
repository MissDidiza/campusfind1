from typing import Optional, List, Dict
from repositories.interfaces import PhotoRepository
from src.photo import Photo


class InMemoryPhotoRepository(PhotoRepository):

    def __init__(self):
        self._storage: Dict[str, Photo] = {}

    def save(self, entity: Photo) -> None:
        self._storage[entity.photo_id] = entity

    def find_by_id(self, entity_id: str) -> Optional[Photo]:
        return self._storage.get(entity_id)

    def find_all(self) -> List[Photo]:
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

    def find_by_report_id(self, report_id: str) -> List[Photo]:
        return [p for p in self._storage.values() if p.report_id == report_id]

    def find_active_by_report_id(self, report_id: str) -> List[Photo]:
        return [p for p in self._storage.values() if p.report_id == report_id and not p.is_deleted]

    def delete_by_report_id(self, report_id: str) -> int:
        to_delete = [pid for pid, p in self._storage.items() if p.report_id == report_id]
        for pid in to_delete:
            del self._storage[pid]
        return len(to_delete)
