# CHANGELOG.md — CampusFind: Smart Campus Lost & Found System

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Assignment 10] — 2026

### Added
- `/src` directory with full Python implementation of all 7 domain entity classes from Assignment 9 Class Diagram:
  - `src/enums.py` — All enumeration types (UserRole, ReportType, ReportStatus, ItemCategory, MatchStatus, HandoverStatus, NotificationType, NotificationStatus, NotificationChannel)
  - `src/user.py` — User entity with registration, email verification, password hashing, role checking
  - `src/report.py` — Report entity with validation, photo management, status transitions, match payload serialisation
  - `src/photo.py` — Photo entity with file validation, Cloudinary URL management, deletion
  - `src/match_record.py` — MatchRecord entity with confidence score calculation, confirm/dismiss workflow
  - `src/handover.py` — Handover entity with collection workflow, reminder tracking, manual override
  - `src/notification.py` — Notification entity with retry logic, read/expire tracking

- `/creational_patterns` directory with all 6 creational design pattern implementations:
  - `simple_factory.py` — NotificationFactory: centralised creation of all notification types
  - `factory_method.py` — LostReportCreator / FoundReportCreator: delegate report instantiation to subclass creators
  - `abstract_factory.py` — ProductionServiceFactory / TestingServiceFactory: families of email and storage service objects
  - `builder.py` — ReportBuilder + ReportDirector: step-by-step construction of complex Report objects
  - `prototype.py` — ReportPrototypeCache + CloneableReport: clone pre-configured report templates
  - `singleton.py` — MatchingConfig + DatabaseConnectionPool: single global instances with thread safety

- `/tests` directory with comprehensive unit tests:
  - `test_classes.py` — 35+ tests for all 7 domain entity classes covering happy paths, business rules, and edge cases
  - `test_creational_patterns.py` — 35+ tests for all 6 creational patterns including thread-safety test for Singleton

- `CHANGELOG.md` — This file

### Changed
- `README.md` — Updated with Assignment 10 section: language choice (Python), pattern rationales, directory structure, and run instructions

### Fixed
- N/A (first implementation sprint)

### GitHub Issues Closed
- #1 Implement User domain class ✅
- #2 Implement Report domain class ✅
- #3 Implement Photo, MatchRecord, Handover, Notification, Session classes ✅
- #4 Implement Simple Factory (NotificationFactory) ✅
- #5 Implement Factory Method (LostReportCreator / FoundReportCreator) ✅
- #6 Implement Abstract Factory (ProductionServiceFactory / TestingServiceFactory) ✅
- #7 Implement Builder (ReportBuilder + ReportDirector) ✅
- #8 Implement Prototype (ReportPrototypeCache) ✅
- #9 Implement Singleton (MatchingConfig + DatabaseConnectionPool) ✅
- #10 Write unit tests for all domain classes ✅
- #11 Write unit tests for all creational patterns ✅
- #12 Thread-safety test for Singleton ✅

---

## [Assignment 9] — 2026
### Added
- `DOMAIN_MODEL.md` — 7 domain entities with attributes, methods, relationships, business rules
- `CLASS_DIAGRAM.md` — Full Mermaid.js class diagram with 7 entity classes, 7 service classes, 9 enumerations

## [Assignment 8] — 2026
### Added
- `STATE_DIAGRAMS.md` — 8 UML state transition diagrams
- `ACTIVITY_DIAGRAMS.md` — 8 UML activity workflow diagrams

## [Assignment 7] — 2026
### Added
- `template_analysis.md`, `kanban_explanation.md`, `REFLECTION_A7.md`

## [Assignment 6] — 2026
### Added
- `AGILE_PLANNING.md` — User stories, product backlog, sprint plan

## [Assignment 5] — 2026
### Added
- `USE_CASES.md`, `TEST_CASES.md`

## [Assignment 4] — 2026
### Added
- `STAKEHOLDERS.md`, `REQUIREMENTS.md`

## [Assignment 3] — 2026
### Added
- `README.md`, `SPECIFICATION.md`, `ARCHITECTURE.md`

## [Assignment 11] — 2026

### Added
- `/repositories/base.py` — Generic `Repository[T, ID]` abstract interface with 6 CRUD methods
- `/repositories/interfaces.py` — 6 entity-specific repository interfaces (User, Report, Photo, MatchRecord, Handover, Notification) with domain-specific query methods
- `/repositories/inmemory/` — 6 full HashMap-based in-memory implementations
  - `user_repository.py` — InMemoryUserRepository (find_by_email, find_by_role, find_unverified)
  - `report_repository.py` — InMemoryReportRepository (find_by_type_and_status, find_open_by_type, find_archived_older_than_days)
  - `photo_repository.py` — InMemoryPhotoRepository (find_by_report_id, delete_by_report_id)
  - `match_repository.py` — InMemoryMatchRecordRepository (find_pending_for_admin sorted by confidence, find_above_threshold)
  - `handover_repository.py` — InMemoryHandoverRepository (find_awaiting_collection_older_than_days)
  - `notification_repository.py` — InMemoryNotificationRepository (find_unread, find_failed, mark_all_read_for_user)
- `/factories/repository_factory.py` — RepositoryFactory (MEMORY/FILE/DATABASE backends) + DIContainer (lightweight dependency injection)
- `/repositories/stubs/file_repository.py` — FileSystem stub with full SQL/JSON implementation notes
- `/repositories/stubs/database_repository.py` — PostgreSQL stub with full SQL schema and query comments
- `/tests/test_repositories.py` — 60+ unit tests covering all repositories, CRUD operations, domain queries, edge cases, and Factory/DI container

### GitHub Issues Created and Resolved
- #13 Design generic Repository interface ✅
- #14 Create entity-specific repository interfaces (6 interfaces) ✅
- #15 Implement InMemoryUserRepository with domain queries ✅
- #16 Implement InMemoryReportRepository ✅
- #17 Implement InMemoryPhotoRepository ✅
- #18 Implement InMemoryMatchRecordRepository ✅
- #19 Implement InMemoryHandoverRepository ✅
- #20 Implement InMemoryNotificationRepository ✅
- #21 Build RepositoryFactory with MEMORY/FILE/DATABASE backends ✅
- #22 Build DIContainer for dependency injection ✅
- #23 Create FileSystem repository stubs ✅
- #24 Create Database repository stubs with SQL schema ✅
- #25 Write 60+ repository unit tests ✅

## [Assignment 14] — 2026
 
### Added
- `CONTRIBUTING.md` — Full contributor guide: prerequisites, setup, coding standards, PR workflow
- `ROADMAP.md` — 30+ planned features across 6 phases, labelled by difficulty
- `LICENSE` — MIT License
- `VOTING_RESULTS.md` — Peer review tracking (stars, forks, feedback)
- `REFLECTION_A14.md` — 700-word reflection on open-source collaboration
- Updated `README.md` — Getting Started section, contribution table, license badge
### GitHub Issues to Create and Label
Label these issues on GitHub after pushing:
 
**good-first-issue (5+):**
- Add JWT token blacklisting with Redis
- Add environment variable config with python-dotenv
- Add pagination to list endpoints
- Add structured logging with Python logging module
- Connect real SendGrid email API
- Add CSV export endpoint
**feature-request (3+):**
- Implement PostgreSQL repository layer with SQLAlchemy
- Build React frontend for students
- Integrate sentence-transformers AI matching engine
 