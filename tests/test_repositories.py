"""
test_repositories.py — Unit Tests for All Repository Implementations
=====================================================================
Tests cover: CRUD operations, domain-specific queries, edge cases,
and the RepositoryFactory / DIContainer abstraction mechanism.
All tests use InMemory implementations — no external dependencies.
"""
import pytest
from datetime import date, datetime
from src.user import User
from src.report import Report
from src.photo import Photo
from src.match_record import MatchRecord
from src.handover import Handover
from src.notification import Notification
from src.enums import (
    UserRole, ReportType, ReportStatus, ItemCategory,
    MatchStatus, HandoverStatus, NotificationType, NotificationChannel
)
from repositories.inmemory.user_repository import InMemoryUserRepository
from repositories.inmemory.report_repository import InMemoryReportRepository
from repositories.inmemory.photo_repository import InMemoryPhotoRepository
from repositories.inmemory.match_repository import InMemoryMatchRecordRepository
from repositories.inmemory.handover_repository import InMemoryHandoverRepository
from repositories.inmemory.notification_repository import InMemoryNotificationRepository
from factories.repository_factory import RepositoryFactory, DIContainer


# ── Shared Fixtures ───────────────────────────────────────────────

def make_user(email="student@university.ac.za", role=UserRole.STUDENT) -> User:
    pw = User.hash_password("Password123!")
    u = User("Test User", email, pw, role)
    u.verify_email()
    return u


def make_report(user_id="user-1", rtype=ReportType.LOST) -> Report:
    return Report(
        user_id=user_id,
        report_type=rtype,
        item_name="Black Nike Backpack",
        category=ItemCategory.ACCESSORIES,
        description="Black Nike backpack with broken zip on left pocket and UCT keyring",
        location="Library Second Floor",
        date_lost_or_found=date.today(),
    )


def make_photo(report_id="report-1") -> Photo:
    return Photo(
        report_id=report_id,
        cloudinary_url="https://res.cloudinary.com/test/image.jpg",
        cloudinary_public_id="test/image",
        file_size_kb=1024,
        mime_type="image/jpeg",
    )


def make_match(lost_id="lost-1", found_id="found-1",
               text=0.85, image=0.80) -> MatchRecord:
    return MatchRecord(lost_id, found_id, text, image)


def make_handover(match_id="m1", admin_id="admin-1", student_id="student-1") -> Handover:
    return Handover(match_id, "lost-1", "found-1", admin_id, student_id)


def make_notification(user_id="user-1") -> Notification:
    return Notification(
        user_id=user_id,
        notification_type=NotificationType.MATCH_ALERT,
        channel=NotificationChannel.BOTH,
        subject="Match found!",
        body="Your item has a probable match.",
    )


# ── User Repository Tests ─────────────────────────────────────────

