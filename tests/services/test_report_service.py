"""
test_report_service.py — Unit Tests for ReportService
"""
import pytest
from datetime import date
from repositories.inmemory.report_repository import InMemoryReportRepository
from repositories.inmemory.photo_repository import InMemoryPhotoRepository
from services.report_service import ReportService
from services.exceptions import (
    ReportNotFoundException,
    ReportNotEditableException,
    ReportValidationException,
    UnauthorisedActionException,
)
from src.enums import ReportType, ReportStatus


@pytest.fixture
def svc():
    return ReportService(InMemoryReportRepository(), InMemoryPhotoRepository())


@pytest.fixture
def lost_report(svc):
    return svc.create_report(
        user_id="user-1",
        report_type="LOST",
        item_name="Black Nike Backpack",
        category="ACCESSORIES",
        description="Black Nike backpack with broken zip on left pocket and UCT keyring",
        location="Library Second Floor",
        date_lost_or_found=date.today(),
    )


class TestReportServiceCreate:

    def test_create_lost_report(self, svc, lost_report):
        assert lost_report.report_type == ReportType.LOST
        assert lost_report.status == ReportStatus.OPEN

    def test_create_found_report(self, svc):
        report = svc.create_report(
            "user-2", "FOUND", "Set of Keys", "KEYS",
            "Keys with blue lanyard and small torch attached",
            "Cafeteria Entrance", date.today()
        )
        assert report.report_type == ReportType.FOUND

    def test_invalid_report_type_raises(self, svc):
        with pytest.raises(ReportValidationException, match="Invalid report type"):
            svc.create_report(
                "u", "MISPLACED", "Item", "OTHER",
                "Some description that is long enough here",
                "Location", date.today()
            )

    def test_invalid_category_raises(self, svc):
        with pytest.raises(ReportValidationException, match="Invalid category"):
            svc.create_report(
                "u", "LOST", "Item", "FURNITURE",
                "Some description that is long enough here",
                "Location", date.today()
            )

    def test_short_description_raises(self, svc):
        with pytest.raises(ReportValidationException, match="20 characters"):
            svc.create_report(
                "u", "LOST", "Item", "OTHER",
                "Too short",
                "Location", date.today()
            )


class TestReportServiceRead:

    def test_get_by_id(self, svc, lost_report):
        found = svc.get_by_id(lost_report.report_id)
        assert found.report_id == lost_report.report_id

    def test_get_by_id_not_found_raises(self, svc):
        with pytest.raises(ReportNotFoundException):
            svc.get_by_id("nonexistent")

    def test_get_by_user(self, svc, lost_report):
        reports = svc.get_by_user("user-1")
        assert len(reports) == 1

    def test_get_open_lost_reports(self, svc, lost_report):
        results = svc.get_open_lost_reports()
        assert any(r.report_id == lost_report.report_id for r in results)

    def test_get_all(self, svc, lost_report):
        svc.create_report(
            "u2", "FOUND", "Keys", "KEYS",
            "Keys with blue lanyard and small torch attached",
            "Gate", date.today()
        )
        assert len(svc.get_all()) == 2


class TestReportServiceUpdate:

    def test_update_description(self, svc, lost_report):
        updated = svc.update_report(
            lost_report.report_id, "user-1",
            description="Updated description that is long enough to pass validation"
        )
        assert "Updated" in updated.description

    def test_update_wrong_user_raises(self, svc, lost_report):
        with pytest.raises(UnauthorisedActionException):
            svc.update_report(lost_report.report_id, "wrong-user", item_name="New")

    def test_update_locked_report_raises(self, svc, lost_report):
        lost_report.update_status(ReportStatus.MATCHED)
        svc._report_repo.save(lost_report)
        with pytest.raises(ReportNotEditableException):
            svc.update_report(lost_report.report_id, "user-1", item_name="New")

    def test_update_short_description_raises(self, svc, lost_report):
        with pytest.raises(ReportValidationException):
            svc.update_report(lost_report.report_id, "user-1", description="Short")


class TestReportServiceDelete:

    def test_delete_own_report(self, svc, lost_report):
        svc.delete_report(lost_report.report_id, "user-1")
        report = svc.get_by_id(lost_report.report_id)
        assert report.status == ReportStatus.ARCHIVED

    def test_delete_wrong_user_raises(self, svc, lost_report):
        with pytest.raises(UnauthorisedActionException):
            svc.delete_report(lost_report.report_id, "wrong-user")

    def test_delete_matched_report_raises(self, svc, lost_report):
        lost_report.update_status(ReportStatus.MATCHED)
        svc._report_repo.save(lost_report)
        with pytest.raises(ReportNotEditableException):
            svc.delete_report(lost_report.report_id, "user-1")
