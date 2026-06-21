import requests

response = requests.get("https://httpbin.org/get")
print("Status code:", response.status_code)

if response.status_code == 200:
    print("Headers:", response.headers["Content-Type"])
    print("Body:", response.json())
else:
    print(f"Request failed with status {response.status_code}")
    print("Response text:", response.text[:200])