class TestInMemoryUserRepository:

    @pytest.fixture
    def repo(self):
        return InMemoryUserRepository()

    def test_save_and_find_by_id(self, repo):
        user = make_user()
        repo.save(user)
        found = repo.find_by_id(user.user_id)
        assert found is not None
        assert found.user_id == user.user_id

    def test_find_by_id_returns_none_for_unknown(self, repo):
        assert repo.find_by_id("nonexistent-id") is None

    def test_save_updates_existing_user(self, repo):
        user = make_user()
        repo.save(user)
        user.update_profile("Updated Name")
        repo.save(user)
        assert repo.count() == 1
        assert repo.find_by_id(user.user_id).full_name == "Updated Name"

    def test_find_all_returns_all_saved_users(self, repo):
        repo.save(make_user("a@university.ac.za"))
        repo.save(make_user("b@university.ac.za"))
        repo.save(make_user("c@university.ac.za"))
        assert len(repo.find_all()) == 3

    def test_delete_existing_user(self, repo):
        user = make_user()
        repo.save(user)
        result = repo.delete(user.user_id)
        assert result is True
        assert repo.find_by_id(user.user_id) is None

    def test_delete_nonexistent_returns_false(self, repo):
        assert repo.delete("ghost-id") is False

    def test_exists_returns_true_after_save(self, repo):
        user = make_user()
        repo.save(user)
        assert repo.exists(user.user_id) is True

    def test_exists_returns_false_before_save(self, repo):
        assert repo.exists("not-saved") is False

    def test_count_reflects_saved_users(self, repo):
        assert repo.count() == 0
        repo.save(make_user("x@university.ac.za"))
        assert repo.count() == 1

    def test_find_by_email(self, repo):
        user = make_user("unique@university.ac.za")
        repo.save(user)
        found = repo.find_by_email("unique@university.ac.za")
        assert found is not None
        assert found.email == "unique@university.ac.za"

    def test_find_by_email_case_insensitive(self, repo):
        user = make_user("Mixed@University.ac.za")
        repo.save(user)
        assert repo.find_by_email("mixed@university.ac.za") is not None

    def test_find_by_email_returns_none_for_unknown(self, repo):
        assert repo.find_by_email("nobody@university.ac.za") is None

    def test_find_by_role_returns_correct_users(self, repo):
        student = make_user("s@university.ac.za", UserRole.STUDENT)
        admin = make_user("a@university.ac.za", UserRole.ADMIN)
        repo.save(student)
        repo.save(admin)
        admins = repo.find_by_role(UserRole.ADMIN)
        assert len(admins) == 1
        assert admins[0].role == UserRole.ADMIN

    def test_find_unverified_returns_unverified_users(self, repo):
        pw = User.hash_password("pass")
        unverified = User("Unverified", "unv@university.ac.za", pw)
        # NOT calling verify_email()
        repo.save(unverified)
        result = repo.find_unverified()
        assert len(result) == 1
        assert result[0].email == "unv@university.ac.za"


# ── Report Repository Tests ───────────────────────────────────────

class TestInMemoryReportRepository:

    @pytest.fixture
    def repo(self):
        return InMemoryReportRepository()

    def test_save_and_find_by_id(self, repo):
        report = make_report()
        repo.save(report)
        assert repo.find_by_id(report.report_id) is not None

    def test_find_by_id_unknown_returns_none(self, repo):
        assert repo.find_by_id("unknown") is None

    def test_find_all(self, repo):
        repo.save(make_report("u1", ReportType.LOST))
        repo.save(make_report("u2", ReportType.FOUND))
        assert len(repo.find_all()) == 2

    def test_delete(self, repo):
        report = make_report()
        repo.save(report)
        assert repo.delete(report.report_id) is True
        assert repo.find_by_id(report.report_id) is None

    def test_count(self, repo):
        assert repo.count() == 0
        repo.save(make_report())
        assert repo.count() == 1

    def test_find_by_user_id(self, repo):
        r1 = make_report("user-A")
        r2 = make_report("user-A")
        r3 = make_report("user-B")
        repo.save(r1)
        repo.save(r2)
        repo.save(r3)
        results = repo.find_by_user_id("user-A")
        assert len(results) == 2

    def test_find_by_type_and_status(self, repo):
        lost = make_report("u1", ReportType.LOST)
        found = make_report("u2", ReportType.FOUND)
        repo.save(lost)
        repo.save(found)
        results = repo.find_by_type_and_status(ReportType.LOST, ReportStatus.OPEN)
        assert len(results) == 1
        assert results[0].report_type == ReportType.LOST

    def test_find_open_by_type(self, repo):
        r1 = make_report("u1", ReportType.LOST)
        r2 = make_report("u2", ReportType.LOST)
        r2.update_status(ReportStatus.MATCHED)
        repo.save(r1)
        repo.save(r2)
        open_reports = repo.find_open_by_type(ReportType.LOST)
        assert len(open_reports) == 1

    def test_find_by_status(self, repo):
        r = make_report()
        r.update_status(ReportStatus.RESOLVED)
        repo.save(r)
        resolved = repo.find_by_status(ReportStatus.RESOLVED)
        assert len(resolved) == 1

    def test_find_archived_older_than_days_empty_for_fresh_reports(self, repo):
        r = make_report()
        r.archive()
        repo.save(r)
        # Fresh report — should NOT appear in "older than 90 days"
        old = repo.find_archived_older_than_days(90)
        assert len(old) == 0


