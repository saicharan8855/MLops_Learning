# Day 04 — Error Handling

## What I Did Today

Day 4 was about making code that doesn't crash. In production, errors are not surprises — they are expected. Good code handles them cleanly instead of blowing up with a traceback.

---

## What I Built

One file — `error_handling.py` — with 5 progressively harder exercises covering every type of error handling you'll use in real projects.

---

## Exercise 1 — Basic try/except

```python
def divide(a: int, b: int) -> float:
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("error: cannot divide by zero")
        return 0.0

print(divide(10, 5))   # 2.0
print(divide(10, 0))   # caught — returns 0.0
```

`try` runs the code. If something goes wrong `except` catches it and handles it. The program keeps running instead of crashing.

---

## Exercise 2 — Multiple except blocks

```python
def parse_feature(feature: str) -> float:
    try:
        value = float(feature)
        return value
    except ValueError:
        print(f"error: cannot convert {feature} to float")
        return 0.0
    except TypeError:
        print(f"error: feature must be a string or integer, got {type(feature)}")
        return 0.0

print(parse_feature("3.14"))   # works
print(parse_feature("abc"))    # ValueError caught
print(parse_feature(None))     # TypeError caught
```

Different errors need different handling. `ValueError` means the value is wrong. `TypeError` means the type itself is wrong. Each gets its own except block.

---

## Exercise 3 — Raising your own errors

```python
def validate_features(features: List[float]) -> bool:
    if not isinstance(features, list):
        raise TypeError(f"features must be a list, got {type(features).__name__}")
    
    if len(features) != 4:
        raise ValueError(f"features must contain 4 elements, got {len(features)}")
    
    if not all(isinstance(f, (int, float)) for f in features):
        raise TypeError("All features must be numeric")
    return True
```

`raise` throws an error on purpose. This is how you tell the caller that they passed bad data. Instead of silently returning wrong results the function loudly complains.

One mistake I made here — wrote `except ([TypeError, ValueError])` with square brackets. Python doesn't accept a list in except. Correct way is just parentheses —

```python
# wrong
except ([TypeError, ValueError]) as e:

# correct
except (TypeError, ValueError) as e:
```

---

## Exercise 4 — finally block

```python
def load_file(path: str) -> str:
    file = None
    try:
        file = open(path, "r")
        content = file.read()
        return content
    except FileNotFoundError:
        print(f"error: file {path} not found")
        return ""
    finally:
        if file:
            file.close()
            print(f"closed file {path}")
```

`finally` always runs — whether the try succeeded or the except caught an error. It's used for cleanup — closing files, closing database connections, releasing resources. You never want to leave a file open even if an error happened.

---

## Exercise 5 — Custom exception classes

```python
class InvalidFeaturesError(Exception):
    "raised when iris features are invalid"
    pass

class ModelNotFoundError(Exception):
    "raised when a model file is not found"
    pass

def predict(features: List[float]) -> str:
    if len(features) != 4:
        raise InvalidFeaturesError(
            f"features must contain 4 elements, got {len(features)}"
        )
    return "setosa"

def load_model(path: str) -> str:
    import os
    if not os.path.exists(path):
        raise ModelNotFoundError(f"model file {path} not found")
    return "model loaded"
```

Custom exceptions are just classes that inherit from `Exception`. They make your errors meaningful. Instead of seeing a generic `ValueError` in your logs you see `InvalidFeaturesError` and immediately know what broke and where.

In real MLOps projects every major component has its own exception class — data errors, model errors, config errors. Makes debugging production issues much faster.

---

## The Mistake I Fixed Today

```python
# wrote this — wrong
except ([TypeError, ValueError]) as e:

# fixed to this — correct
except (TypeError, ValueError) as e:
```

Square brackets create a list. `except` doesn't accept a list — it only accepts exception classes directly, optionally grouped in parentheses.

---

## What to Remember

| Concept | What it means |
|---|---|
| `try/except` | run code, catch if it fails |
| `except ValueError` | catch one specific error |
| `except (TypeError, ValueError)` | catch multiple errors |
| `raise` | throw an error on purpose |
| `finally` | always runs, used for cleanup |
| Custom exception | your own error class for clarity |

---

## Why This Matters in MLOps

When your model is running as an API in production it cannot crash. If someone sends 2 features instead of 4 the server should return a clean error response — not a 500 traceback. Every prediction function, every data loader, every model file reader needs proper error handling around it. This is the foundation of reliable production code.

---

*Day 04 done. Tomorrow — Logging.*