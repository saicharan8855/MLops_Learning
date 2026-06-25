import requests

def safe_get(url: str, headers: dict = None, timeout: int = 5) -> dict:
    """
    A production-style wrapper around requests.get that never crashes
    the caller, no matter what goes wrong.
    """
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # raises an exception for 4xx/5xx
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


# test it against several scenarios
print(safe_get("https://jsonplaceholder.typicode.com/posts/1"))
print(safe_get("https://jsonplaceholder.typicode.com/posts/99999"))
print(safe_get("https://httpbin.org/delay/10", timeout=2))
print(safe_get("https://this-domain-does-not-exist-12345.com"))