# ── Photo Repository Tests ────────────────────────────────────────

class TestInMemoryPhotoRepository:

    @pytest.fixture
    def repo(self):
        return InMemoryPhotoRepository()

    def test_save_and_find(self, repo):
        photo = make_photo("report-1")
        repo.save(photo)
        assert repo.find_by_id(photo.photo_id) is not None

    def test_find_by_report_id(self, repo):
        p1 = make_photo("report-1")
        p2 = make_photo("report-1")
        p3 = make_photo("report-2")
        repo.save(p1)
        repo.save(p2)
        repo.save(p3)
        assert len(repo.find_by_report_id("report-1")) == 2

    def test_find_active_by_report_id_excludes_deleted(self, repo):
        p1 = make_photo("report-1")
        p2 = make_photo("report-1")
        p2.delete()
        repo.save(p1)
        repo.save(p2)
        active = repo.find_active_by_report_id("report-1")
        assert len(active) == 1
        assert not active[0].is_deleted

    def test_delete_by_report_id(self, repo):
        p1 = make_photo("report-1")
        p2 = make_photo("report-1")
        p3 = make_photo("report-2")
        repo.save(p1)
        repo.save(p2)
        repo.save(p3)
        deleted_count = repo.delete_by_report_id("report-1")
        assert deleted_count == 2
        assert repo.count() == 1

    def test_delete_by_report_id_returns_zero_for_unknown(self, repo):
        assert repo.delete_by_report_id("nonexistent") == 0


# ── MatchRecord Repository Tests ──────────────────────────────────

class TestInMemoryMatchRecordRepository:

    @pytest.fixture
    def repo(self):
        return InMemoryMatchRecordRepository()

    def test_save_and_find(self, repo):
        match = make_match()
        repo.save(match)
        assert repo.find_by_id(match.match_id) is not None

    def test_find_by_lost_report_id(self, repo):
        m1 = make_match("lost-A", "found-1")
        m2 = make_match("lost-A", "found-2")
        m3 = make_match("lost-B", "found-3")
        repo.save(m1)
        repo.save(m2)
        repo.save(m3)
        assert len(repo.find_by_lost_report_id("lost-A")) == 2

    def test_find_pending_for_admin_sorted_by_confidence(self, repo):
        m1 = make_match("l1", "f1", text=0.70, image=0.60)  # lower confidence
        m2 = make_match("l2", "f2", text=0.90, image=0.95)  # higher confidence
        m1.notify()
        m2.notify()
        repo.save(m1)
        repo.save(m2)
        pending = repo.find_pending_for_admin()
        assert len(pending) == 2
        # Higher confidence should come first
        assert pending[0].confidence_score >= pending[1].confidence_score

    def test_find_above_threshold(self, repo):
        high = make_match("l1", "f1", 0.90, 0.85)
        low = make_match("l2", "f2", 0.50, 0.40)
        repo.save(high)
        repo.save(low)
        above = repo.find_above_threshold(0.70)
        assert len(above) == 1
        assert above[0].confidence_score >= 0.70

    def test_find_by_status(self, repo):
        m = make_match()
        m.notify()
        m.confirm("admin-1")
        repo.save(m)
        confirmed = repo.find_by_status(MatchStatus.CONFIRMED)
        assert len(confirmed) == 1

    def test_delete(self, repo):
        match = make_match()
        repo.save(match)
        assert repo.delete(match.match_id) is True
        assert repo.find_by_id(match.match_id) is None


# ── Handover Repository Tests ─────────────────────────────────────

