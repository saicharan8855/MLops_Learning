# Day 03 — Modules and Packages

## What I Did Today

Day 3 was about structuring Python code properly. Not just writing everything in one file — but splitting it into modules and packages the way real projects do it.

---

## What is a Module

A module is just a `.py` file. That's it. Every Python file you write is a module. You can import it from another file and use what's inside.

```python
# data.py is a module
from iris_package.data import get_sample_data
```

---

## What is a Package

A package is a folder that contains Python modules. But not just any folder — it needs one special file inside it called `__init__.py`. Without that file Python treats the folder as just a folder, not a package.

```
iris_package/
├── __init__.py      ← this makes it a package
├── data.py
├── model.py
└── utils.py
```

---

## What I Built Today

A small iris prediction package split across 3 files — each file doing one specific job.

### data.py — handles data

```python
from typing import List, Tuple

def get_sample_data() -> List[List[float]]:
    """Return hardcoded iris sample data."""
    return [
        [5.1, 3.5, 1.4, 0.2],
        [6.2, 2.9, 4.3, 1.3],
        [7.3, 3.0, 6.3, 1.8],
    ]

def split_data(
    data: List[List[float]],
    split: float = 0.8
) -> Tuple[List[List[float]], List[List[float]]]:
    """Split data into train and test sets."""
    cut = int(len(data) * split)
    return data[:cut], data[cut:]
```

### utils.py — handles helper functions

```python
from typing import List

def validate_features(features: List[float]) -> bool:
    """Check if feature list has exactly 4 values."""
    if len(features) != 4:
        raise ValueError(f"Expected 4 features, got {len(features)}")
    return True

def get_label(prediction: int) -> str:
    """Convert prediction index to label name."""
    labels = {0: "setosa", 1: "versicolor", 2: "virginica"}
    return labels.get(prediction, "unknown")
```

### model.py — handles prediction

```python
from typing import List, Dict
from iris_package.utils import validate_features, get_label

def predict(features: List[float]) -> Dict[str, str]:
    validate_features(features)

    if features[0] < 5.5:
        label = get_label(0)
    elif features[0] < 6.5:
        label = get_label(1)
    else:
        label = get_label(2)

    return {"prediction": label, "status": "success"}
```

### `__init__.py` — the gateway

```python
from iris_package.data import get_sample_data, split_data
from iris_package.model import predict
from iris_package.utils import get_label, validate_features
```

This file is what allows `main.py` to do clean imports like —

```python
from iris_package import get_sample_data, predict
```

Without `__init__.py` Python doesn't know this folder is a package and imports break.

### main.py — entry point

```python
from iris_package.data import get_sample_data, split_data
from iris_package.model import predict

def main() -> None:
    data = get_sample_data()
    print(f"Total samples: {len(data)}")

    train, test = split_data(data, split=0.8)
    print(f"Train samples: {len(train)}")
    print(f"Test samples: {len(test)}")

    for sample in test:
        result = predict(sample)
        print(f"Input: {sample} → Prediction: {result['prediction']}")

if __name__ == "__main__":
    main()
```

---

## Errors I Hit and Fixed

### Error 1 — `cannot import name 'get_sample_data' from 'iris_package'`

Happened because `__init__.py` was empty. Python found the package but had nothing to expose from it.

Fix — added the imports inside `__init__.py`.

### Error 2 — `No module named 'utils'`

Happened inside `model.py` because the import was written as —

```python
from utils import validate_features  # wrong
```

Python didn't know where `utils` was. The correct way is to always use the full package path —

```python
from iris_package.utils import validate_features  # correct
```

**Key lesson — always use full package paths when importing between files inside a package.**

---

## What to Understand

| Concept | What it means |
|---|---|
| module | any single `.py` file |
| package | folder with `__init__.py` inside |
| `__init__.py` | makes a folder a package, controls what gets exposed |
| `from package.module import something` | full path import |
| separating concerns | each file does one job only |

---

## Why This Matters in MLOps

Every real MLOps project is structured this way. You'll never see a production codebase with all the code in one file. Data loading, model logic, utilities — they all live separately. When you containerize with Docker or serve with FastAPI, Python needs to find your code cleanly. This structure is what makes that possible.

---

*Day 03 done. Tomorrow — Error Handling.*