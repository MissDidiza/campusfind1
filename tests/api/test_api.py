"""
test_api.py — Integration Tests for FastAPI Endpoints
Uses FastAPI TestClient (no server needed).
"""
import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.dependencies import _container  # reset between tests

client = TestClient(app)


# ── Helpers ───────────────────────────────────────────────────────

def register_and_verify(email="test@university.ac.za", name="Test User"):
    res = client.post("/api/users/register", json={
        "full_name": name,
        "email": email,
        "password": "Password123!"
    })
    assert res.status_code == 201
    user_id = res.json()["user_id"]
    client.post(f"/api/users/verify/{user_id}")
    return user_id


def create_report(user_id, rtype="LOST"):
    res = client.post("/api/reports/", json={
        "user_id": user_id,
        "report_type": rtype,
        "item_name": "Black Nike Backpack",
        "category": "ACCESSORIES",
        "description": "Black Nike backpack with broken zip on left pocket and UCT keyring",
        "location": "Library Second Floor",
        "date_lost_or_found": "2026-03-10"
    })
    assert res.status_code == 201
    return res.json()["report_id"]


# ── Health Tests ──────────────────────────────────────────────────

class TestHealth:
    def test_root_returns_running(self):
        res = client.get("/")
        assert res.status_code == 200
        assert res.json()["status"] == "running"

    def test_health_check(self):
        res = client.get("/health")
        assert res.status_code == 200
        assert res.json()["status"] == "healthy"


# ── User API Tests ────────────────────────────────────────────────

class TestUserAPI:

    def test_register_success(self):
        res = client.post("/api/users/register", json={
            "full_name": "API Test User",
            "email": "apitest@university.ac.za",
            "password": "Password123!"
        })
        assert res.status_code == 201
        assert res.json()["email"] == "apitest@university.ac.za"

    def test_register_invalid_domain_returns_400(self):
        res = client.post("/api/users/register", json={
            "full_name": "Bad Email",
            "email": "bad@gmail.com",
            "password": "Password123!"
        })
        assert res.status_code == 400

    def test_register_duplicate_email_returns_409(self):
        client.post("/api/users/register", json={
            "full_name": "Dup User",
            "email": "dup2@university.ac.za",
            "password": "Password123!"
        })
        res = client.post("/api/users/register", json={
            "full_name": "Dup User 2",
            "email": "dup2@university.ac.za",
            "password": "Password123!"
        })
        assert res.status_code == 409

    def test_login_success(self):
        user_id = register_and_verify("login_test@university.ac.za")
        res = client.post("/api/users/login", json={
            "email": "login_test@university.ac.za",
            "password": "Password123!"
        })
        assert res.status_code == 200
        assert res.json()["is_verified"] is True

    def test_login_wrong_password_returns_401(self):
        register_and_verify("wrongpw@university.ac.za")
        res = client.post("/api/users/login", json={
            "email": "wrongpw@university.ac.za",
            "password": "WrongPassword!"
        })
        assert res.status_code == 401

    def test_get_user_by_id(self):
        user_id = register_and_verify("getbyid@university.ac.za")
        res = client.get(f"/api/users/{user_id}")
        assert res.status_code == 200
        assert res.json()["user_id"] == user_id

    def test_get_user_not_found_returns_404(self):
        res = client.get("/api/users/nonexistent-id")
        assert res.status_code == 404

    def test_update_profile(self):
        user_id = register_and_verify("updateme@university.ac.za")
        res = client.put(f"/api/users/{user_id}", json={"full_name": "Updated Name"})
        assert res.status_code == 200
        assert res.json()["full_name"] == "Updated Name"

    def test_deactivate_user(self):
        user_id = register_and_verify("deactivate@university.ac.za")
        res = client.delete(f"/api/users/{user_id}")
        assert res.status_code == 200
        assert "deactivated" in res.json()["message"]



    def test_get_users_supports_pagination(self):
        register_and_verify("pageuser1@university.ac.za", "Page User 1")
        register_and_verify("pageuser2@university.ac.za", "Page User 2")
        register_and_verify("pageuser3@university.ac.za", "Page User 3")

        res = client.get("/api/users/?page=1&limit=2")

        assert res.status_code == 200
        assert len(res.json()) == 2

    def test_pagination_rejects_invalid_page_value(self):
        res = client.get("/api/users/?page=0&limit=10")

        assert res.status_code == 422

# ── Report API Tests ──────────────────────────────────────────────

