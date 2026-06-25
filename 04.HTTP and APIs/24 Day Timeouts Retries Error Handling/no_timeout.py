import requests

print("sending request with no timeout set...")
response = requests.get("https://httpbin.org/delay/3")
print("status code:",response.status_code)
print("This took a while because nothing stopped it from waiting")

