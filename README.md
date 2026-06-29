# MLOps learning journey

# 01. Python For Production — Summary

## What This Section Covers
7 days of Python fundamentals needed before writing any MLOps code.

## Days
| Day | Topic | Key Concepts |
|---|---|---|
| 01 | Virtual Environments | venv, pip, requirements.txt |
| 02 | Type Hints | int, str, List, Dict, Optional |
| 03 | Modules + Packages | __init__.py, imports, structure |
| 04 | Error Handling | try/except, raise, custom exceptions |
| 05 | Logging | levels, handlers, named loggers |
| 06 | Config + .env | load_dotenv, os.getenv |
| 07 | Config Class | dataclass, load_config() |

## Key Takeaways
- Always use virtual environments
- Type hints make code self documenting
- Split code into modules, not one big file
- Never crash — handle errors gracefully
- Never print — use logging
- Never hardcode — use .env and config

---

# 02. Git and GitHub — Summary

## What This Section Covers
4 days of Git and GitHub workflow beyond the basics — going past add, commit, push, pull into branching, undoing mistakes, clean history, and real team collaboration through Pull Requests.

## Days
| Day | Topic | Key Concepts |
|---|---|---|
| 11 | Git Basics Deep Dive | git diff, git status, branching (create/switch/merge/delete), .gitignore patterns |
| 12 | Restore and Reset | git restore, git restore --staged, git reset --soft, git reset --hard, git log variations |
| 13 | Commit Messages and Tags | Conventional commits (feat/fix/docs), lightweight vs annotated tags, tagging past commits |
| 14 | Pull Requests | Branch → push → PR → review → merge flow, resolving merge conflicts |

## Key Takeaways
- Never work directly on main — always branch first
- `git diff` before committing to see exactly what changed
- `git restore` undoes unstaged changes; `git reset --soft` undoes commits but keeps files; `git reset --hard` deletes everything — use with care
- Write commit messages that explain *what* and *why*, not just "fix" or "update"
- Tag meaningful checkpoints (`v0.1`, `v0.2`) so the project history reads like a timeline
- Every change goes through a Pull Request, even solo — it's a checkpoint to review before merging
- Merge conflicts happen when two branches edit the same line — resolve manually, keep what's correct, commit

## Common Mistakes Made
- Typos in branch names causing "not something we can merge" errors
- Forgetting to `git pull` after merging a PR on GitHub, leaving local out of sync
- `--origin` vs `origin --tags` — remote name and flag order matters
- Square brackets instead of parentheses in `except` (carried over Python habit, not Git — but same "syntax precision matters" lesson)

## What's Next
Topic 03 — Linux and Terminal *(already completed)*
Topic 04 — HTTP and APIs

---

# 03. Linux and Terminal - Summary

## Days Covered

| Day | Topic |
|---|---|
| 15 | Navigation, files, search, pipes, environment variables, permissions, processes |
| 16 | Shell scripting basics and `curl` |
| 17 | Practice project: log analyzer |
| 18 | Bash functions, exit codes, arrays |
| 19 | Real projects: project checker, strings, user input, while loops |
| 20 | Final review and wrap-up |

## Key Commands Mastered

- Navigation: `pwd`, `cd`, `ls`
- Files: `touch`, `cat`, `cp`, `mv`, `rm`, `mkdir`
- Reading: `head`, `tail`, `less`, `wc`
- Searching: `grep`, `grep -E`, `find`
- Piping and redirection: `|`, `>`, `>>`
- Scripting: functions, `if/else`, `for`, `while`, arrays
- Environment: `export`, `$VAR`, `$?`
- Permissions: `chmod +x`

## Biggest Lessons

- A frozen terminal usually means a command is waiting on standard input.
- `grep` needs a file argument or another input source, otherwise it can appear to hang.
- Bash test brackets like `[ ]` need spaces around them or the command breaks.
- `$?` only reflects the exit status of the command that ran immediately before it.
- Always quote variables in conditions to avoid unexpected errors.

--- 

# 04. HTTP and APIs — Summary

## Days Covered
| Day | Topic |
|---|---|
| 21 | Request/response basics, status codes, requests library |
| 22 | POST, PUT, DELETE, idempotency |
| 23 | API authentication — Bearer tokens, API keys, .env |
| 24 | Timeouts, retries, exponential backoff, error handling |
| 25 | JSON deep dive, REST design, final combined client |

## Key Concepts Mastered
- Request = method + URL + headers + body
- Response = status code + headers + body
- Status code families: 2xx success, 4xx client error, 5xx server error
- POST creates (not idempotent), PUT/DELETE are idempotent
- Bearer tokens via Authorization header, secrets via .env
- timeout= prevents hanging forever, retries need backoff
- JSON: objects for single things, arrays for lists, nested structure for real responses
- REST: URLs are nouns (resources), HTTP methods are verbs (actions)

## Biggest Lessons
- External APIs fail in real, unpredictable ways (httpbin taught this all week)
- Never trust response.json() without checking status first
- Wrap every API call in try/except with specific exception  types
- Never hardcode secrets — always .env + .gitignore






