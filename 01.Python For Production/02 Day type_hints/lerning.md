# Day 02 — Functions + Type Hints

## What I Did Today

Day 2 was about writing functions the right way. Not just functions that work — functions that tell you exactly what goes in and what comes out. That's what type hints are for.

---

## What Are Type Hints

Type hints are a way to label your function arguments and return values with their expected types. Python won't crash if you ignore them — they don't enforce anything at runtime. But they make your code readable, catch bugs early, and are used by tools like `mypy` to validate your code before it even runs.

Simple example —

```python
def add_numbers(a: int, b: int) -> int:
    return a + b
```

`a: int` means this argument should be an integer. `-> int` means this function returns an integer. That's it.

---

## What I Practiced

### Exercise 1 — Basic types

Started with the simplest possible type hints — `int`, `str`, `float`, `bool`.

```python
def add_numbers(a: int, b: int) -> int:
    return a + b

def greet_user(name:str) -> str:
    return f"Hello {name}!"

def is_valid(age: int) -> bool:
    return age > 0


print(add_numbers(5,10))
print(greet_user("saicharan"))
print(is_valid(20))
```

Nothing fancy. Just getting comfortable with the syntax.

---

### Exercise 2 — Collection types

Real data in ML is never just a single number. It's lists, dictionaries, tuples. So I learned how to type hint those.

```python
from typing import List, Dict, Tuple

def get_features(data: List[float]) -> int:
    return len(data)

def get_model_info(model: str , version: float) -> Dict[str , str]:
    return {
        "model" : model ,
        "version" : str(version)
    }

def get_min_max(data : List[float]) -> Tuple[float , float]:
    return min(data) , max(data)

print(get_features([1.0 , 2.0 , 3.5 , 4.0]))
print(get_model_info("iris" , 1.0))
print(get_min_max([1.0 , 2.0 , 3.0 , 4.0 , 5.0]))
```

`List[float]` means a list where every item is a float. `Dict[str, str]` means a dictionary where both keys and values are strings. `Tuple[float, float]` means exactly two floats.

---

### Exercise 3 — Optional types

Sometimes a function might return a value or might return nothing. That's `Optional`.

```python
from typing import Optional

def label(prediction: int) -> Optional[str]:
    labels = {0: "cat" , 1: " dog" , 2: " rabbit"}
    return labels.get(prediction)

print(label(1))
print(label(5))
```

`Optional[str]` means the function returns either a string or `None`. This is honest — it tells whoever reads the code that None is a real possible output, not a surprise.

---

### Exercise 4 — Docstrings with type hints

Type hints tell you the types. Docstrings tell you the meaning. Together they make a function completely self-explanatory.

```python
def predict_iris(features : List[float]) -> Dict[str , str]:
    """"
    Predict the iris species based on the input data
    Args:
        data (float): The input data for prediction
    Returns:
        Dict[str , str]: A dictionary containing the predicted species
    """
    if len(features) != 4:
        raise ValueError(f"expected 4 features but got {len(features)}")
    
    return {
        "Prdiction" : "setosa" , 
        "status" : "success"
    }

print(predict_iris([5.1 , 3.5 , 1.4 , 0.2]))
```

This is the standard format used in real production codebases. Args section explains each input. Returns section explains the output.

---

### Exercise 5 — Union types

Sometimes a function should accept more than one type. `Union` handles that.

```python
from typing import Union

def process_age(age: Union[int , str , float]) -> str:
    return str(age)


def process_data(data: Union[float ,str]) -> str:
    return str(data)

print(process_age(20))
print(process_data(3.14))
```

`Union[int, float, str]` means the argument can be any of those three types.

---

### Exercise 6 — List of Dicts

In real MLOps you deal with batches of data — not one sample but many. This is how that looks with type hints.

```python
def batch_predict(data: List[Dict[str , float]]) -> List[str]:
    """
    Predict for multiple samples at once

    Args:
        samples: List of feature dictionaries
    Returns:
        List of predicted labels
    """
    result = []
    for sample in data:
        result.append("setosa")
    return result 

samples = [
    {"sepal_length": 5.1, "sepal_width": 3.5},
    {"sepal_length": 6.2, "sepal_width": 2.9},
]
print(batch_predict(samples))
```

`List[Dict[str, float]]` — a list where each item is a dictionary with string keys and float values. This is a very common shape in ML input data.

---

### Exercise 7 — Default values with type hints

Functions can have default values and type hints at the same time.

```python
def create_expeirment(
        name: str,
        version: float = 1.0,
        debug: bool = False,
    ) -> Dict[str, Union[str, float, bool]]:
    
    return {
        "name" : name,
        "version" : version,
        "bebug" : debug
    }
print(create_expeirment("iris"))
print(create_expeirment("iris" , version=2.0 , debug=True))
```

`version: float = 1.0` means version is a float and defaults to 1.0 if not passed. Clean and readable.

---

### Exercise 8 — Type hints with loops and conditions

Type hints work everywhere — not just simple one-liners.

```python
def filter_valid_features(all_samples: List[Union[float , str]] , expected_length: int) -> List[float]:
    valid_features = []
    for sample in all_samples:
        if len(sample) == expected_length:
            valid_features.append(sample)
    return valid_features

samples = [
    [5.1 , 3.5 , 1.4 , 0.2],
    [6.2 , 2.9 , 4.3],
    [7.0 , 3.2 , 4.7 , 1.4]
]

print(filter_valid_features(samples , expected_length=4))
```

`List[List[float]]` — a list of lists, where each inner list contains floats. This is how raw feature data looks before it hits a model.

---

### Exercise 9 — Nested Dict return type

Real model reports are nested. Learning to type hint them properly.

```python
from typing import Any

def get_model_results(
        model_name: str,
        accuracy: float,
        features: List[str]
) -> Dict[str , Any]:
    
    return {
        "model_name" : model_name,
        "metrics" : {
            "accuracy" : accuracy,
            "features_count" : len(features)
        },
        "features" : features,
        "status" : "ready" if accuracy > 0.8 else "needs improvement"
    }

print(get_model_results(
    model_name="iris-classifier",
    accuracy=0.95,
    features=["sepal_length", "sepal_width", "petal_length", "petal_width"]
))
```

`Dict[str, Any]` is used when the dictionary values can be of mixed types — strings, numbers, nested dicts. `Any` basically says don't restrict the value type.

---

## Full Type Hints Cheatsheet

| Type hint | What it means |
|---|---|
| `int, float, str, bool` | basic Python types |
| `List[float]` | list where every item is a float |
| `Dict[str, str]` | dictionary with string keys and string values |
| `Tuple[float, float]` | exactly two floats |
| `Optional[str]` | string or None |
| `Union[int, float]` | int or float |
| `List[Dict[str, float]]` | list of dictionaries |
| `Dict[str, Any]` | dict with mixed value types |
| `-> None` | function returns nothing |

---

## One Thing to Remember

Type hints are not enforced by Python. If you pass a string where an int is expected, Python won't stop you. The value of type hints is for humans reading the code and for static analysis tools like `mypy`. In production teams nobody reads undocumented functions — type hints and docstrings together make functions self-documenting.

---

*Day 02 done. Tomorrow — Modules and `__init__.py`.*