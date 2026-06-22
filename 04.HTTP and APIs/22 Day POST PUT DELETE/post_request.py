import requests
new_post = {
	"title" : "iris predictor",
	"body" : "model predicted setosa with 0.95 confidence",
	"userId" : 1
}

response = requests.post(
	"https://jsonplaceholder.typicode.com/posts",
	json=new_post
)

print("status code :", response.status_code)
print("created resources :", response.json())
