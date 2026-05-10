"""
photo.py — Photo domain entity.
Maps to Photo class in CLASS_DIAGRAM.md.
Composition relationship: Photo cannot exist without a Report.
Traces to FR-03, FR-04, FR-11 and US-003, US-004, US-011.
"""
import uuid
from datetime import datetime
from typing import Optional

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE_KB = 5120  # 5 MB


class Photo:
    """Represents an image uploaded with a Report. Stored externally in Cloudinary."""

    def __init__(
        self,
        report_id: str,
        cloudinary_url: str,
        cloudinary_public_id: str,
        file_size_kb: int,
        mime_type: str,
    ):
        self._photo_id: str = str(uuid.uuid4())
        self._report_id: str = report_id
        self._cloudinary_url: str = cloudinary_url
        self._cloudinary_public_id: str = cloudinary_public_id
        self._file_size_kb: int = file_size_kb
        self._mime_type: str = mime_type
        self._uploaded_at: datetime = datetime.utcnow()
        self._is_deleted: bool = False

    # ── Properties ────────────────────────────────────────────────

    @property
    def photo_id(self) -> str:
        return self._photo_id

    @property
    def report_id(self) -> str:
        return self._report_id

    @property
    def cloudinary_url(self) -> str:
        return self._cloudinary_url

    @property
    def file_size_kb(self) -> int:
        return self._file_size_kb

    @property
    def is_deleted(self) -> bool:
        return self._is_deleted

    # ── Methods ───────────────────────────────────────────────────

    @staticmethod
    def validate(file_size_kb: int, mime_type: str) -> bool:
        """BR-03: Max 5 MB, image types only."""
        if file_size_kb > MAX_FILE_SIZE_KB:
            raise ValueError(f"Photo exceeds 5 MB limit ({file_size_kb} KB).")
        if mime_type not in ALLOWED_MIME_TYPES:
            raise ValueError(f"Invalid file type '{mime_type}'. Allowed: jpeg, png, webp.")
        return True

    def delete(self) -> None:
        """Mark photo as deleted (Cloudinary deletion handled by PhotoService)."""
        self._is_deleted = True

    def fetch_for_analysis(self) -> str:
        """Return the Cloudinary URL for AI image similarity analysis."""
        if self._is_deleted:
            raise RuntimeError("Cannot fetch a deleted photo.")
        return self._cloudinary_url

    def __repr__(self) -> str:
        return f"Photo(id={self._photo_id[:8]}, report={self._report_id[:8]}, deleted={self._is_deleted})"