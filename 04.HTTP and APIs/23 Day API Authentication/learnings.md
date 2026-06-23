# Day 23 — API Authentication: API Keys and Bearer Tokens

Today's focus was authentication — how a server knows whether a request is allowed to do what it's asking. Worked through the failure case first (no auth), then the correct Bearer token pattern, then tied it back to `.env` from Topic 01 so the secret never lives directly in code. Plenty of typos today, each one a small reminder that auth code is exactly the kind of code where a tiny mistake silently fails instead of crashing loud.

---

## Exercise 1 — No Auth (seeing the failure first)

First attempt had a typo in the URL itself —

```python
response = requests.get("httsps://httpbin.org/bearer")
```

```
requests.exceptions.InvalidSchema: No connection adapters were found for 'httsps://httpbin.org/bearer'
```

An extra `s` turned `https` into `httsps` — `requests` has no idea what protocol that's supposed to be, so it refuses outright before even trying to connect. Fixed the typo and ran again —

```
status code: 401
body :
```

Empty body, `401 Unauthorized`. This confirms what the ChatGPT prompt covered conceptually — no token means no access, and the server doesn't even bother sending content back, just the rejection.

---

## Exercise 2 — Bearer Token (the correct way)

Hit a small command typo first —

```bash
pytho3 bearer.py
# Command 'pytho3' not found
```

Two mistakes stacked — `pytho3` instead of `python3`, and `bearer.py` instead of the actual filename `bearer_auth.py`. Fixed the command, then —

```
python3 bearer.py
# can't open file 'bearer.py': No such file or directory
```

Ran the real filename —

```
status code : 401
JSONDecodeError: Expecting value...
```

Still `401` on this attempt — meaning the token wasn't actually being attached to the request correctly yet. Since the body was empty (401 pages have no JSON), calling `response.json()` crashed the same way it did back on Day 21 with httpbin's 503 pages. Same root cause every time: trying to parse a non-JSON body as JSON blows up.

Went back, fixed whatever was wrong with the header construction, ran again —

```
Status code: 200
Body: {'authenticated': True, 'token': 'my-secret-token-123'}
```

That's the Bearer pattern working correctly —

```python
headers = {
    "Authorization": f"Bearer {token}"
}
response = requests.get("https://httpbin.org/bearer", headers=headers)
```

`httpbin.org/bearer` specifically checks for this exact header format and echoes back confirmation that it recognized the token. The word "Bearer" in the header value isn't optional decoration — the server is literally checking for that prefix before reading whatever comes after it.

---

## Exercise 3 — Custom API Key Header

```python
headers = {"X-API-Key": "my-api-key-456"}
response = requests.get("https://httpbin.org/headers", headers=headers)
```

Ran clean on the first try —

```
status code 200
what the server received:
{'headers': {..., 'X-Api-Key': 'my-api-key-456'}}
```

`httpbin.org/headers` just echoes back every header it received, which is a genuinely useful way to confirm your custom header actually made it across the network exactly as intended — no typos in the header name, no missing value. Worth noting the server capitalized it as `X-Api-Key` in the echo even though it was sent as `X-API-Key` — HTTP header names are case-insensitive, so this is normal and not a bug.

---

## Exercise 4 — Moving the Key into .env

```bash
nano .env
# API_KEY=my-secret-token-123

pip install python-dotenv
```

First script attempt had a typo in the import call —

```python
laod_dotenv()
```

```
NameError: name 'laod_dotenv' is not defined. Did you mean: 'load_dotenv'?
```

Python's error message directly suggested the fix — fixed the typo, ran again —

```
status code 401
JSONDecodeError...
```

Still failing at this point — most likely the `.env` value wasn't being read correctly yet, or there was a mismatch between the key name in `.env` and what `os.getenv()` was looking for. Went back in, fixed it, ran a third time —

```
Status code: 200
Body: {'authenticated': True, 'token': 'my-secret-token-123'}
```

