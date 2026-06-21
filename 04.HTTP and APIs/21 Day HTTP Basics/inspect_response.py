import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

print("Status code:", response.status_code)
print("OK?:", response.ok)
print("URL:", response.url)
print("")
print("All headers:")
for key, value in response.headers.items():
    print(f"  {key}: {value}")
print("")
print("JSON body:")
print(response.json())
