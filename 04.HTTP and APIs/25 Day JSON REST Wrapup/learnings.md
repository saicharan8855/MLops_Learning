# Day 25 — JSON Deep Dive, REST Design, and Topic 04 Wrap-Up

Last day of HTTP and APIs. Today was the smoothest session of the whole topic — almost everything ran clean on the first try, which says something about how much stuck from the previous four days. Ended with one script that pulls together every single concept from this week into a single reusable client function.

---

## Exercise 1 — JSON Objects vs Arrays

```python
import json

model_info = {
    "name": "iris-classifier",
    "version": "1.0",
    "accuracy": 0.95
}

all_models = [
    {"name": "iris-classifier", "version": "1.0"},
    {"name": "spam-detector", "version": "2.1"},
]

print(json.dumps(model_info, indent=2))
print(json.dumps(all_models, indent=2))

json_string = '{"name": "fraud-detector", "version": "1.5"}'
parsed = json.loads(json_string)
print(parsed, type(parsed))
```

Output —
```
Object as JSON string:
{
  "name": "iris-classifier",
  "version": "1.0",
  "accuracy": 0.95
}

Array as JSON string:
[
  {"name": "iris-classifier", "version": "1.0"},
  {"name": "spam-detector", "version": "2.1"}
]

Parsed back to Python dict: {'name': 'fraud-detector', 'version': '1.5'}
Type: <class 'dict'>
```

`json.dumps()` goes Python → JSON string, used right before sending data out. `json.loads()` goes JSON string → Python, used right after receiving data in. A curly-brace object is for one thing with named fields; a square-bracket array is for a list of things. Ran perfectly first try.

---

## Exercise 2 — Nested JSON (the real prediction response shape)

One small typo on the way —

```
python3 nest_json.py
# can't open file 'nest_json.py': No such file or directory
```

Filename was actually `nested_json.py` — fixed and ran clean —

```python
prediction_response = {
    "model": {"name": "iris-classifier", "version": "1.0"},
    "input": {"sepal_length": 5.1, "sepal_width": 3.5, ...},
    "result": {
        "prediction": "setosa",
        "confidence": 0.97,
        "probabilities": {"setosa": 0.97, "versicolor": 0.02, "virginica": 0.01}
    },
    "metadata": {"request_id": "abc-123", "timestamp": "2026-06-25T10:00:00Z"}
}
```

Output confirmed nested access works exactly as expected —
```
Prediction: setosa
Confidence: 0.97
Setosa probability: 0.97
```

This structure — grouping `model`, `input`, `result`, and `metadata` into separate nested objects rather than one flat dictionary — is intentionally close to what a real `/predict` endpoint response will look like. Flat data gets messy fast once there's more than 3-4 fields; nesting keeps related data together.

---

## Exercise 3 — REST Design Notes

```markdown
## Bad design (verb-based)
GET  /getAllModels
POST /createNewPrediction

## Good design (resource-based)
GET    /models              → list all models
GET    /models/5            → get model with id 5
DELETE /models/5            → delete model with id 5
```

The core idea written down — **the URL is the noun (what), the HTTP method is the verb (how)**. Same URL with a different method means something completely different. `GET /models/5` reads it. `DELETE /models/5` removes it. The resource doesn't change, only the action does.

---

## Exercise 4 — Mock Model API Client (everything from this week, in one function)

```python
def safe_request(method: str, endpoint: str, payload: dict = None, timeout: int = 5) -> dict:
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.request(method, url, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()
        return {"status": "success", "code": response.status_code, "data": response.json()}
    except requests.exceptions.Timeout:
        return {"status": "error", "reason": "timeout"}
    except requests.exceptions.ConnectionError:
        return {"status": "error", "reason": "connection_failed"}
    except requests.exceptions.HTTPError:
        return {"status": "error", "reason": f"http_error_{response.status_code}"}
    except Exception as e:
        return {"status": "error", "reason": str(e)}
```

Ran through a full simulated model lifecycle — list, create, update, delete, and a not-found case — and every single one returned cleanly —

```
GET    /users/1     → success, 200, full nested user object
POST   /posts       → success, 201, created prediction with id 101
PUT    /posts/1     → success, 200, replaced resource
DELETE /posts/1     → success, 200, empty data
GET    /posts/999999 → error, http_error_404
```

This one function now does everything separately learned across five days — picks the HTTP method dynamically with `requests.request(method, ...)`, attaches a Bearer token automatically, has a timeout, and catches every category of failure into one consistent return shape. No crashes, no unhandled exceptions, across five very different scenarios in a single run.

---

## Topic 04 — Looking Back

| Day | What stuck the most |
|---|---|
| 21 | Status codes aren't optional details — they're the first thing to check before trusting a body |
| 22 | POST creates, PUT replaces, DELETE removes — and only some of those are safe to repeat |
| 23 | Secrets belong in `.env`, never in code — directly reusing the Topic 01 config pattern |
| 24 | A request can fail in many different ways, and each one needs its own handling |
| 25 | All of it combines into one small, reusable, fail-safe client function |

The htbpin.org outages throughout the week turned out to be the most valuable accident of the whole topic — instead of every exercise running perfectly and feeling like a formality, real instability forced every error-handling concept to actually prove itself against a genuinely unreliable server.

---

## What to Remember

| Concept | What it means |
|---|---|
| `json.dumps()` | Python object → JSON string, for sending |
| `json.loads()` | JSON string → Python object, for receiving |
| JSON object `{}` | one thing, key-value pairs |
| JSON array `[]` | a list of things |
| Nested JSON | groups related fields together instead of one flat dict |
| REST URL = noun | `/models/5` is the resource |
| HTTP method = verb | GET/POST/PUT/DELETE define the action on that resource |
| `requests.request(method, ...)` | one function handles any HTTP method dynamically |

---

## Why This Matters in MLOps

Everything from this week comes together the moment a FastAPI `/predict` endpoint exists. FastAPI will handle a lot automatically — routing methods to functions, parsing JSON bodies, generating docs. But the things practiced this week are exactly what FastAPI does *not* do for free — designing a sensible nested response shape, protecting the endpoint with auth, and making sure the client calling it survives timeouts and errors gracefully. The `mock_model_api_client.py` written today is genuinely close to the real client code that will call the real endpoint in the next topic.

---

*Topic 04 — HTTP and APIs — complete. Next: Topic 05, FastAPI Basics.*