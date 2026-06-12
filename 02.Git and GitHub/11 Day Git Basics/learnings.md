# Day 11 — Git and GitHub Workflow

Last half load day. Exams done. Today covered three core Git concepts that go beyond the basic add, commit, push routine — diff, branching, and gitignore patterns.

---

## Exercise 1 — git diff and git status

Created a file, staged it, then edited it again before committing. Then ran two different diff commands to see what changed.

```bash
echo print("hello") > test.py
git add test.py
echo print("hello world") > test.py

git diff test.py        # shows unstaged changes
git diff --staged       # shows staged changes
```

Output of `git diff test.py` —
```
-print("hello")
+print("hello world")
```

Red line with `-` is what was there before. Green line with `+` is what's there now. This is how you review changes before committing — see exactly what you're about to save.

`git diff --staged` shows what's already staged and ready to commit. `git diff` without `--staged` shows changes not yet staged. Two different views of two different states.

---

## Exercise 2 — Branching

This is the most important thing from today.

```bash
git checkout -b feature/day11-practice
```

`-b` creates the branch and switches to it in one command. Without `-b` it just switches to an existing branch.

Made a commit on the feature branch —

```bash
echo print("on feature branch test file") > branch_test.py
git add .
git commit -m "test: add branch test file"
```

Switched back to main —

```bash
git checkout main
```

`branch_test.py` was gone. The folder showed zero files. That's branching doing exactly what it should — the feature branch has its own state, main has its own state. They don't affect each other.

Merged the feature branch into main —

```bash
git merge feature/day11-practice
```

Output said `Fast-forward` — meaning main had no new commits since the branch was created, so Git just moved main forward to the branch's commit. No conflicts.

`branch_test.py` came back. Deleted the branch since it's merged —

```bash
git branch -d feature/day11-practice
```

### Why branching matters

```
main                  → stable, always working
feature/something     → experimental, safe to break
```

In real teams nobody works directly on main. Every feature, every fix, every experiment gets its own branch. When it's ready and reviewed it gets merged. Main stays clean and deployable at all times.

---

## Exercise 3 — .gitignore Patterns

Created a `.gitignore` with these patterns —

```
*.pkl
*.log
temp/
secrets.txt
```

Then created `secrets.txt` and a `temp/` folder with a file inside. Ran `git status` —

```
Untracked files:
    .gitignore
    secrets.txt
```

Wait — `secrets.txt` showed up even though it's in `.gitignore`. That's because the `.gitignore` file itself wasn't committed yet when I ran status. After committing the `.gitignore`, any new `secrets.txt` would be ignored properly.

`temp/` folder didn't show up at all — correctly ignored.

### Pattern rules

| Pattern | What it ignores |
|---|---|
| `*.pkl` | all pkl files anywhere |
| `*.log` | all log files anywhere |
| `temp/` | the entire temp folder |
| `secrets.txt` | that specific file |

---

## Typo I Made

```bash
got commit -m "test: add branch test file"
# 'got' is not recognized
```

Typed `got` instead of `git`. Simple typo but a good reminder — terminal has zero tolerance for spelling mistakes.

---

## What to Remember

| Command | What it does |
|---|---|
| `git diff file` | shows unstaged changes |
| `git diff --staged` | shows staged changes |
| `git checkout -b branch-name` | create and switch to new branch |
| `git checkout main` | switch back to main |
| `git merge branch-name` | merge branch into current branch |
| `git branch -d branch-name` | delete merged branch |
| `.gitignore` | tells git which files to never track |

---

## The Bigger Picture

Branching is what makes collaborative development possible. It's also what makes solo development safe — you can experiment freely on a branch knowing main is always stable. Every MLOps project from here uses this pattern — a main branch that's always deployable and feature branches for every change.

---

*Day 11 done. Exams over. Full load resumes tomorrow — Day 12.*