# Day 05 — Logging

## What I Did Today

Day 5 was about replacing `print` statements with proper logging. In production nobody uses print — logging gives you timestamps, severity levels, file output, and the ability to silence or amplify output without touching your code.

---

## Why Not print

Simple comparison —

```python
print("prediction done")                          # no context

logger.info("prediction complete: setosa")        # timestamp, level, message
```

The logging version tells you when it happened, how serious it is, and what happened. The print version tells you nothing useful in production.

---

## What I Built

One file — `logging_basics.py` — covering 6 progressively real exercises.

---

## Exercise 1 — Basic logging setup

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.debug("this is a debug message")
logging.info("this is an info message")
logging.warning("this is a warning message")
logging.error("this is an error message")
logging.critical("this is a critical message")
```

`basicConfig` sets up the logger with a level and a format. The format string controls what each log line looks like — here it shows timestamp, level, and message.

---

## Exercise 2 — Logging levels

```python
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.debug("you won't see this")
logging.info("you won't see this either")
logging.warning("you will see this")
logging.error("you will see this")
logging.critical("you will see this")
```

Setting level to `WARNING` silences everything below it. DEBUG and INFO disappear. This is how production apps control noise — in development you set DEBUG, in production you set WARNING or ERROR.

| Level | When to use |
|---|---|
| `DEBUG` | detailed info during development |
| `INFO` | general flow, things working fine |
| `WARNING` | unexpected but not breaking |
| `ERROR` | something broke |
| `CRITICAL` | system going down |

---

## Exercise 3 — Named loggers

```python
logger = logging.getLogger("iris_model")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger.info("model logger started")
logger.debug("loading features")
logger.warning("feature count is low")
logger.error("prediction failed")
```

`getLogger("iris_model")` creates a logger with the name `iris_model`. The `%(name)s` in the format prints that name in every log line. In real projects every module has its own named logger — when something breaks in production you can immediately see which file the log came from.

---

## Exercise 4 — Log to a file

```python
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("iris_model")

logger.info("application started")
logger.debug("loading features")
logger.warning("feature count is low")
logger.error("prediction failed")
```

Two handlers — `FileHandler` writes to `app.log`, `StreamHandler` writes to terminal. Both at the same time. In production logs always go to files so you can check what happened after the fact. The `app.log` file gets auto created when this runs.

---

## Exercise 5 — Logging inside functions

```python
logger = logging.getLogger("iris_pipeline")

def validate_feature(features: List[float]) -> bool:
    logger.debug(f"validating features: {features}")

    if len(features) != 4:
        logger.error(f"invalid feature count: {len(features)}")
        raise ValueError(f"expected 4 features but got {len(features)}")

    logger.info("features are valid")
    return True

def predict(features: List[float]) -> Dict[str, Any]:
    logger.info(f"starting prediction for features: {features}")

    try:
        validate_feature(features)
        label = "setosa" if features[0] < 5.0 else "versicolor"
        logger.info(f"prediction complete: {label}")
        return {"prediction": label, "status": "success"}
    except ValueError as e:
        logger.error(f"prediction failed: {e}")
        return {"prediction": None, "status": "failed", "error": str(e)}

print(predict([5.1, 3.5, 1.4, 0.2]))   # success
print(predict([5.1, 3.5]))              # invalid
```

This is the real pattern. Every function logs what it's doing at the start, logs the result at the end, and logs the error if something breaks. When this runs in production and something goes wrong you have a full trail of what happened step by step.

---

## Exercise 6 — Log level from environment

```python
import os

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper())
)

logger = logging.getLogger("iris_app")

logger.debug("debug only shows if LOG_LEVEL=DEBUG")
logger.warning("something to watch")
```

`os.environ.get("LOG_LEVEL", "INFO")` reads the log level from an environment variable. If it's not set it defaults to INFO. This means you can change how much logging you see without touching any code — just set the environment variable.

```bash
# Windows — see debug logs
set LOG_LEVEL=DEBUG
python logging_basics.py
```

This is exactly how real deployments work. Different log levels for development, staging, and production environments.

---

## One Thing I Noticed

`basicConfig` only works once — the first call sets the config and subsequent calls are ignored. So in a single file with multiple exercises the later `basicConfig` calls don't actually change anything. In a real project you set up logging once at the entry point and every module just calls `getLogger` with its name.

---

## What to Remember

| Concept | What it means |
|---|---|
| `basicConfig` | sets up logging once at startup |
| `getLogger("name")` | creates a named logger for a module |
| `FileHandler` | writes logs to a file |
| `StreamHandler` | writes logs to terminal |
| `LOG_LEVEL` env var | controls verbosity without code changes |
| Log inside functions | gives a full trail of what happened |

---

## Why This Matters in MLOps

When your model is running as an API in production and a prediction fails at 3am you need logs to understand why. Who sent the request, what features came in, where exactly it broke, what error was thrown — all of that comes from logging. Without it you're debugging blind.

---

*Day 05 done. Tomorrow — Config and .env files.*