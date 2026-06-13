# Day 13 — Good Commit Messages and Git Tags

Today was about making the Git history actually readable. Two things — writing commit messages that mean something, and using tags to mark important points in the project timeline.

---

## Why Commit Messages Matter

Your `git log` is the story of your project. If every commit says "fix" or "update" or "changes" that story is unreadable. Six months later you won't know what any of it means.

Compare these two logs —

```
# unreadable
fix
update
changes
asdfgh

# readable
feat: add feature validation logic
fix: correct feature logic validation
docs: add README for day 13
```

The second one tells you exactly what happened at each step without opening a single file.

---

## Conventional Commits Format

This is the industry standard format —

```
<type>: <short description>
```

Types used in real projects —

| Type | When to use |
|---|---|
| `feat` | new feature added |
| `fix` | bug was fixed |
| `docs` | only documentation changed |
| `refactor` | code restructured, no feature change |
| `test` | tests added or updated |
| `chore` | maintenance, dependencies |
| `style` | formatting only |

---

## What I Did — Exercise 1

Practiced writing proper commit messages across three commits —

```bash
git commit -m "feat: add feature validation logic"
git commit -m "fix: correct feature logic validation"
git commit -m "docs: add README for day 13"
```

Then ran `git log --oneline` and the history read like a clean changelog. That's the goal.

---

## Mistake I Made

First attempt at `fix` commit —

```bash
echo print("bug fixed") feature.py
```

Forgot the `>` redirect operator. The text just printed to terminal instead of writing to the file. Nothing changed in `feature.py` so git had nothing to commit —

```
nothing to commit, working tree clean
```

Fixed it with —

```bash
echo print("bug fixed") > feature.py
```

One character makes all the difference in terminal.

---

## Exercise 2 — Git Tags

Tags mark specific commits as important milestones. Like version releases.

### Lightweight tag — just a label

```bash
git tag v0.1
```

No extra info. Just a name pointing to a commit.

### Annotated tag — full details

```bash
git tag -a v0.2 -m "iris model training complete"
```

Has your name, date, time, and message stored with it. Always use `-a` for real releases.

Running `git show v0.2` showed everything —

```
tag v0.2
Tagger: saicharan8855
Date: Sat Jun 13 14:39:06 2026

iris model training complete
```

Compared to `git show v0.1` on a lightweight tag — it just shows the commit, no tagger info, no message.

### Tagging a past commit

```bash
git tag -a v0.0 016ef83 -m "project start"
```

Picked the hash `016ef83` from `git log --oneline` and put a tag on it. You can go back and label any point in history. Useful when you forgot to tag something when you were working on it.

---

## Exercise 3 — Delete and Move a Tag

```bash
git tag -d v0.1          # deleted it
git tag                  # confirmed it's gone
git tag v0.1 f27758e     # recreated on a different commit
git tag                  # v0.1 is back
```

Tags can be moved, deleted, recreated. They're not permanent.

---

## Pushing Tags to GitHub

```bash
# wrong — typo
git push --origin tags

# correct
git push origin --tags
```

`origin` is the remote name, not an option. `--tags` is the option. Tags don't get pushed with a regular `git push` — you have to push them separately with `--tags`.

After pushing —

```
* [new tag] v0.0 -> v0.0
* [new tag] v0.1 -> v0.1
* [new tag] v0.2 -> v0.2
```

All three tags now visible on GitHub under the releases section.

---

## The Final Log

```
320532d (HEAD, tag: v0.2) docs: add README for day 13
8da40f4 fix: correct feature logic validation
f27758e (tag: v0.1) feat: add feature validation logic
e4c323b delete feature.py
016ef83 (tag: v0.0) feat: add feature one to iris pipeline
```

Three tags spread across the history — v0.0 at the start, v0.1 at the first working feature, v0.2 at the current HEAD. Clean, versioned, readable.

---

## What to Remember

| Command | What it does |
|---|---|
| `git tag v0.1` | lightweight tag on current commit |
| `git tag -a v0.1 -m "msg"` | annotated tag with message |
| `git tag -a v0.0 <hash> -m "msg"` | tag a past commit |
| `git tag` | list all tags |
| `git show v0.2` | show tag details |
| `git tag -d v0.1` | delete a tag locally |
| `git push origin --tags` | push all tags to GitHub |

---

## Typos Made Today

```bash
got log --oneline -3     # 'got' not recognized
git status'              # extra quote mark
git push --origin tags   # --origin is wrong, should be origin --tags
```

Same pattern every time — one wrong character, command fails. Terminal doesn't guess what you meant.

---

*Day 13 done. Git and GitHub topic wrapping up. Tomorrow — Pull Requests.*