import requests

urls = [
    "https://jsonplaceholder.typicode.com/posts/1",   # exists - 200
    "https://jsonplaceholder.typicode.com/posts/9999", # doesn't exist - 404
]

for url in urls:
    response = requests.get(url)
    
    if response.status_code == 200:
        print(f"{url} → Success")
    elif response.status_code == 404:
        print(f"{url} → Not Found")
    elif response.status_code >= 500:
        print(f"{url} → Server Error")
    else:
        print(f"{url} → Status: {response.status_code}")
