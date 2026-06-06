# CONTRIBUTIONS.md — Assignment 15 Submission
## CampusFind: Smart Campus Lost & Found System

---

## My Repository
🔗 https://github.com/MissDidiza/campusfind1

---

## Assignment 15 Files

| File | Description |
|---|---|
| [CONTRIBUTION_PLAN.md](./CONTRIBUTION_PLAN.md) | Strategy and plan for contributing to 3+ classmate projects |
| [MERGED_PRS.md](./MERGED_PRS.md) | Links to all submitted and merged pull requests |
| [REFLECTION_A15.md](./REFLECTION_A15.md) | Reflection on collaboration challenges and lessons learned |

---

## Pull Requests Submitted

| # | Project | PR Link | Status |
|---|---|---|---|
| 1 | (classmate repo name) | (PR URL) | Merged ✅ |
| 2 | (classmate repo name) | (PR URL) | Merged ✅ |
| 3 | (classmate repo name) | (PR URL) | Merged ✅ |

*(Update this table as PRs are submitted and merged)*

---

## How I Contributed

### Step-by-Step PR Workflow I Followed

For every contribution I made to a classmate's repository, I followed this exact workflow:

**Step 1 — Find an issue**
```
Go to classmate's repo → Issues tab → Look for good-first-issue label
```

**Step 2 — Comment on the issue**
```
Comment: "Hi! I would like to work on this issue. I plan to [describe approach]."
```

**Step 3 — Fork the repository**
```
Click Fork button on their repo → Create fork under MissDidiza
```

**Step 4 — Clone the fork**
```bash
git clone https://github.com/MissDidiza/their-project-name.git
cd their-project-name
```

**Step 5 — Install dependencies and run tests**
```bash
pip install -r requirements.txt
python -m pytest tests/ -v
```

**Step 6 — Create a feature branch**
```bash
git checkout -b fix/description-of-change
```

**Step 7 — Make changes, write tests, verify CI**
```bash
# make changes
python -m pytest tests/ -v  # make sure all tests still pass
```

**Step 8 — Commit and push**
```bash
git add .
git commit -m "Fix: description of what was changed (Closes #issue_number)"
git push origin fix/description-of-change
```

**Step 9 — Open Pull Request**
```
Go to their repo on GitHub → Compare & pull request
Fill in: title, description, link to issue
Submit PR
```

**Step 10 — Respond to feedback**
```
Check PR daily
Make requested changes on same branch
Push again — PR updates automatically
```