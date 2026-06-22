import requests

response = requests.delete(
	"https://jsonplaceholder.typicode.com/posts/1"
)

print("status code :", response.status_code)
print("body :"  ,response.text)

