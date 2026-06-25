from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()
API_KEY = os.getenv("API_KEY", "fallback-key-123")

BASE_URL = "https://jsonplaceholder.typicode.com"


def safe_request(method: str, endpoint: str, payload: dict = None, timeout: int = 5) -> dict:
    """
    A single function that handles GET/POST/PUT/DELETE,
    auth headers, timeouts, and errors - all in one place.
    """
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.request(
            method, url, headers=headers, json=payload, timeout=timeout
        )
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


# simulate a full model lifecycle
print("--- Listing 'models' (using /users as stand-in resource) ---")
print(safe_request("GET", "/users/1"))

print("")
print("--- Creating a 'prediction' ---")
result = safe_request("POST", "/posts", payload={
    "title": "iris_prediction",
    "body": json.dumps({"prediction": "setosa", "confidence": 0.97}),
    "userId": 1
})
print(result)

print("")
print("--- Updating a 'model' ---")
print(safe_request("PUT", "/posts/1", payload={
    "id": 1, "title": "iris-classifier-v2", "body": "updated", "userId": 1
}))

print("")
print("--- Deleting a 'model' ---")
print(safe_request("DELETE", "/posts/1"))

print("")
print("--- Requesting something that doesn't exist ---")
print(safe_request("GET", "/posts/999999"))
