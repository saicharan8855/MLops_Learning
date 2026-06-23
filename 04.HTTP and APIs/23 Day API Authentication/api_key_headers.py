import requests

headers = {
	"X-API-Key": "my-api-key-456"
}

response = requests.get("https://httpbin.org/headers", headers = headers)
print("status code", response.status_code)
print("what the seerver received:")
print(response.json())

