"""
test_match_service.py — Unit Tests for MatchService
"""
import pytest
from datetime import date
from repositories.inmemory.report_repository import InMemoryReportRepository
from repositories.inmemory.match_repository import InMemoryMatchRecordRepository
from services.match_service import MatchService
from services.report_service import ReportService
from repositories.inmemory.photo_repository import InMemoryPhotoRepository
from services.exceptions import (
    MatchNotFoundException,
    MatchAlreadyResolvedException,
    ReportNotFoundException,
)
from src.enums import MatchStatus, ReportStatus


@pytest.fixture
def report_repo():
    return InMemoryReportRepository()


@pytest.fixture
def match_svc(report_repo):
    return MatchService(InMemoryMatchRecordRepository(), report_repo)


@pytest.fixture
def report_svc(report_repo):
    return ReportService(report_repo, InMemoryPhotoRepository())


@pytest.fixture
def lost(report_svc):
    return report_svc.create_report(
        "u1", "LOST", "Laptop", "ELECTRONICS",
        "Silver Dell laptop with UCT sticker and charger bag attached",
        "Library", date.today()
    )


@pytest.fixture
def found(report_svc):
    return report_svc.create_report(
        "u2", "FOUND", "Laptop", "ELECTRONICS",
        "Silver laptop found near library entrance with university sticker",
        "Library Entrance", date.today()
    )


class TestMatchServiceCreate:

    def test_create_match_above_threshold(self, match_svc, lost, found):
        match = match_svc.create_match(lost.report_id, found.report_id, 0.90, 0.85)
        assert match.confidence_score >= 0.70
        assert match.status == MatchStatus.NOTIFIED

    def test_create_match_below_threshold_raises(self, match_svc, lost, found):
        with pytest.raises(ValueError, match="threshold"):
            match_svc.create_match(lost.report_id, found.report_id, 0.40, 0.30)

    def test_create_match_unknown_lost_report_raises(self, match_svc, found):
        with pytest.raises(ReportNotFoundException):
            match_svc.create_match("nonexistent", found.report_id, 0.90, 0.85)

    def test_create_match_unknown_found_report_raises(self, match_svc, lost):
        with pytest.raises(ReportNotFoundException):
            match_svc.create_match(lost.report_id, "nonexistent", 0.90, 0.85)


class TestMatchServiceAdminActions:

    def test_confirm_match_updates_report_statuses(
        self, match_svc, lost, found, report_repo
    ):
        match = match_svc.create_match(lost.report_id, found.report_id, 0.90, 0.85)
        match_svc.confirm_match(match.match_id, "admin-1")
        assert report_repo.find_by_id(lost.report_id).status == ReportStatus.MATCHED
        assert report_repo.find_by_id(found.report_id).status == ReportStatus.MATCHED

    def test_confirm_already_confirmed_raises(self, match_svc, lost, found):
        match = match_svc.create_match(lost.report_id, found.report_id, 0.90, 0.85)
        match_svc.confirm_match(match.match_id, "admin-1")
        with pytest.raises(MatchAlreadyResolvedException):
            match_svc.confirm_match(match.match_id, "admin-1")

    def test_dismiss_match_with_reason(self, match_svc, lost, found, report_repo):
        match = match_svc.create_match(lost.report_id, found.report_id, 0.90, 0.85)
        match_svc.dismiss_match(match.match_id, "admin-1", "Different colours")
        assert match.status == MatchStatus.DISMISSED
        assert report_repo.find_by_id(lost.report_id).status == ReportStatus.OPEN

    def test_dismiss_without_reason_raises(self, match_svc, lost, found):
        match = match_svc.create_match(lost.report_id, found.report_id, 0.90, 0.85)
        with pytest.raises(ValueError, match="reason"):
            match_svc.dismiss_match(match.match_id, "admin-1", "")

    def test_get_pending_sorted_by_confidence(self, match_svc, lost, found):
        m1 = match_svc.create_match(lost.report_id, found.report_id, 0.75, 0.70)
        m2 = match_svc.create_match(lost.report_id, found.report_id, 0.95, 0.90)
        pending = match_svc.get_pending_for_admin()
        assert pending[0].confidence_score >= pending[1].confidence_score

    def test_get_by_id_not_found_raises(self, match_svc):
        with pytest.raises(MatchNotFoundException):
            match_svc.get_by_id("nonexistent")
