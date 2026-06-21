# Day 21 — HTTP Basics: Requests, Responses, and Status Codes

Topic 04 kicks off. Today was less about new syntax and more about understanding what actually happens every time a client talks to a server — and dealing with a genuinely flaky public test API along the way, which turned into its own useful lesson.

---

## The Core Idea

Every API call is just two messages —

```
Client → Request  → Server
Client ← Response ← Server
```

A request carries a method (GET, POST, etc), a URL, headers, and sometimes a body. A response carries a status code, headers, and a body. Everything in FastAPI, every model serving endpoint, every webhook — all of it is built on this same two-message pattern.

---

## Exercise 1 — Status Codes with curl

```bash
curl -o /dev/null/ -s -w "%{http_code}\n" https://httpbin.org/status/200
# 200

curl -o /dev/null/ -s -w "%{http_code}\n" https://httpbin.org/status/404
# 503  ← unexpected

curl -o /dev/null/ -s -w "%{http_code}\n" https://httpbin.org/status/301
# 301
```

Three out of five requests came back `503` instead of the status code that was actually being requested. This wasn't a curl mistake — httpbin.org itself was overloaded and unable to serve requests reliably. The `301` and the first `200` happened to get through; the rest didn't. First real taste of working against a public service that isn't always available — something every API consumer eventually runs into.

---

## Setting Up the Python Environment

Tried to create a fresh venv for this topic and hit a setup error —

```
The virtual environment was not created successfully because ensurepip is not
available. apt install python3.14-venv
```

Ubuntu's Python 3.14 doesn't ship the venv tooling by default — it's a separate package. Fixed it —

```bash
sudo apt update
sudo apt install python3.14-venv
```

First `sudo` attempt failed with "Authentication failed" — simple mistyped password, nothing more. Retried and it went through. After installing the package, venv created cleanly —

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests
```

---

## Exercise 3 — First requests Script, and the 503 Problem

```python
import requests

response = requests.get("https://httpbin.org/get")
print("status code:", response.status_code)
print("headers :", response.headers["Content-Type"])
print("body :", response.json())
```

First run —

```
status code: 503
headers : text/html
JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

This is the same httpbin outage showing up inside Python now. The server returned an HTML error page instead of JSON. `response.json()` tries to parse whatever came back as JSON — when it's actually HTML, parsing fails and throws `JSONDecodeError`. The status code and the content type headers both already told the real story (`503`, `text/html`) before the crash even happened — that's exactly the kind of information that should be checked *before* trusting the body.

Ran the exact same script again a minute later and it went through clean —

```
Status code: 200
Headers: application/json
Body: {'args': {}, 'headers': {...}, 'origin': '...', 'url': 'https://httpbin.org/get'}
```

Same code, different outcome — purely because of the server's state at that moment, not anything in the script.

---

## Exercise 4 — Inspecting a Full Response

Hit the 503 issue twice more on `inspect_response.py`, with the same `JSONDecodeError` pattern. At that point switched the URL entirely to a more reliable test API — `jsonplaceholder.typicode.com` — instead of keep retrying httpbin.

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

print("Status code:", response.status_code)
print("OK?:", response.ok)
print("URL:", response.url)

for key, value in response.headers.items():
    print(f"  {key}: {value}")

print(response.json())
```

This worked immediately and consistently —

```
Status code: 200
OK?: True
```

`response.ok` returned `True` here, and earlier with httpbin it had returned `False` during the outage. This is exactly what `.ok` is for — a fast boolean check without needing to remember exact status code numbers. The full headers list also showed real production details — cache control, rate limit headers (`X-Ratelimit-Limit: 1000`), CDN info (`cloudflare`, `CF-RAY`) — the kind of metadata that's invisible unless you actually go looking at the headers.

---

## Exercise 5 — Branching on Status Code

```python
urls = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/9999",
]

for url in urls:
    response = requests.get(url)
    if response.status_code == 200:
        print(f"{url} → Success")
    elif response.status_code == 404:
        print(f"{url} → Not Found")
    elif response.status_code >= 500:
        print(f"{url} → Server Error")
    else:
        print(f"{url} → Status: {response.status_code}")
```

Output —
```
https://jsonplaceholder.typicode.com/posts/1 → Success
https://jsonplaceholder.typicode.com/posts/9999 → Not Found
```

Post `1` exists, post `9999` doesn't — the API correctly returned `404` for the second one, and the script correctly branched on it without crashing.

---

## Exercise 6 — Query Parameters

```python
params = {"userId": 1}
response = requests.get("https://jsonplaceholder.typicode.com/posts", params=params)

print("Final URL:", response.url)
print("Number of posts:", len(response.json()))
print("First post title:", response.json()[0]["title"])
```

Output —
```
Final URL: https://jsonplaceholder.typicode.com/posts?userId=1
Number of posts: 10
First post title: sunt aut facere repellat provident occaecati excepturi optio reprehenderit
```

Passing a dictionary to `params=` builds the `?userId=1` query string automatically — no manual string concatenation, no worrying about escaping special characters. `requests` handles all of that.

---

## Final curl Check

```bash
curl -o /dev/null -s -w "%{http_code}\n" https://jsonplaceholder.typicode.com/posts/1
# 200

curl -o /dev/null -s -w "%{http_code}\n" https://jsonplaceholder.typicode.com/posts/9999
# 404
```

Clean, consistent results — confirming jsonplaceholder is a more dependable API to practice against than httpbin was today.

---

## The Real Lesson Today

No actual bugs in the Python code itself — every script was syntactically correct from the start. The entire day's friction came from an external dependency (httpbin.org) being unreliable. That's not a coding mistake, but it's an extremely common real-world situation: **the code can be perfect and a request can still fail because of something entirely outside your control.**

This is exactly why `response.status_code`, `response.ok`, and proper `try/except` around `.json()` matter in real production code — not as defensive paranoia, but because servers genuinely do go down, get overloaded, or return unexpected content. A model serving API needs to handle that exact scenario gracefully instead of crashing with an unhandled `JSONDecodeError`.

---

## What to Remember

| Concept | What it means |
|---|---|
| Request | method + URL + headers + body, sent by client |
| Response | status code + headers + body, sent by server |
| `response.status_code` | the actual numeric code |
| `response.ok` | quick True/False for any 2xx |
| `response.json()` | parses body as JSON — crashes if body isn't valid JSON |
| `response.headers` | metadata, including `Content-Type` which hints at what `.json()` will do |
| `params=` | builds query string automatically from a dict |
| 503 | server overloaded/unavailable — not a client-side bug |
| 404 | resource doesn't exist |

---

*Day 21 done. Topic 04 — HTTP and APIs — underway.*