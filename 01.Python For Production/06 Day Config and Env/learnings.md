# Day 06 — Config and .env Files

## What I Did Today

Day 6 was a lighter day — exams coming up. Covered the basics of config management. The idea is simple — never hardcode values like model paths, log levels, or app names directly in your code. Store them in a `.env` file and read them at runtime.

---

## What is a .env File

A `.env` file is a plain text file that stores configuration values as key-value pairs.

```
APP_NAME=Iris MLOps App
LOG_LEVEL=DEBUG
MODEL_PATH=models/iris_model.pkl
MODEL_VERSION=1.0
DEBUG_MODE=True
MAX_BATCH_SIZE=32
```

These values are specific to your machine and your environment. Someone else running the same code might have different paths, different log levels, different settings. The `.env` file handles that cleanly.

**Most important rule — never push `.env` to GitHub.** It can contain API keys, passwords, secret tokens. Add it to `.gitignore` always.

---

## What I Built

### .env file

```
APP_NAME=Iris MLOps App
LOG_LEVEL=DEBUG
MODEL_PATH=models/iris_model.pkl
MODEL_VERSION=1.0
DEBUG_MODE=True
MAX_BATCH_SIZE=32
```

### config.py

```python
from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Default App")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.pkl")
MODEL_VERSION = float(os.getenv("MODEL_VERSION", "1.0"))
DEBUG_MODE = os.getenv("DEBUG_MODE", False).lower() == "true"
MAX_BATCH_SIZE = int(os.getenv("MAX_BATCH_SIZE", "16"))

print(f"App: {APP_NAME}")
print(f"Log Level: {LOG_LEVEL}")
print(f"Model Path: {MODEL_PATH}")
print(f"Model Version: {MODEL_VERSION}")
print(f"Max Batch Size: {MAX_BATCH_SIZE}")
```

`load_dotenv()` reads the `.env` file and loads everything into the environment. After that `os.getenv` picks up each value by key.

---

## How os.getenv Works

```python
os.getenv("APP_NAME", "Default App")
```

Two arguments — the key to look for, and a default value if the key is not found. So if `.env` is missing or the key is not in it the code still works — it falls back to the default.

This is important. In production the `.env` file might not exist — environment variables are set directly on the server instead. The default values make sure nothing crashes.

---

## Type Conversion

Everything from `.env` comes in as a string. So you need to convert manually —

```python
MODEL_VERSION = float(os.getenv("MODEL_VERSION", "1.0"))   # string to float
MAX_BATCH_SIZE = int(os.getenv("MAX_BATCH_SIZE", "16"))    # string to int
DEBUG_MODE = os.getenv("DEBUG_MODE", False).lower() == "true"  # string to bool
```

For booleans especially — `"True"` as a string is not the same as `True` as a boolean. The `.lower() == "true"` pattern handles that correctly.

---

## What to Remember

| Concept | What it means |
|---|---|
| `.env` | stores config values locally |
| `load_dotenv()` | loads `.env` into environment |
| `os.getenv("KEY", "default")` | reads value with fallback |
| Type conversion | everything from .env is a string |
| Never push `.env` | add to .gitignore always |

---

## Why This Matters in MLOps

Your model path on your laptop is different from the model path on a server. Your log level in development is DEBUG, in production it's WARNING. Your batch size depends on how much memory the server has. Hardcoding any of these means changing code every time you move environments. With `.env` you just swap the file and the code stays exactly the same.

---

*Day 06 done — light day. Back to full load on Day 12. Good luck with exams.*