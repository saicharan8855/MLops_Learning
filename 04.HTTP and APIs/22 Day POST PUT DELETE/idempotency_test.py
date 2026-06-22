import requests

# DELETE the same resource 3 times
for i in range(3):
    response = requests.delete(
        "https://jsonplaceholder.typicode.com/posts/1"
    )
    print(f"Attempt {i+1} → Status: {response.status_code}")
