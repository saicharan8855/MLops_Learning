from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_KEY = os.getenv("API_KEY")

def send_prediction_request(features: list) -> dict:
	headers = {
		"Authorization" : f"bearer {API_KEY}",
		"content-type" : "application/json"
	}
	payload = {
		"title": "iris_prediction_request",
		"body": str(features),
		"userid": 1
	}

	response = requests.post(
		"https://jsonplaceholder.typicode.com/posts",
		json = payload,
		headers= headers
	)

	if response.status_code == 201:
		return {"status": "success", "data": response.json()}
	else:
		return{"status": "failed", "code": response.status_code}

test_cases = [
	[5.1,3.5,1.4,0.2],
	[6.2,2.9,4.3,1.3],
]

for features in test_cases:
	result = send_prediction_request(features)
	print(f"features {features} -> {result}")

