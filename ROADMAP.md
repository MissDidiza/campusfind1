# ROADMAP.md — CampusFind: Smart Campus Lost & Found System

This roadmap outlines the planned features and improvements for CampusFind beyond the current semester implementation. Items are grouped by priority and complexity to help contributors pick tasks that match their skill level.

---

## Current Status (Completed — Assignments 3–13)

| Feature | Status |
|---|---|
| User registration and email verification | ✅ Done |
| JWT authentication and session management | ✅ Done |
| Lost and found report submission with photos | ✅ Done |
| AI match record management (confidence scoring) | ✅ Done |
| Admin match confirmation and dismissal workflow | ✅ Done |
| Digital handover workflow with audit trail | ✅ Done |
| In-memory repository layer | ✅ Done |
| REST API with FastAPI and Swagger docs | ✅ Done |
| 120 unit and integration tests | ✅ Done |
| CI/CD pipeline with GitHub Actions | ✅ Done |
| Branch protection and PR workflow | ✅ Done |

---

## Phase 2 — Core Infrastructure (Next Priority)

These features are needed to make CampusFind production-ready.

### 🔴 High Priority

| Feature | Description | Difficulty | Label |
|---|---|---|---|
| PostgreSQL database integration | Replace in-memory repositories with real PostgreSQL using SQLAlchemy. SQL schemas are already documented in `repositories/stubs/database_repository.py` | Medium | `good-first-issue` |
| Redis job queue integration | Connect the background worker to a real Redis instance for async AI matching jobs | Medium | `feature-request` |
| JWT token blacklisting | Store revoked tokens in Redis to fully implement logout (currently session is client-side only) | Easy | `good-first-issue` |
| Cloudinary photo upload integration | Connect the real Cloudinary API to replace the mock URL storage | Easy | `good-first-issue` |
| SendGrid email integration | Connect the real SendGrid API to send match alerts and handover notifications | Easy | `good-first-issue` |
| Environment variable configuration | Move all hardcoded config (DSN, API keys, thresholds) to `.env` file using `python-dotenv` | Easy | `good-first-issue` |

---

## Phase 3 — AI Matching Engine

| Feature | Description | Difficulty | Label |
|---|---|---|---|
| Real text similarity with sentence-transformers | Replace the simulated confidence scores with real semantic embedding comparison using `sentence-transformers` library | Hard | `feature-request` |
| Image similarity with MobileNetV2 | Add image feature extraction using TensorFlow/MobileNetV2 for photo-based matching | Hard | `feature-request` |
| Matching microservice (FastAPI) | Extract the AI matching logic into a separate FastAPI microservice that the main API calls via HTTP | Hard | `feature-request` |
| Configurable confidence threshold | Allow super admins to adjust the matching threshold (currently hardcoded at 70%) via the API | Easy | `good-first-issue` |

---

## Phase 4 — User Experience

| Feature | Description | Difficulty | Label |
|---|---|---|---|
| React frontend | Build the student-facing web portal in React 18 with Tailwind CSS | Hard | `feature-request` |
| Admin dashboard UI | Build the admin match review and handover management interface | Hard | `feature-request` |
| Password reset via email | Implement the forgot password flow using a time-limited reset token | Medium | `good-first-issue` |
| Email notification opt-out | Allow students to disable email notifications from their profile settings | Easy | `good-first-issue` |
| Report search and filter | Add search by item name, category, location, and date range on the reports endpoint | Medium | `feature-request` |
| Pagination | Add cursor-based pagination to all list endpoints (`GET /api/reports/`, `GET /api/users/`) | Easy | `good-first-issue` |

---

## Phase 5 — Operations and Compliance

| Feature | Description | Difficulty | Label |
|---|---|---|---|
| POPIA automated deletion job | Implement the nightly background job that archives resolved reports and deletes personal data after 120 days | Medium | `feature-request` |
| Statistics dashboard endpoint | Add `GET /api/stats` returning recovery rates, top locations, and category breakdowns | Medium | `feature-request` |
| CSV export endpoint | Add `GET /api/stats/export` that returns a downloadable CSV of anonymised report data | Easy | `good-first-issue` |
| Docker Compose deployment | Create a `docker-compose.yml` that spins up the API, PostgreSQL, and Redis together | Medium | `feature-request` |
| API rate limiting | Add per-IP rate limiting to prevent abuse of the registration and report submission endpoints | Medium | `feature-request` |
| Structured logging | Replace `print()` statements with structured JSON logging using Python's `logging` module | Easy | `good-first-issue` |

---

## Phase 6 — Future Extensions (Long-term)

| Feature | Description |
|---|---|
| Mobile app (React Native) | Native iOS and Android app for students to submit reports with camera access |
| Multi-campus support | Allow the system to support multiple university campuses with separate admin teams |
| Real-time notifications | WebSocket-based push notifications so students are alerted instantly without email |
| QR code item tagging | Generate QR codes for high-risk items (e.g., laptops) that link directly to a found report form |
| Analytics dashboard | Visual charts showing recovery trends, seasonal loss patterns, and campus hotspots |

---

## How to Contribute to the Roadmap

If you have a feature idea that is not on this list:
1. Open a **GitHub Issue** with the label `feature-request`
2. Describe the feature, why it is valuable, and how it fits the existing architecture
3. The maintainer will review and add it to the roadmap if it aligns with the project goals

See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to get started.