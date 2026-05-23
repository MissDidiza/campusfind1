# PROTECTION.md — Branch Protection Rules
## CampusFind: Smart Campus Lost & Found System

---

## What Branch Protection Rules Are Set Up

The `main` branch of the CampusFind repository is protected with the following rules configured under **Settings → Branches → Branch protection rules**:

| Rule | Setting | Why |
|---|---|---|
| Require pull request before merging | ✅ Enabled | No direct pushes to main allowed |
| Required approving reviews | 1 reviewer minimum | All code must be reviewed before merging |
| Require status checks to pass | ✅ CI pipeline must pass | Tests must pass before any merge |
| Require branches to be up to date | ✅ Enabled | Branch must be current with main before merging |
| Include administrators | ✅ Enabled | Rules apply to everyone including repo owner |
| Allow force pushes | ❌ Disabled | Prevents history rewriting on main |
| Allow deletions | ❌ Disabled | Prevents accidental deletion of main |

---

## How to Set These Rules on GitHub

1. Go to your repository on GitHub
2. Click **Settings** (top menu)
3. Click **Branches** (left sidebar)
4. Click **Add branch protection rule**
5. Under **Branch name pattern** type: `main`
6. Tick the following checkboxes:
   - ✅ **Require a pull request before merging**
     - Set **Required approving reviews** to `1`
   - ✅ **Require status checks to pass before merging**
     - Search for and select: `Run Tests` (your CI job name)
     - Tick **Require branches to be up to date before merging**
   - ✅ **Include administrators**
7. Click **Save changes**

---

## Why These Rules Matter

### 1. Require Pull Request Before Merging
Without this rule, any developer (including yourself) can push broken code directly to `main`. On a team project, this is especially dangerous because `main` is what gets deployed. Every change going through a PR means there is always at least one review step before code reaches production.

For CampusFind, this means even solo changes go through a PR, which forces a structured review of every feature before it is merged.

### 2. Require Status Checks (CI Must Pass)
This is the most important rule for code quality. It means GitHub will **block the merge button** if the CI pipeline (defined in `.github/workflows/ci.yml`) reports any test failures. 

For CampusFind, all 120 tests must pass before any PR can be merged to `main`. This ensures:
- No broken authentication endpoints reach production
- No report submission bugs are introduced
- No match management regressions slip through

### 3. Require Approving Reviews
Even as a solo developer, requiring at least one approval before merging forces a moment of deliberate review. In a team setting, this prevents one developer from bypassing the review process. It also creates an audit trail showing who approved what change and when.

### 4. Include Administrators
Without this, a repository owner (admin) can bypass all the protection rules. Enabling this means the rules apply to everyone equally, including the person who set them up. This is a governance best practice.

### 5. Disable Force Pushes
Force pushing to `main` rewrites git history, which can destroy the audit trail of what changed and when. Disabling this ensures the history of `main` is always accurate and traceable.

---

## How This Works with the CI Pipeline

When a developer opens a PR to merge into `main`:

```
Developer opens PR
        ↓
GitHub triggers CI workflow (ci.yml)
        ↓
CI runs: pip install → pytest tests/ -v (120 tests)
        ↓
    Tests PASS?
   ↙           ↘
YES              NO
↓                ↓
Green checkmark  Red X on PR
on PR            Merge button BLOCKED
↓                Developer must fix tests
Reviewer approves
↓
PR can be merged
↓
CD job runs: builds wheel artifact
↓
Release created on GitHub
```

This workflow ensures that `main` always contains tested, reviewed, working code.

---

## Why This Matters for CampusFind Specifically

CampusFind handles student personal data (names, emails, student numbers) and must comply with POPIA. A bug in the authentication or data deletion code that reaches production could cause a data breach or compliance failure. Branch protection rules ensure that every change to these critical code paths is tested and reviewed before deployment — not just as a development best practice but as a data governance requirement.
