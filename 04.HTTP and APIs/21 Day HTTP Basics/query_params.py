import requests

params = {
    "userId": 1
}

response = requests.get("https://jsonplaceholder.typicode.com/posts", params=params)
print("Final URL:", response.url)
print("Number of posts:", len(response.json()))
print("First post title:", response.json()[0]["title"])
