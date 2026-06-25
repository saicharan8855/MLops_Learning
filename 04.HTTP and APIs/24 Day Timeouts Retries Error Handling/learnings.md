# Day 24 — Timeouts, Retries, and Error Handling

Today's lesson proved itself in real time. The whole point was learning to handle unreliable servers gracefully — and httpbin.org being genuinely unreliable again today meant every exercise got tested against the exact kind of failure it was designed to handle, without even trying.

---

## Exercise 1 — No Timeout (baseline)

```python
print("sending request with no timeout set...")
response = requests.get("https://httpbin.org/delay/3")
print("status code:", response.status_code)
```

Expected this to just be slow and eventually return 200. Instead —

```
sending request with no timeout set...
status code: 503
```

httpbin returned `503` again — same flakiness from Day 21. Not a code bug, just the server being unavailable. Still demonstrates the core point though: without a timeout, the program has no choice but to sit there for however long the server takes to respond, whether that's 3 seconds or 3 minutes.

---

## Exercise 2 — With Timeout

```python
try:
    response = requests.get("https://httpbin.org/delay/3", timeout=2)
    print("status code:", response.status_code)
except requests.exceptions.Timeout:
    print("Request timed out after 2 seconds — giving up gracefully")
```

One typo on the way — `pytho3` instead of `python3`, caught immediately by bash's suggestion. After fixing it, the result was —

```
sending request with a 2 second timeout...
status code: 503
```

Again `503` rather than an actual timeout — the server responded fast with an error rather than being genuinely slow this time. The `timeout=2` setup was correct either way; it just didn't get exercised in this particular run since the server failed before the clock ran out.

---

## Exercise 3 — Retry with Exponential Backoff

This is where things got interesting.

```python
def call_with_retry(url, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=2)
            ...
        except requests.exceptions.Timeout:
            print(f"Attempt {attempt}: Timed out")
        ...
        wait_time = 2 ** attempt
        time.sleep(wait_time)
```

Output —
```
Attempt 1: Timed out
Waiting 2s before retrying...
Attempt 2: Timed out
Waiting 4s before retrying...
Attempt 3: Timed out
Waiting 8s before retrying...
All retries failed.
```

This time it actually hit a real timeout — three times in a row, with the wait growing 2 seconds, then 4, then 8, exactly as exponential backoff is supposed to work. httpbin was apparently overloaded enough that it couldn't even respond within 2 seconds, three separate times. The script handled it exactly the way it should — no crash, clear logging at every attempt, and a clean "all retries failed" message instead of an unhandled exception.

---

## Exercise 4 — Why Retrying POST Is Dangerous

```python
def unsafe_retry_post(url, payload, max_retries=3):
    for attempt in range(1, max_retries + 1):
        response = requests.post(url, json=payload)
        print(f"Attempt {attempt}: Created resource with id {response.json().get('id')}")
```

Output —
```
Attempt 1: Created resource with id 101
Attempt 2: Created resource with id 101
Attempt 3: Created resource with id 101
```

All three attempts show `id: 101` — but that's specifically because jsonplaceholder is a fake API that doesn't actually persist anything. It always reports the same fake id for a new post rather than incrementing it. In a real database, this exact code would have created three separate rows with three different, increasing IDs from one logical "create a post" action that was only supposed to happen once. The fake API's behavior here slightly hides the danger, but the underlying point still holds — POST is not safe to retry blindly, because each retry is treated as a brand new creation request, not a repeat of the same one.

---

## Exercise 5 — The Production-Style Safe Wrapper

```python
def safe_get(url: str, headers: dict = None, timeout: int = 5) -> dict:
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.Timeout:
        return {"status": "error", "reason": "Request timed out"}
    except requests.exceptions.ConnectionError:
        return {"status": "error", "reason": "Could not connect to server"}
    except requests.exceptions.HTTPError as e:
        return {"status": "error", "reason": f"HTTP error: {e}"}
    except requests.exceptions.JSONDecodeError:
        return {"status": "error", "reason": "Server returned non-JSON response"}
    except Exception as e:
        return {"status": "error", "reason": f"Unexpected error: {e}"}
```

Tested against four very different scenarios, and every single one returned cleanly —

```python
{'status': 'success', 'data': {...}}
{'status': 'error', 'reason': 'HTTP error: 404 Client Error: Not Found for url: .../posts/99999'}
{'status': 'error', 'reason': 'Request timed out'}
{'status': 'error', 'reason': 'Could not connect to server'}
```

In order — a real post that exists, a post ID that doesn't exist (caught by `raise_for_status()` as an `HTTPError`), a deliberately slow endpoint that exceeded the timeout, and a domain that doesn't even resolve on the internet. Not one of these crashed the script. Every failure became a predictable dictionary the calling code can branch on with a simple `if result["status"] == "success"` check.

`response.raise_for_status()` is the key new piece here — instead of manually checking `if response.status_code >= 400`, this one call automatically raises an exception for any 4xx or 5xx response, which then gets caught by the `except HTTPError` block below it.

---

## What to Remember

| Concept | What it means |
|---|---|
| `timeout=N` | stop waiting after N seconds instead of hanging forever |
| `requests.exceptions.Timeout` | raised when the timeout is hit |
| `requests.exceptions.ConnectionError` | raised when the server can't be reached at all |
| Exponential backoff | wait longer between each retry (2s, 4s, 8s...) |
| Retrying GET/PUT/DELETE | generally safe — idempotent |
| Retrying POST blindly | dangerous — can create duplicate resources |
| `response.raise_for_status()` | auto-raises an exception for 4xx/5xx responses |
| Wrapping API calls in try/except | turns unpredictable failures into predictable return values |

---

## Why This Matters in MLOps

A model-serving endpoint will eventually be called by something — a frontend, another service, a scheduled job — and that caller needs to survive the model server being briefly slow, briefly down, or unreachable. Today's `safe_get` pattern is exactly the shape of code that belongs around any real call to a `/predict` endpoint. And the fact that httpbin's own instability today turned into a live demonstration of every failure mode in the lesson is, honestly, the most realistic practice session so far — production systems don't fail in clean, predictable ways either.

---

*Day 24 done. HTTP and APIs topic continuing.*