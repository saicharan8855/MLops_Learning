# Day 08 — Revision and Repo Cleanup

Exam week. No new code today — just went back through everything from the past 7 days and wrote a README for the repo. Boring on the surface but honestly useful. Reading your own code a week later tells you a lot about whether you actually understood it.

---

## What I Went Through

### Day 01 — Virtual Environments

Each project gets its own isolated box. Install packages inside it, freeze them to `requirements.txt`, never push the venv folder itself. Someone clones your repo, runs `pip install -r requirements.txt`, and they're set up. That's the whole point.

### Day 02 — Type Hints

Labels on function arguments and return values. `List[float]`, `Dict[str, Any]`, `Optional[str]`. Python ignores them at runtime — they're for humans, not the interpreter. Future you will thank present you for writing them.

### Day 03 — Modules and Packages

A `.py` file is a module. A folder with `__init__.py` inside is a package. Split code by what it does — data loading in one file, prediction logic in another, helpers in a third. The bug I hit: writing `from utils import something` instead of `from iris_package.utils import something`. Always use the full path when importing between files inside a package.

### Day 04 — Error Handling

`try/except` stops code from crashing. `raise` throws errors on purpose when data is wrong. `finally` runs no matter what — cleanup goes there. Custom exception classes like `InvalidFeaturesError` make logs readable. The bug I hit: `except ([TypeError, ValueError])` — square brackets don't work there, just parentheses.

### Day 05 — Logging

Stop using `print`. Logging gives you timestamps, levels, named sources, and file output. Five levels from quiet to loud: DEBUG, INFO, WARNING, ERROR, CRITICAL. Set the level from an environment variable so you can change verbosity without touching code. Every function logs what it's doing — that trail is what saves you at 3am when something breaks in production.

### Day 06 — Config and .env

Never hardcode paths, versions, or settings in Python files. Put them in `.env`, load with `load_dotenv()`, read with `os.getenv("KEY", "default")`. The default value is important — if `.env` is missing the code still runs. Everything that comes out of `.env` is a string, so convert manually: `int()`, `float()`, `.lower() == "true"` for bools.

### Day 07 — Config Class

Instead of calling `os.getenv` in ten different files, call it once inside `load_config()` and return a dataclass. One object, all config, typed fields. Pass it around. Change `.env`, behavior changes — no code touched. `.env.example` goes to GitHub as a template. `.env` never does.

---

## What I Pushed

A README inside `01.Python For Production` summing up all 7 days. Topics, concepts, key takeaways. Anyone landing on the repo knows what's in there without digging through folders.

---

## My View After 7 Days

```
venv        → isolated workspace per project
type hints  → code that explains itself
modules     → one file, one job
errors      → handled, never ignored
logging     → full trail, no print statements
config      → controlled from outside the code
```

FastAPI, Docker, MLflow all come next. Every one of them assumes you already have these habits. Good time to have them locked in.

---

*Day 08 done. Exams ongoing. Full load resumes Day 12.*