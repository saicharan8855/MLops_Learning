import requests

updated_post = {
	"id" : 1,
	"title" : "iris prediction - updated",
	"body" : "model re-predicted versicolor with 0.88 confidence",
	"userId" : 1
}


response = requests.put(
	"https://jsonplaceholder.typicode.com/posts/1",
	json=updated_post
)

print("status code :", response.status_code)
print("updated resource :", response.json())