class TestReportAPI:

    def test_create_lost_report(self):
        user_id = register_and_verify("reporter@university.ac.za")
        res = client.post("/api/reports/", json={
            "user_id": user_id,
            "report_type": "LOST",
            "item_name": "Wallet",
            "category": "ACCESSORIES",
            "description": "Brown leather wallet with student ID and two bank cards inside",
            "location": "Cafeteria Block B",
            "date_lost_or_found": "2026-03-10"
        })
        assert res.status_code == 201
        assert res.json()["report_type"] == "LOST"

    def test_create_report_short_description_returns_400(self):
        user_id = register_and_verify("shortdesc@university.ac.za")
        res = client.post("/api/reports/", json={
            "user_id": user_id,
            "report_type": "LOST",
            "item_name": "Item",
            "category": "OTHER",
            "description": "Too short",
            "location": "Somewhere",
            "date_lost_or_found": "2026-03-10"
        })
        assert res.status_code == 400

    def test_get_report_by_id(self):
        user_id = register_and_verify("getreport@university.ac.za")
        report_id = create_report(user_id)
        res = client.get(f"/api/reports/{report_id}")
        assert res.status_code == 200
        assert res.json()["report_id"] == report_id

    def test_get_report_not_found_returns_404(self):
        res = client.get("/api/reports/nonexistent")
        assert res.status_code == 404

    def test_get_reports_by_user(self):
        user_id = register_and_verify("byuser@university.ac.za")
        create_report(user_id)
        create_report(user_id, "FOUND")
        res = client.get(f"/api/reports/user/{user_id}")
        assert res.status_code == 200
        assert len(res.json()) == 2

    def test_update_report(self):
        user_id = register_and_verify("updreport@university.ac.za")
        report_id = create_report(user_id)
        res = client.put(f"/api/reports/{report_id}", json={
            "user_id": user_id,
            "location": "New Updated Location Here"
        })
        assert res.status_code == 200
        assert res.json()["location"] == "New Updated Location Here"

    def test_update_wrong_user_returns_403(self):
        user_id = register_and_verify("own1@university.ac.za")
        report_id = create_report(user_id)
        res = client.put(f"/api/reports/{report_id}", json={
            "user_id": "wrong-user-id",
            "location": "Some location"
        })
        assert res.status_code == 403

    def test_delete_report(self):
        user_id = register_and_verify("delreport@university.ac.za")
        report_id = create_report(user_id)
        res = client.delete(f"/api/reports/{report_id}?user_id={user_id}")
        assert res.status_code == 200



    def test_get_reports_supports_pagination(self):
        user_id = register_and_verify("pagereports@university.ac.za")
        create_report(user_id, "LOST")
        create_report(user_id, "FOUND")
        create_report(user_id, "LOST")

        res = client.get("/api/reports/?page=1&limit=2")

        assert res.status_code == 200
        assert len(res.json()) == 2

# ── Match API Tests ───────────────────────────────────────────────

class TestMatchAPI:

    def test_create_match_above_threshold(self):
        u1 = register_and_verify("matchuser1@university.ac.za")
        u2 = register_and_verify("matchuser2@university.ac.za")
        lost_id = create_report(u1, "LOST")
        found_id = create_report(u2, "FOUND")
        res = client.post("/api/matches/", json={
            "lost_report_id": lost_id,
            "found_report_id": found_id,
            "text_similarity": 0.90,
            "image_similarity": 0.85
        })
        assert res.status_code == 201
        assert res.json()["confidence_score"] >= 0.70

    def test_create_match_below_threshold_returns_400(self):
        u1 = register_and_verify("lowconf1@university.ac.za")
        u2 = register_and_verify("lowconf2@university.ac.za")
        lost_id = create_report(u1, "LOST")
        found_id = create_report(u2, "FOUND")
        res = client.post("/api/matches/", json={
            "lost_report_id": lost_id,
            "found_report_id": found_id,
            "text_similarity": 0.30,
            "image_similarity": 0.20
        })
        assert res.status_code == 400

    def test_confirm_match(self):
        u1 = register_and_verify("conf1@university.ac.za")
        u2 = register_and_verify("conf2@university.ac.za")
        lost_id = create_report(u1, "LOST")
        found_id = create_report(u2, "FOUND")
        match_res = client.post("/api/matches/", json={
            "lost_report_id": lost_id,
            "found_report_id": found_id,
            "text_similarity": 0.90,
            "image_similarity": 0.85
        })
        match_id = match_res.json()["match_id"]
        res = client.post(f"/api/matches/{match_id}/confirm",
                          json={"admin_id": "admin-1"})
        assert res.status_code == 200
        assert res.json()["status"] == "CONFIRMED"

    def test_dismiss_match(self):
        u1 = register_and_verify("dis1@university.ac.za")
        u2 = register_and_verify("dis2@university.ac.za")
        lost_id = create_report(u1, "LOST")
        found_id = create_report(u2, "FOUND")
        match_res = client.post("/api/matches/", json={
            "lost_report_id": lost_id,
            "found_report_id": found_id,
            "text_similarity": 0.90,
            "image_similarity": 0.85
        })
        match_id = match_res.json()["match_id"]
        res = client.post(f"/api/matches/{match_id}/dismiss", json={
            "admin_id": "admin-1",
            "reason": "Items are different colours"
        })
        assert res.status_code == 200
        assert res.json()["status"] == "DISMISSED"

    def test_get_match_not_found_returns_404(self):
        res = client.get("/api/matches/nonexistent")
        assert res.status_code == 404
