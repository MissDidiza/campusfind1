# MERGED_PRS.md — Merged Pull Requests
## CampusFind: Smart Campus Lost & Found System — Assignment 15

---

## Summary

This document tracks all pull requests I submitted to classmates' repositories and their merge status.

| PR # | Repository | Title | Status | Link |
|---|---|---|---|---|
| 1 | PRASA-System | Feature: Add modulo operation to calculator | Pending ⏳ | https://github.com/Makunga0471/PRASA-System/pull/1 |
| 2 | (classmate repo) | (PR title) | Merged ✅ / Pending ⏳ | (GitHub PR URL) |
| 3 | (classmate repo) | (PR title) | Merged ✅ / Pending ⏳ | (GitHub PR URL) |

---

## PR 1 — Details

| Field | Detail |
|---|---|
| **Repository** | https://github.com/Makunga0471/PRASA-System |
| **Branch created** | `feature/add-modulo-operation` |
| **Issue addressed** | Modulo operation feature |
| **PR Link** | https://github.com/Makunga0471/PRASA-System/pull/1 |
| **Status** | Pending ⏳ |
| **Merged on** | (update when merged) |

### Summary of Changes
Added a modulo (remainder) operation to the PRASA calculator. The original calculator only had add, subtract, multiply and divide. I added a modulo function with full input validation, added it as option 5 in the menu, and wrote 5 unit tests covering basic use, floats, zero division, and None input. Also fixed existing syntax errors in app.py and test_app.py that were preventing tests from running.

### Files Changed
- `app.py` — Added modulo() function and added it to the operations menu
- `tests/test_app.py` — Added TestModulo class with 5 unit tests, fixed syntax errors

### Files Changed
- `(filename.py)` — (what you changed)
- `(test_filename.py)` — (tests you added)

---

## PR 2 — Details

| Field | Detail |
|---|---|
| **Repository** | (classmate's repo URL) |
| **Branch created** | `feature/your-branch-name` |
| **Issue addressed** | Closes #(issue number) |
| **PR Link** | (paste GitHub PR URL here) |
| **Status** | Merged ✅ |
| **Merged on** | (date) |

### Summary of Changes
(Describe what you changed and why.)

### Files Changed
- `(filename.py)` — (what you changed)

---

## PR 3 — Details

| Field | Detail |
|---|---|
| **Repository** | (classmate's repo URL) |
| **Branch created** | `feature/your-branch-name` |
| **Issue addressed** | Closes #(issue number) |
| **PR Link** | (paste GitHub PR URL here) |
| **Status** | Merged ✅ |
| **Merged on** | (date) |

### Summary of Changes
(Describe what you changed and why.)

### Files Changed
- `(filename.py)` — (what you changed)

---

## How to Update This File

After each PR is submitted:
1. Paste the PR link in the table above
2. Update the status as Pending ⏳
3. When the PR gets merged, change status to Merged ✅ and add the merge date
4. Push the updated file:
```bash
git add MERGED_PRS.md
git commit -m "Update merged PRs tracking"
git push origin main
```