class TestInMemoryHandoverRepository:

    @pytest.fixture
    def repo(self):
        return InMemoryHandoverRepository()

    def test_save_and_find(self, repo):
        h = make_handover()
        repo.save(h)
        assert repo.find_by_id(h.handover_id) is not None

    def test_find_by_student_id(self, repo):
        h1 = make_handover(student_id="student-A")
        h2 = make_handover(student_id="student-A")
        h3 = make_handover(student_id="student-B")
        repo.save(h1)
        repo.save(h2)
        repo.save(h3)
        assert len(repo.find_by_student_id("student-A")) == 2

    def test_find_by_admin_id(self, repo):
        h = make_handover(admin_id="admin-99")
        repo.save(h)
        assert len(repo.find_by_admin_id("admin-99")) == 1

    def test_find_by_status(self, repo):
        h = make_handover()
        h.record_collection()
        repo.save(h)
        collected = repo.find_by_status(HandoverStatus.COLLECTED)
        assert len(collected) == 1

    def test_count(self, repo):
        repo.save(make_handover("m1"))
        repo.save(make_handover("m2"))
        assert repo.count() == 2


# ── Notification Repository Tests ─────────────────────────────────

class TestInMemoryNotificationRepository:

    @pytest.fixture
    def repo(self):
        return InMemoryNotificationRepository()

    def test_save_and_find(self, repo):
        n = make_notification()
        repo.save(n)
        assert repo.find_by_id(n.notification_id) is not None

    def test_find_by_user_id(self, repo):
        n1 = make_notification("user-A")
        n2 = make_notification("user-A")
        n3 = make_notification("user-B")
        repo.save(n1)
        repo.save(n2)
        repo.save(n3)
        assert len(repo.find_by_user_id("user-A")) == 2

    def test_find_unread_by_user_id(self, repo):
        n1 = make_notification("user-A")
        n2 = make_notification("user-A")
        n2.mark_read()
        repo.save(n1)
        repo.save(n2)
        unread = repo.find_unread_by_user_id("user-A")
        assert len(unread) == 1
        assert not unread[0].is_read

    def test_find_failed(self, repo):
        n = make_notification()
        n.log_failure("SendGrid timeout")
        repo.save(n)
        failed = repo.find_failed()
        assert len(failed) == 1

    def test_mark_all_read_for_user(self, repo):
        n1 = make_notification("user-X")
        n2 = make_notification("user-X")
        repo.save(n1)
        repo.save(n2)
        count = repo.mark_all_read_for_user("user-X")
        assert count == 2
        assert len(repo.find_unread_by_user_id("user-X")) == 0

    def test_delete(self, repo):
        n = make_notification()
        repo.save(n)
        assert repo.delete(n.notification_id) is True
        assert repo.count() == 0


# ── RepositoryFactory Tests ───────────────────────────────────────

class TestRepositoryFactory:

    def test_memory_factory_returns_in_memory_repos(self):
        factory = RepositoryFactory("MEMORY")
        user_repo = factory.get_user_repository()
        assert isinstance(user_repo, InMemoryUserRepository)

    def test_memory_factory_report_repo(self):
        factory = RepositoryFactory("MEMORY")
        report_repo = factory.get_report_repository()
        assert isinstance(report_repo, InMemoryReportRepository)

    def test_invalid_storage_type_raises(self):
        with pytest.raises(ValueError, match="Unsupported storage type"):
            RepositoryFactory("ORACLE")

    def test_factory_case_insensitive(self):
        factory = RepositoryFactory("memory")
        assert isinstance(factory.get_user_repository(), InMemoryUserRepository)

    def test_file_backend_raises_not_implemented_for_photo(self):
        factory = RepositoryFactory("FILE")
        with pytest.raises(NotImplementedError):
            factory.get_photo_repository()

    def test_di_container_creates_all_repos(self):
        container = DIContainer("MEMORY")
        assert container.user_repo is not None
        assert container.report_repo is not None
        assert container.photo_repo is not None
        assert container.match_repo is not None
        assert container.handover_repo is not None
        assert container.notification_repo is not None

    def test_di_container_repos_are_independent_instances(self):
        container = DIContainer("MEMORY")
        user = make_user()
        container.user_repo.save(user)
        # Report repo should be empty — different instance
        assert container.report_repo.count() == 0

    def test_switching_backend_gives_fresh_repo(self):
        c1 = DIContainer("MEMORY")
        user = make_user()
        c1.user_repo.save(user)
        c2 = DIContainer("MEMORY")
        # New container = new repo instances = empty store
        assert c2.user_repo.count() == 0