Same successful result as Exercise 2, but now the actual token value never appears anywhere in the Python file — it lives only in `.env`, which got added to `.gitignore` immediately after —

```bash
echo ".env" >> .gitignore
```

This connects directly back to Day 06 and Day 07. The whole reason that config pattern was worth learning early is exactly this moment — a real secret that must never end up on GitHub.

---

## Exercise 5 — Authenticated Predict Client

First run hit a syntax error —

```
File "authenticated_predict_client.py", line 21
    json = payload
SyntaxError: invalid syntax. Perhaps you forgot a comma?
```

Python's newer error messages are good at pointing toward missing commas — most likely the line just above this one (probably the URL or `headers=headers` argument) was missing its trailing comma, which made Python read the next argument as a malformed continuation of the previous line.

Fixed that, ran again, hit a different problem —

```python
from dotenv import lead_datenv
```

```
ImportError: cannot import name 'lead_datenv' from 'dotenv'. Did you mean: 'load_dotenv'?
```

A more mangled version of the same typo as Exercise 4 — `lead_datenv` instead of `load_dotenv`. Fixed it, ran a third time, and it finally worked —

```
features [5.1, 3.5, 1.4, 0.2] -> {'status': 'success', 'data': {'title': 'iris_prediction_request', 'body': '[5.1, 3.5, 1.4, 0.2]', 'userid': 1, 'id': 101}}
features [6.2, 2.9, 4.3, 1.3] -> {'status': 'success', 'data': {...}}
```

Both fake iris samples sent successfully, now with a real `Authorization: Bearer` header attached to each request. One small detail worth a second look — the response shows `'userid'` in lowercase rather than `'userId'` as originally written. Worth double checking the payload dict still has the key spelled exactly as intended, since case consistency matters once this talks to a real API with strict validation, even though jsonplaceholder doesn't care either way.

---

## Copying to the Repo

Hit the now-familiar missing-folder error —

```
cp: target '.../23 Day API Authentication/': No such file or directory
```

```bash
mkdir -p "/mnt/c/Users/sai charan/OneDrive/Desktop/MLops Learning Grind/04.HTTP and APIs/23 Day API Authentication"
```

Created the folder first, then the copy worked. `.env` was correctly left out of the copy — only the five `.py` files made it into the repo folder.

---

## Typos Made Today

| Typo | Should be |
|---|---|
| `httsps://` | `https://` |
| `pytho3` | `python3` |
| `bearer.py` | `bearer_auth.py` (wrong filename) |
| `bearrer_auth.py` | `bearer_auth.py` |
| `laod_dotenv()` | `load_dotenv()` |
| `lead_datenv` | `load_dotenv` |
| missing comma before `json = payload` | added trailing comma to previous argument |

Every error message pointed almost directly at the fix — Python and bash are unforgiving about exact spelling, but they're also very specific about exactly where they got confused.

---

## What to Remember

| Concept | What it means |
|---|---|
| `401 Unauthorized` | server understood the request but refused — missing/invalid credentials |
| `Authorization: Bearer <token>` | standard header format almost every API expects |
| Custom headers (`X-API-Key`) | some APIs use their own header name instead |
| `httpbin.org/headers` | echoes back received headers — useful to confirm what's actually sent |
| `.env` + `load_dotenv()` | keeps real secrets out of the codebase entirely |
| `.gitignore` the `.env` | never let a real key reach GitHub |

---

## Why This Matters in MLOps

Once a FastAPI model-serving endpoint exists, leaving it open to anyone is rarely the right call — especially if it costs compute per request or returns anything sensitive. The exact pattern practiced today — Bearer token in the `Authorization` header, real key stored in `.env`, client code attaching the header on every request — is precisely how a protected `/predict` endpoint gets called in production. Today's authenticated fake client is one small step away from the real thing.

---

*Day 23 done. HTTP and APIs topic continuing.*