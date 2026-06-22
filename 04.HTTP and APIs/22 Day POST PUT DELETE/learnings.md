# Day 22 — POST, PUT, DELETE and Idempotency

Today moved past GET into the methods that actually change something on a server — POST to create, PUT to update, DELETE to remove. Also built a fake prediction client that's a direct preview of what the real FastAPI client code will look like later in this grind. Hit a handful of typos along the way, each one a useful reminder of how unforgiving both Python and bash are about exact spelling.

---

## Exercise 1 — POST (create something)

First attempt hit a syntax error —

```
File "post_request.py", line 5
    "userId" : 1
             ^
SyntaxError: invalid syntax
```

Likely a missing comma on the line above it in the dictionary — Python dictionaries need commas between every key-value pair, and a missing one shows up as a syntax error on the *next* line, which can be confusing the first few times you see it.

Second attempt had a different problem —

```python
import requets
ModuleNotFoundError: No module named 'requets'
```

Typo'd `requests` as `requets`. Fixed both issues and it ran clean —

```python
import requests

new_post = {
    "title": "iris predictor",
    "body": "model predicted setosa with 0.95 confidence",
    "userId": 1
}

response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=new_post
)

print("status code :", response.status_code)
print("created resources :", response.json())
```

Output —
```
status code : 201
created resources : {'title': 'iris predictor', 'body': '...', 'userId': 1, 'id': 101}
```

`201` instead of `200` — that's the REST convention for "something new was created." The server even assigned it a new `id: 101`. Passing `json=new_post` to `requests.post` does two things automatically — converts the dict to a JSON string, and sets the `Content-Type: application/json` header. No manual work needed for either.

---

## Exercise 2 — PUT (full replace)

Saved the file as `put_requests.py` (plural) but tried running `put_request.py` (singular) first —

```
python3: can't open file 'put_request.py': No such file or directory
```

Ran the correct filename and it worked —

```python
updated_post = {
    "id": 1,
    "title": "iris prediction - updated",
    "body": "model re-predicted versicolor with 0.88 confidence",
    "userId": 1
}

response = requests.put(
    "https://jsonplaceholder.typicode.com/posts/1",
    json=updated_post
)
```

Output —
```
status code : 200
updated resource : {'id': 1, 'title': 'iris prediction - updated', 'body': '...', 'userId': 1}
```

`200` here, not `201` — PUT doesn't create something new, it replaces what's already there at that exact URL (`/posts/1`). Every field had to be sent, even `id` and `userId` which didn't actually change. That's the PUT contract — full replacement, not a partial patch.

---

## Exercise 3 — DELETE

Hit a real syntax error this time —

```python
print("body :" , ,response.text)
```

Extra comma typed by accident — two commas in a row before `response.text`. Python doesn't know what's supposed to go between them. Fixed by removing the extra comma —

```python
print("body :", response.text)
```

Also typo'd `pyhton3` instead of `python3` once along the way — bash correctly suggested the fix.

Final run —
```
status code : 200
body : {}
```

Empty body with `200` is jsonplaceholder's way of confirming the delete succeeded. Some real APIs return `204 No Content` for the same situation — both mean "it's gone, nothing more to say."

---

## Exercise 4 — Idempotency

```python
for i in range(3):
    response = requests.delete("https://jsonplaceholder.typicode.com/posts/1")
    print(f"Attempt {i+1} → Status: {response.status_code}")
```

Output —
```
Attempt 1 → Status: 200
Attempt 2 → Status: 200
Attempt 3 → Status: 200
```

Same status code all three times, even though the post was already "deleted" after attempt 1. That's idempotency in action — calling DELETE on something that's already gone still reports success, rather than erroring out. Compare that to POST: calling POST three times would create three separate new resources, each with its own new ID. DELETE and PUT are idempotent — repeating them doesn't change the outcome. POST is not — repeating it multiplies the effect.

---

## Exercise 5 — Fake Predict Client

This is the one that matters most for where this grind is heading.

```python
def send_prediction_request(features: list) -> dict:
    payload = {
        "title": "iris_prediction_request",
        "body": str(features),
        "userId": 1
    }
    response = requests.post(
        "https://jsonplaceholder.typicode.com/posts",
        json=payload
    )
    if response.status_code == 201:
        return {"status": "success", "data": response.json()}
    else:
        return {"status": "failed", "code": response.status_code}
```

First run threw a `NameError` —

```python
for features in test_cases:
    result = send_prediction_request(features)
    print(f"features {feature} -> {result}")  # wrong variable name
```

Loop variable was `features` but the print statement referenced `feature` (singular) — a name that was never defined. Fixed by matching the variable name exactly —

```python
print(f"features {features} -> {result}")
```

Final output —
```
features [5.1, 3.5, 1.4, 0.2] -> {'status': 'success', 'data': {...}}
features [6.2, 2.9, 4.3, 1.3] -> {'status': 'success', 'data': {...}}
features [7.3, 3.0, 6.3, 1.8] -> {'status': 'success', 'data': {...}}
```

All three fake iris samples "sent" successfully. This function shape — take features in, POST them as JSON, check the status code, return a clean success/failure dict — is almost exactly what the real client code will look like once there's an actual FastAPI `/predict` endpoint to call instead of jsonplaceholder standing in for it.

---

## Typos Made Today

| Typo | Should be |
|---|---|
| `import requets` | `import requests` |
| `put_request.py` (ran) | `put_requests.py` (saved) |
| `print("body :" , ,response.text)` | one comma, not two |
| `pyhton3` | `python3` |
| `{feature}` in f-string | `{features}` — matched loop variable name |

Every single one of these caused either a `SyntaxError`, `ModuleNotFoundError`, `NameError`, or a plain "file not found" — and every single one was caught immediately by Python's error message pointing at the exact line.

---

## What to Remember

| Concept | What it means |
|---|---|
| `requests.post(url, json=data)` | creates something, returns 201 |
| `requests.put(url, json=data)` | replaces something fully, returns 200 |
| `requests.delete(url)` | removes something, often returns 200 or 204 |
| Idempotent (PUT, DELETE) | repeating it gives the same result |
| Not idempotent (POST) | repeating it creates multiple new things |
| `json=` parameter | auto-converts dict to JSON, sets Content-Type header |

---

## Why This Matters in MLOps

The `send_prediction_request` function written today is the rough draft of the actual client code that will call a real `/predict` endpoint once FastAPI is set up. Understanding POST vs PUT vs DELETE now means understanding exactly why a model-serving API uses POST for predictions (each prediction request is a new event, not a replacement of an old one) and why a model registry might use PUT to update a model's metadata (replacing the existing record entirely) or DELETE to retire an old version.

---

*Day 22 done. HTTP and APIs topic continuing.*