# Day 07 — Config Class with Dataclass

## What I Did Today

Day 7 finished off the config topic. Yesterday was reading values from `.env` using `os.getenv`. Today was about organizing those values into a clean config object using a dataclass — and then actually using that config inside a real pipeline.

---

## The Problem with Scattered os.getenv Calls

If you call `os.getenv` in every file that needs config, you end up with this mess —

```python
# in model.py
model_path = os.getenv("MODEL_PATH")

# in api.py
log_level = os.getenv("LOG_LEVEL")

# in pipeline.py
batch_size = int(os.getenv("MAX_BATCH_SIZE", 32))
```

Same values, read in 5 different places. If you rename a key in `.env` you have to hunt down every file. Config class solves this — read once, use everywhere.

---

## What is a Dataclass

A dataclass is a clean way to create a class that just holds data. You don't need `__init__`, no boilerplate — just declare the fields and their types.

```python
from dataclasses import dataclass

@dataclass
class AppConfig:
    app_name: str
    log_level: str
    model_path: str
    model_version: float
    debug_mode: bool
    max_batch_size: int
```

That's it. Python auto generates `__init__`, `__repr__`, and `__eq__` for you. When you print a dataclass object it shows all fields cleanly — very useful for debugging.

---

## What I Built

### config.py

```python
from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class AppConfig:
    app_name: str
    log_level: str
    model_path: str
    model_version: float
    debug_mode: bool
    max_batch_size: int

def load_config() -> AppConfig:
    return AppConfig(
        app_name=os.getenv("APP_NAME", "Default App"),
        log_level=os.getenv("LOG_LEVEL"),
        model_path=os.getenv("MODEL_PATH"),
        model_version=float(os.getenv("MODEL_VERSION", 1.0)),
        debug_mode=os.getenv("DEBUG_MODE", "False").lower() == "true",
        max_batch_size=int(os.getenv("MAX_BATCH", 32))
    )

config = load_config()
print(config)
print(f"App name: {config.app_name}")
print(f"Debug mode: {config.debug_mode}")
print(f"Model version: {config.model_version}")
```

`load_config()` reads all values from `.env` once and returns a single typed object. Every part of the app that needs config just calls `load_config()` and gets everything in one place.

---

### main.py — config driving the pipeline

```python
import logging
from typing import List, Dict, Any
from config import load_config

config = load_config()

logging.basicConfig(
    level=getattr(logging, config.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(config.app_name)

def predict(features: List[float]) -> Dict[str, Any]:
    logger.info(f"Predicting for features: {features}")

    if len(features) != 4:
        logger.error(f"Invalid features: {len(features)}")
        return {"prediction": None, "status": "failed"}

    label = "setosa" if features[0] < 5.5 else "versicolor"
    logger.info(f"prediction: {label}")

    return {
        "prediction": label,
        "model_version": config.model_version,
        "model_path": config.model_path,
        "status": "success"
    }

print(predict([5.1, 3.5, 1.4, 0.2]))
print(predict([6.0, 3.0, 4.8, 1.8]))
```

Notice what's happening here — logging level comes from config, logger name comes from config, model version in the response comes from config. Change one value in `.env` and the whole app behavior changes. No code touched.

---

## The .env.example File

```
APP_NAME=your_app_name
LOG_LEVEL=INFO
MODEL_PATH=models/iris_model.pkl
MODEL_VERSION=1.0
DEBUG_MODE=False
MAX_BATCH_SIZE=32
```

This file goes to GitHub. The real `.env` never does. Anyone cloning the repo sees `.env.example`, copies it, fills in their own values and they're set up. It's the safe template.

---

## Exercise 4 — Changing behavior without touching code

Changed `LOG_LEVEL=WARNING` in `.env` and ran `main.py` again. All DEBUG and INFO logs disappeared. Changed it back to `DEBUG` and they came back.

Same code. Different behavior. Just by editing one line in a text file. This is exactly how production deployments work — dev environment has `DEBUG`, production has `WARNING` or `ERROR`.

---

## What to Remember

| Concept | What it means |
|---|---|
| `@dataclass` | auto generates init and repr for a class |
| `load_config()` | reads all env vars once, returns typed object |
| `config.log_level` | access config values like object attributes |
| `.env.example` | safe template pushed to GitHub |
| Change `.env` not code | behavior changes without touching Python files |

---

## Two Days, One Topic

Day 06 covered reading raw values with `os.getenv`. Day 07 wrapped those values into a proper config class. Together they form the complete config pattern used in real MLOps projects — `.env` for values, `load_dotenv` to load them, dataclass to organize them, one import to use them everywhere.

---

*Day 07 done. Back to full load on Day 12. Go crush those exams.*