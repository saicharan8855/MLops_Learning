# Day 01 — Python for Production: Virtual Environments

## What I Did Today

Started the MLOps grind. Day 1 was all about setting up a proper Python environment before writing any real code. Sounds boring but this is what separates beginner scripts from production-ready projects.

---

## The Problem I Understood First

Say you have two projects on your laptop.

- Project A needs `numpy 1.0`
- Project B needs `numpy 2.0`

If you install everything globally, one of them breaks. There's no clean way to manage which version belongs to which project. This is the exact problem virtual environments solve.

---

## What is a Virtual Environment

A virtual env is an isolated box for your project. It has its own Python, its own packages, its own versions. Whatever you install inside it stays inside it. Your other projects don't see it. Your global Python doesn't get polluted.

---

## What I Actually Did

### Step 1 — Created the project folder and set up venv

```bash
mkdir "01.Python For Production"
cd "01.Python For Production"
python -m venv venv
venv\Scripts\activate
```

After activation the terminal shows `(venv)` at the start. That means I'm inside the box now.

### Step 2 — Installed packages and saved them

```bash
pip install requests numpy pandas
pip list
pip freeze > requirements.txt
```

`pip freeze` captures every installed package with its exact version and dumps it into `requirements.txt`. This file is how any developer (or future me) can recreate this exact environment.

### Step 3 — Simulated a fresh clone

```bash
deactivate
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip list
```

Deleted the venv folder and rebuilt it from `requirements.txt`. This is exactly what happens in real teams — someone clones the repo and runs `pip install -r requirements.txt`. The environment comes back exactly as it was.

### Step 4 — Wrote a test script

```python
# test_env.py
import requests
import numpy as np
import pandas as pd

print("requests version:", requests.__version__)
print("numpy version:", np.__version__)
print("pandas version:", pd.__version__)
print("Environment is working correctly!")
```

Ran it inside venv — worked. Deactivated and ran it again — threw an import error. That error is the whole point. It showed me exactly why venv exists.

### Step 5 — Fixed .gitignore

```bash
echo venv/ >> .gitignore
echo __pycache__/ >> .gitignore
```

Never push the venv folder to GitHub. It's huge, machine-specific, and completely unnecessary. Anyone can recreate it from `requirements.txt`.

---

## Git Issue I Ran Into

When I ran `git status` from inside the `01.Python For Production` folder it showed `./` as untracked. Confusing.

The reason — git is initialized in the parent folder `MLops Learning Grind`. Running git commands from inside a subfolder makes git see the whole subfolder as one untracked item.

Fix was simple — always run git commands from the root of the repo.

```bash
cd "C:\Users\sai charan\OneDrive\Desktop\MLops Learning Grind"
git status
git add .
git commit -m "day01: venv setup and test script"
git push
```

---

## What I'll Carry Forward

Every single project from this day on starts with these 3 steps —

1. Create venv
2. Activate it
3. Install packages, freeze to requirements.txt

No exceptions.

---

## Key Commands to Remember

| Command | What it does |
|---|---|
| `python -m venv venv` | creates the virtual environment |
| `venv\Scripts\activate` | activates it on Windows |
| `deactivate` | exits the environment |
| `pip freeze > requirements.txt` | saves all packages |
| `pip install -r requirements.txt` | recreates environment from file |

---

*Day 01 done. Tomorrow — functions and type hints.*