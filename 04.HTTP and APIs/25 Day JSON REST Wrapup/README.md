# 04. HTTP and APIs — Summary

## Days Covered
| Day | Topic |
|---|---|
| 21 | Request/response basics, status codes, requests library |
| 22 | POST, PUT, DELETE, idempotency |
| 23 | API authentication — Bearer tokens, API keys, .env |
| 24 | Timeouts, retries, exponential backoff, error handling |
| 25 | JSON deep dive, REST design, final combined client |

## Key Concepts Mastered
- Request = method + URL + headers + body
- Response = status code + headers + body
- Status code families: 2xx success, 4xx client error, 5xx server error
- POST creates (not idempotent), PUT/DELETE are idempotent
- Bearer tokens via Authorization header, secrets via .env
- timeout= prevents hanging forever, retries need backoff
- JSON: objects for single things, arrays for lists, nested structure for real responses
- REST: URLs are nouns (resources), HTTP methods are verbs (actions)

## Biggest Lessons
- External APIs fail in real, unpredictable ways (httpbin taught this all week)
- Never trust response.json() without checking status first
- Wrap every API call in try/except with specific exception types
- Never hardcode secrets — always .env + .gitignore

## What's Next
Topic 05 — FastAPI Basics
