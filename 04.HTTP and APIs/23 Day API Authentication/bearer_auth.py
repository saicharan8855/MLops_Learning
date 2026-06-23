import requests

token = "my-secret-token-123"

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get("https://httpbin.org/bearer", headers=headers)
print("Status code:", response.status_code)
print("Body:", response.json())
