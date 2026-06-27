# Day 27 — FastAPI POST Requests and Request Bodies

Today added a POST endpoint to yesterday's FastAPI server, backed by a small Pydantic model describing exactly what shape the request body needs. Also ran into a very real, very common mistake — trying to call a server that wasn't actually running — which turned into a live example of the exact `ConnectionError` scenario covered back in Day 24's error handling lesson.

---

## Setup

One typo before anything else —

```bash
source venv\bin\activate
# -bash: venvbinactivate: No such file or directory
```

Backslashes are a Windows path convention — bash on Linux only understands forward slashes. Fixed —

```bash
source venv/bin/activate
```

`python3-venv` was already installed from a previous session, so no reinstall was needed this time.

---

## Exercise 1 — Adding the POST Endpoint

```python
class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@app.post("/predict")
def predict_body(features: IrisFeatures):
    return {
        "input": [
            features.sepal_length,
            features.sepal_width,
            features.petal_length,
            features.petal_width
        ],
        "prediction": "setosa"
    }
```

`IrisFeatures` is the simplest possible Pydantic model — four named fields, each with a type. FastAPI reads this class and knows exactly what a valid request body looks like, without any manual `if` checks written anywhere.

---

## Exercise 2-3 — Testing the Endpoint

The uvicorn server log showed three POST requests in a row, and notably **all three came back `422 Unprocessable Content`** —

```
INFO: "POST /predict HTTP/1.1" 422 Unprocessable Content
INFO: "POST /predict HTTP/1.1" 422 Unprocessable Content
INFO: "POST /predict HTTP/1.1" 422 Unprocessable Content
```

The two deliberately broken requests (missing field, wrong type) were *supposed* to fail with 422 — that's the automatic validation working exactly as expected, no validation code written by hand. But if the very first, supposedly-valid request also shows 422 in this log, that's worth double-checking — the most common cause is a quoting issue in the curl command itself (single quotes inside a JSON body can get mangled by the shell depending on exactly how they're escaped). Worth rerunning the valid example on its own and confirming it actually returns `200` with a real prediction back, rather than assuming it did.

Either way, the core lesson came through clearly — FastAPI rejected malformed input automatically, with a clear error response instead of crashing the server or silently accepting bad data.

---

## Exercise 5 — The Connection Refused Error

Wrote `call_my_api.py` to call the new POST endpoint using `requests`, same pattern as Day 22 and Day 23 —

```python
response = requests.post("http://127.0.0.1:8000/predict", json=payload)
```

Ran it and got a wall of traceback ending in —

```
requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=8000): 
Max retries exceeded with url: /predict (Caused by NewConnectionError(... Connection refused))
```

The uvicorn server had already been stopped with `Ctrl+C` a little earlier in the session — so there was simply nothing listening on port 8000 anymore. The client code itself was completely correct; it just had no server to talk to.

This is exactly the `ConnectionError` exception type wrapped and handled back in Day 24's `safe_get` function — except this time experienced firsthand rather than read about. Tried running the script a second time with the same result, since the server still wasn't restarted yet at that point.

Restarted the server afterward —

```bash
uvicorn main:app --reload
# Application startup complete.
```

— but the session ended there with `Ctrl+C` shortly after, before `call_my_api.py` got a chance to run again against a live server. **This is a loose end worth closing before moving on** — rerun the server, leave it running in one terminal, and run `call_my_api.py` in a second terminal to actually see a successful `200` response with a real prediction, rather than ending the day on the connection-refused error.

---

## What to Remember

| Concept | What it means |
|---|---|
| `class X(BaseModel)` | defines the required shape of a request body |
| `@app.post("/path")` | registers a function to handle POST requests |
| `422 Unprocessable Content` | FastAPI's automatic response to invalid request data |
| `ConnectionRefusedError` | nothing is listening on that host/port — server isn't running |
| Client code can be correct and still fail | if the thing it's calling isn't actually up |
| Always confirm the server log shows "Application startup complete" | before testing from a second terminal |

---

## Why This Matters in MLOps

Two real production lessons collided today by accident. First — automatic request validation is exactly what protects a deployed model from receiving four strings instead of four floats and crashing somewhere deep inside the prediction logic; FastAPI stops bad data at the door. Second — a `ConnectionRefused` error from a client is one of the most common real-world support tickets in any system with a client and a server running separately: "it's not working" almost always means "is the other side even running right now?" before it means anything more complicated.

---

*Day 27 — needs a quick rerun to confirm call_my_api.py succeeds against a live server before fully closing out. FastAPI Basics continuing.*