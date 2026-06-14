# Day 14 — Pull Requests and Merge Conflicts

Today was the most realistic Git day so far. Pull Requests are how real teams work — nobody merges directly to main. Everything goes through a PR so changes can be reviewed before they hit the main branch. Also hit a real merge conflict and fixed it manually.

---

## What is a Pull Request

A Pull Request is a proposal to merge your branch into main. You push your branch to GitHub, open a PR, someone reviews it, and then it gets merged. In solo projects you review your own PRs — still a good habit because the PR shows you exactly what changed before you commit to merging it.

---

## Exercise 1 — Create a Branch and Push to GitHub

```bash
git checkout -b feature/add-predict-script
echo print("predict function here") > predict.py
git add .
git commit -m "feat: add feature script"
git push origin feature/add-predict-script
```

After pushing, GitHub immediately showed a banner —

```
remote: Create a pull request for 'feature/add-predict-script' on GitHub by visiting:
remote: https://github.com/saicharan8855/MLops_Learning/pull/new/feature/add-predict-script
```

GitHub detected the new branch and gave a direct link to open a PR. That's the normal flow — push branch, GitHub prompts you to open PR.

---

## Exercise 2 — Opened the PR on GitHub

On GitHub clicked "Compare and pull request", added a title and description, then clicked "Create pull request". On the PR page used the "Files changed" tab to see exactly what `predict.py` looked like before and after. Then merged it.

---

## Exercise 3 — Pulled the Merged Changes Locally

After merging on GitHub, local main didn't know about it yet —

```bash
git checkout main
git pull origin main
```

Output showed —

```
Fast-forward
 predict.py | 1 +
 1 file changed, 1 insertion(+)
```

`predict.py` appeared in the local folder after pulling. The log showed the merge commit —

```
9e333ed Merge pull request #1 from saicharan8855/feature/add-predict-script
```

**Important habit** — always `git pull` after merging a PR on GitHub. Your local and remote get out of sync the moment someone merges on GitHub.

---

## Exercise 4 — Simulated a Merge Conflict

Created a new branch and edited `predict.py` there —

```bash
git checkout -b feature/update-preict
echo print("updated predict function") > predict.py
git commit -m "feat: update predict function"
```

Then switched back to main and edited the same file —

```bash
git checkout main
echo print("main branch edit") > predict.py
git commit -m "fix: edit prediction on main"
```

Both branches now had different versions of the same line. Tried to merge —

```bash
git merge feature/update-preict
```

Output —

```
CONFLICT (content): Merge conflict in predict.py
Automatic merge failed; fix conflicts and then commit the result.
```

Git cannot decide which version to keep when two branches change the same line. It stops and asks you to decide manually.

---

## Fixing the Conflict

Opened `predict.py` in VS Code. Saw this —

```
<<<<<<< HEAD
print("main branch edit")
=======
print("updated predict function")
>>>>>>> feature/update-preict
```

- `<<<<<<< HEAD` to `=======` — what's on main (current branch)
- `=======` to `>>>>>>>` — what's coming in from the feature branch

Deleted the conflict markers and kept the version I wanted —

```python
print("updated predict function")
```

Then finished the merge —

```bash
git add predict.py
git commit -m "fix: resolve merge conflicts in predict.py"
```

Log after resolving —

```
fd3eeb5 fix: resolve merge conflicts in predict.py
475c7cf fix: edit prediction on main
102340f feat: update predict function
9e333ed Merge pull request #1
```

---

## Typos Made Today

```bash
git ckeckout -b feature/add-predict-script   # ckeckout not recognized
git commmit -m "feat: update predict function" # commmit not recognized
git merge feature/update-predict              # wrong name — branch was update-preict
```

The branch name typo was the most interesting one. Created `feature/update-preict` by accident. Git doesn't care about spelling — whatever you type becomes the branch name. Always run `git branch` to verify the exact name before merging.

---

## What to Remember

| Concept | What it means |
|---|---|
| `git push origin branch-name` | push branch to GitHub |
| Pull Request | propose changes before merging to main |
| Files changed tab | see exactly what the PR changes |
| `git pull origin main` | sync local after merging on GitHub |
| Merge conflict | two branches edited the same line |
| `<<<<<<< HEAD` | current branch version |
| `>>>>>>> branch` | incoming branch version |
| Fix conflict | delete markers, keep what you want, commit |

---

## Why PRs Matter in MLOps

In production you never push directly to main. A broken model serving endpoint affects real users. PRs give you a checkpoint — review the diff, run tests, approve — before anything hits the deployed branch. GitHub Actions CI (coming later in this grind) runs automatically on every PR so tests pass before merge. That's the full safety net.

---

*Day 14 done. Git and GitHub topic complete. Tomorrow — Linux and Terminal basics.*