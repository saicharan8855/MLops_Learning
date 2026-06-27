import requests

payload = {
    "sepal_length": 6.2,
    "sepal_width": 2.9,
    "petal_length": 4.3,
    "petal_width": 1.3
}

response = requests.post("http://127.0.0.1:8000/predict", json=payload)
print("Status code:", response.status_code)
print("Response:", response.json())

