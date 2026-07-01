import requests

batch_payload = {
    "samples": [
        {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
        {"sepal_length": 6.2, "sepal_width": 2.9, "petal_length": 4.3, "petal_width": 1.3},
        {"sepal_length": 7.3, "sepal_width": 3.0, "petal_length": 6.3, "petal_width": 1.8},
    ]
}

response = requests.post(
    "http://127.0.0.1:8000/predict/batch",
    json=batch_payload
)

print("Status:", response.status_code)
data = response.json()
print(f"Total predictions: {data['total']}")
for i, pred in enumerate(data["predictions"]):
    print(f"  Sample {i+1}: {pred['prediction']} (confidence: {pred['confidence']})")
