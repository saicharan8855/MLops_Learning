# Day 09 — Train and Save the Iris Model

Lighter day — exams still ongoing. But this was probably the most important thing I've built so far. Every topic from here uses this model. FastAPI will serve it, Docker will containerize it, MLflow will track it. One file, built once, carried everywhere.

---

## The Dataset

Iris is a classic — 150 flower samples, 3 species, 4 measurements each. Ships inside scikit-learn so there's nothing to download. Perfect for learning because the data is clean, small, and well understood.

The 4 features per sample:
- sepal length
- sepal width
- petal length
- petal width

The 3 classes to predict: `setosa`, `versicolor`, `virginica`

---

## What I Built

```python
import pickle
import os
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy:.2f}")

os.makedirs("model", exist_ok=True)
with open("model/iris_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("model saved to model/iris_model.pkl")

print(f"Classes: {list(iris.target_names)}")
```

Output:
```
Accuracy: 1.00
model saved to model/iris_model.pkl
Classes: ['setosa', 'versicolor', 'virginica']
```

---

## What Each Part Does

### Load and split

```python
iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

`load_iris()` gives back the full dataset. `X` is the features, `y` is the labels. `train_test_split` cuts 80% for training and 20% for testing. `random_state=42` makes the split reproducible — same split every time you run it.

### Train

```python
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
```

Random Forest builds 100 decision trees and combines their votes. `random_state=42` here makes the model reproducible too. Same data, same seed, same model every run.

### Evaluate

```python
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
```

Run the model on test data it has never seen. Compare its predictions against the real labels. 1.00 accuracy means it got every single test sample right — Iris is a clean dataset so this is expected.

### Save with pickle

```python
os.makedirs("model", exist_ok=True)
with open("model/iris_model.pkl", "wb") as f:
    pickle.dump(model, f)
```

`pickle.dump` serializes the trained model into a binary file. `"wb"` means write binary. `exist_ok=True` means create the folder if it doesn't exist, don't crash if it does. The `.pkl` file now contains the fully trained model — weights, trees, everything.

This file is what FastAPI will load later to serve predictions.

---

## Why random_state Matters

Without `random_state`, every run gives a slightly different model because the randomness is unseeded. With it, the model is identical every time. In production this matters — if something breaks you need to be able to reproduce the exact model that was running.

---

## What Gets Gitignored

```
model/*.pkl
```

Model files are binary, heavy, and machine-generated. They don't belong in version control. Anyone who clones the repo runs `python train.py` to regenerate the model locally. MLflow handles proper model versioning later in the grind.

---

## Why This Model Specifically

Could have used any dataset but Iris makes sense here because it needs no downloading, no preprocessing, no cleaning — just load and train. The goal of this grind is MLOps not ML, so keeping the model dead simple means the focus stays on the infrastructure around it.

---

## What's Coming Next

This `.pkl` file is about to show up everywhere —

| Topic | How the model gets used |
|---|---|
| Git workflow | version the training script |
| FastAPI | load pkl, serve predictions via API |
| Docker | containerize the API + model together |
| MLflow | track training runs, log the model |
| Deployment | ship the container to the cloud |
| Model Registry | version and stage the model properly |

---

*Day 09 done. Exams wrapping up. Full load Day 12.*