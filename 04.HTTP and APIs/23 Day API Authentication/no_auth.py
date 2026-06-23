import requests
response = requests.get("https://httpbin.org/bearer")
print("status code:", response.status_code)
print("body : ", response.text)
