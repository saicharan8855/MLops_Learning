import requests

def unsafe_retry_post(url, payload, max_retries=3):
    """
    DON'T do this in real life without an idempotency key.
    This demonstrates the danger, not the solution.
    """
    for attempt in range(1, max_retries + 1):
        response = requests.post(url, json=payload)
        print(f"Attempt {attempt}: Created resource with id {response.json().get('id')}")

payload = {"title": "iris_prediction", "userId": 1}
unsafe_retry_post("https://jsonplaceholder.typicode.com/posts", payload)
