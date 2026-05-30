# CONTRIBUTING.md — CampusFind: Smart Campus Lost & Found System

Thank you for your interest in contributing to CampusFind! This guide will help you get set up, understand the codebase, and submit your first pull request.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup Instructions](#setup-instructions)
3. [Project Structure](#project-structure)
4. [Coding Standards](#coding-standards)
5. [How to Pick an Issue](#how-to-pick-an-issue)
6. [How to Submit a Pull Request](#how-to-submit-a-pull-request)
7. [Running Tests](#running-tests)
8. [Getting Help](#getting-help)

---

## Prerequisites

Before you start, make sure you have the following installed:

| Tool | Version | How to install |
|---|---|---|
| Python | 3.11 or higher | https://www.python.org/downloads/ |
| Git | Any recent version | https://git-scm.com/downloads |
| VS Code (recommended) | Any | https://code.visualstudio.com/ |

---

## Setup Instructions

### Step 1 — Fork the repository
Click the **Fork** button at the top right of the GitHub repository page. This creates your own copy of the project.

### Step 2 — Clone your fork
```bash
git clone https://github.com/YOUR_USERNAME/campusfind1.git
cd campusfind1
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
pip install pytest pytest-cov
```

### Step 4 — Verify everything works
```bash
python -m pytest tests/ -v
```
You should see **120 tests passing**. If anything fails, open an issue and we will help you.

### Step 5 — Run the API locally
```bash
uvicorn api.main:app --reload
```
Open your browser at `http://localhost:8000/docs` to see the Swagger UI.

### Step 6 — Create a feature branch
Never work directly on `main`. Always create a new branch:
```bash
git checkout -b feature/your-feature-name
```

---

## Project Structure

```
campusfind1/
  src/                    # Domain entity classes (User, Report, Photo, etc.)
  repositories/           # Repository interfaces and in-memory implementations
  factories/              # RepositoryFactory and DIContainer
  services/               # Business logic (UserService, ReportService, MatchService)
  api/                    # FastAPI routers, schemas, and entry point
  tests/                  # All unit and integration tests
  docs/                   # API documentation and screenshots
  .github/workflows/      # CI/CD pipeline
```

---

## Coding Standards

### Style
- Follow **PEP 8** Python style guidelines
- Use **4 spaces** for indentation (no tabs)
- Maximum line length: **100 characters**
- All functions and classes must have **docstrings**

### Naming Conventions
- Classes: `PascalCase` (e.g., `UserService`)
- Functions and variables: `snake_case` (e.g., `find_by_email`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_PHOTOS`)
- Files: `snake_case.py` (e.g., `user_service.py`)

### Testing Requirements
- Every new feature **must** include unit tests
- Every bug fix **must** include a regression test
- Minimum test coverage for new code: **70%**
- Tests go in the `tests/` directory following the existing structure

### Linting
Before submitting a PR, run:
```bash
pip install flake8
flake8 src/ services/ api/ repositories/ --max-line-length=100
```
Fix any issues before opening a PR.

---

## How to Pick an Issue

1. Go to the **Issues** tab on GitHub
2. Look for issues labelled:
   - 🟢 `good-first-issue` — perfect for new contributors, clearly scoped
   - 🔵 `feature-request` — new features that need design and implementation
   - 🔴 `bug` — something that is broken and needs fixing
3. **Comment on the issue** saying you want to work on it — this prevents two people working on the same thing
4. Wait for a maintainer to assign it to you before starting

---

## How to Submit a Pull Request

### Step 1 — Make your changes on your feature branch
```bash
git add .
git commit -m "Brief description of what you changed"
```

### Step 2 — Push your branch to your fork
```bash
git push origin feature/your-feature-name
```

### Step 3 — Open a Pull Request
1. Go to your fork on GitHub
2. Click **Compare & pull request**
3. Fill in the PR template:
   - **What does this PR do?** — Describe the change clearly
   - **Which issue does it close?** — Write `Closes #issue_number`
   - **How was it tested?** — List the tests you wrote or ran
4. Click **Create pull request**

### Step 4 — Wait for CI and review
- The CI pipeline will automatically run all 120 tests
- If tests fail, fix them before requesting review
- A maintainer will review your code and may request changes
- Once approved, your PR will be merged into `main`

---

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run only service tests
python -m pytest tests/services/ -v

# Run only API tests
python -m pytest tests/api/ -v

# Run with coverage report
python -m pytest tests/ -v --cov=. --cov-report=term-missing
```

---

## Getting Help

- **Open an issue** if you find a bug or have a question
- **Check existing issues** before opening a new one — your question may already be answered
- **Be respectful** — this is a learning project and all contributors are welcome regardless of experience level

We are excited to have you contribute to CampusFind! 🎉