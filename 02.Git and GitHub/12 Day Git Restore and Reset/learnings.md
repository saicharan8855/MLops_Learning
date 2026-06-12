# Day 12 — Git Restore and Reset

Full load resumes today. This is the most practical Git topic so far — undoing mistakes. Every developer uses these commands regularly. Understanding the difference between restore and reset is what separates someone who panics when something breaks from someone who fixes it in 10 seconds.

---

## The Three States of a File in Git

Before anything else — understanding these three states makes everything click.

```
Working Directory → Staging Area → Repository
(you edit here)     (git add)       (git commit)
```

- `git restore` — undoes changes in the working directory
- `git restore --staged` — moves a file back from staging to working directory
- `git reset` — moves HEAD backward to a previous commit

---

## Exercise 1 — git restore (undo unstaged changes)

Created `mistake.py`, committed it, then broke it —

```bash
echo print("oops i broke it") > mistake.py
git diff mistake.py
```

Diff showed exactly what changed — original line in red, broken line in green. Then restored it —

```bash
git restore mistake.py
type mistake.py
# output: print("original")
```

File went back to exactly what it was at the last commit. The bad change is completely gone. This is the safest undo — it only touches the working directory, nothing else.

---

## Exercise 2 — git restore --staged (unstage a file)

Made a change and staged it with `git add` — then realized I didn't want to commit it yet —

```bash
git restore --staged mistake.py
git status
```

After `--staged` the file moved back from staging area to working directory. The change was still there in the file — `type mistake.py` showed `print("stages change")` was still there. Just unstaged, not deleted.

**Key difference —**
- `git restore mistake.py` — throws away the change completely
- `git restore --staged mistake.py` — keeps the change but removes it from staging

---

## Exercise 3 — git reset --soft (undo commit, keep files)

Made two commits then undid the last one —

```bash
git log --oneline
# 73b05b2 commit two
# ae3fabf commit one

git reset --soft HEAD~1

git log --oneline
# ae3fabf commit one   ← commit two is gone
```

`HEAD~1` means one commit before the current HEAD. After the reset `commit two` disappeared from the log. But `file2.py` was still there and `git status` showed it as staged — ready to commit again whenever I want.

`--soft` is a safe undo. It removes the commit but keeps everything you did. Nothing is lost.

---

## Exercise 4 — git reset --hard (nuclear option)

Made a bad commit then completely wiped it —

```bash
git log --oneline
# 5055b32 bad commit
# ae3fabf commit one

git reset --hard HEAD~1

git log --oneline
# ae3fabf commit one   ← bad commit gone

dir
# bad.py is gone too
```

`--hard` removes the commit AND deletes the files. `bad.py` and `file2.py` were both gone after running it. No recovery — they're just gone.

**Use `--hard` carefully. There's no undo for this.**

---

## The Difference — Soft vs Hard

| Command | Removes commit | Keeps files |
|---|---|---|
| `git reset --soft HEAD~1` | ✅ yes | ✅ yes, staged |
| `git reset --hard HEAD~1` | ✅ yes | ❌ no, deleted |

Default rule — always try `--soft` first. Only use `--hard` when you're absolutely sure you want to throw everything away.

---

## Exercise 5 — git log properly

Four ways to read the log —

```bash
git log                        # full details, author, date, message
git log --oneline              # one line per commit, hash + message
git log --oneline --graph --all  # visualizes branches
git log --oneline -3           # only last 3 commits
```

`--graph --all` shows a visual tree of branches. Right now the repo is linear so it shows a straight line of `*` characters. Once there are multiple branches merging it shows a proper tree structure.

---

## Typos I Made Today

```bash
git ad .       # 'ad' is not a git command
git add.       # missing space — 'add.' is not a git command
git status'    # extra quote mark at the end
```

Terminal has zero tolerance. One wrong character and the command fails. The habit to build — type slowly, read before pressing Enter.

---

## What to Remember

| Command | What it does |
|---|---|
| `git restore file` | undo unstaged changes, file goes back to last commit |
| `git restore --staged file` | unstage a file, change is kept |
| `git reset --soft HEAD~1` | undo last commit, keep files staged |
| `git reset --hard HEAD~1` | undo last commit, delete files permanently |
| `git log --oneline` | clean one-line commit history |
| `git log --oneline -3` | last 3 commits only |
| `HEAD~1` | one commit before current HEAD |

---

## Why This Matters

In production you will make bad commits. You will stage the wrong file. You will push something you didn't mean to. These commands are how you fix that cleanly without panicking. The difference between `--soft` and `--hard` is the difference between recovering your work and losing it permanently.

---

*Day 12 done. Full load resumed. Exams over.*