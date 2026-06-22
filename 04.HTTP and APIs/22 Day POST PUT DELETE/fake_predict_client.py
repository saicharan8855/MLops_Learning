import requests

def send_prediction_request(feature: list) -> dict:
	payload = {
		"title" : "iris_prediction_request",
		"body" : str(feature),
		"userId" : 1
	}

	response = requests.post(
		"https://jsonplaceholder.typicode.com/posts",
		json=payload
	)

	if response.status_code == 201:
		return {"status" : "success", "data": response.json()}
	else:
		return {"status" : "failed", "code": response.status_code}

test_cases =[
	[5.1,3.5,1.4,0.2],
	[6.2,2.9,4.3,1.3],
	[7.3,3.0,6.3,1.8]
]

for features in test_cases:
	result = send_prediction_request(features)
	print(f"features {features} -> {result}")
