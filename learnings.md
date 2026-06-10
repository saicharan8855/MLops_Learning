# Day 10 — Load and Use the Saved Model

Yesterday trained the model and saved it as a `.pkl` file. Today loaded it back and made predictions with it. This is the exact pattern FastAPI will use later — load the file at startup, run predictions on demand.

---

## What Loading a Model Actually Means

When you train a model, sklearn builds a Python object in memory — decision trees, weights, learned patterns, everything. `pickle.dump` freezes that object into a binary file on disk. `pickle.load` thaws it back into the exact same object. No retraining, no recalculating — the model picks up right where training left off.

---

## The Path Problem I Hit First

Ran the script from the wrong folder. Got this —

```
FileNotFoundError: No such file or directory: '../09 Day Iris Model/model/iris_model.pkl'
```

Relative paths like `../` depend on where you run the script from, not where the script lives. Fix was to build the path dynamically using `__file__` —

```python
model_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "09 Day Iris Model",
    "model",
    "iris_model.pkl"
)
```

`__file__` is the script's own location. `os.path.abspath` converts it to a full absolute path. `os.path.dirname` strips the filename leaving just the folder. Then `os.path.join` builds the full path to the model from there. Works regardless of where you run the script from.

---

## The Second Problem

Ran the script outside venv. Got —

```
ModuleNotFoundError: No module named 'numpy'
```

numpy was installed inside venv, not globally. Python was looking in the wrong place. Fix was to activate venv first, then run.

```bash
venv\Scripts\activate
python predict.py
```

If `(venv)` isn't showing in the terminal, venv isn't active. That's the check.

---

## What I Built

```python
import pickle
import os
from typing import List, Dict, Any

model_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "09 Day Iris Model",
    "model",
    "iris_model.pkl"
)

with open(model_path, "rb") as f:
    model = pickle.load(f)

print("model loaded successfully")

labels = {0: "setosa", 1: "versicolor", 2: "virginica"}

def predict(features: List[float]) -> Dict[str, Any]:
    if len(features) != 4:
        raise ValueError(f"Expected 4 features, got {len(features)}")

    prediction = model.predict([features])[0]
    probabilities = model.predict_proba([features])[0]
    confidence = round(float(max(probabilities)), 4)

    return {
        "prediction": labels[prediction],
        "confidence": confidence,
        "status": "success"
    }

print(predict([5.1, 3.5, 1.4, 0.2]))
print(predict([6.2, 2.9, 4.3, 1.3]))
print(predict([7.3, 3.0, 6.3, 1.8]))
```

Output —
```
model loaded successfully
{'prediction': 'setosa', 'confidence': 1.0, 'status': 'success'}
{'prediction': 'versicolor', 'confidence': 0.9, 'status': 'success'}
{'prediction': 'virginica', 'confidence': 1.0, 'status': 'success'}
```

---

## What Each Part Does

### Loading the model

```python
with open(model_path, "rb") as f:
    model = pickle.load(f)
```

`"rb"` means read binary. The pkl file is binary — not plain text. `pickle.load` deserializes it back into a sklearn RandomForestClassifier object with all its trained trees intact.

### Predicting

```python
prediction = model.predict([features])[0]
```

`model.predict` expects a 2D array — a list of samples. So `[features]` wraps the single sample in a list. `[0]` pulls out the first result since we only sent one sample.

### Confidence score

```python
probabilities = model.predict_proba([features])[0]
confidence = round(float(max(probabilities)), 4)
```

`predict_proba` returns the probability for each class. `max` picks the highest one — that's how confident the model is about its prediction. A confidence of 1.0 means the model is completely certain.

### Label map

```python
labels = {0: "setosa", 1: "versicolor", 2: "virginica"}
```

The model returns integers — 0, 1, or 2. The label map converts them to readable names.

---

## What to Remember

| Concept | What it means |
|---|---|
| `pickle.load` | deserializes model back into memory |
| `"rb"` | read binary mode |
| `__file__` | the script's own path |
| `model.predict([features])` | needs 2D input, returns array |
| `predict_proba` | confidence scores per class |
| activate venv first | always, before running anything |

---

## Why This Pattern Matters

This is exactly what a FastAPI endpoint does — loads the pkl file when the server starts, then calls `model.predict()` every time a request comes in. Understanding this flow now means FastAPI later is just wrapping this in an HTTP endpoint. Nothing fundamentally new.

---

*Day 10 done. One more half load day tomorrow. Full load resumes Day 12.*