import json

prediction_response = {
    "model": {
        "name": "iris-classifier",
        "version": "1.0"
    },
    "input": {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    },
    "result": {
        "prediction": "setosa",
        "confidence": 0.97,
        "probabilities": {
            "setosa": 0.97,
            "versicolor": 0.02,
            "virginica": 0.01
        }
    },
    "metadata": {
        "request_id": "abc-123",
        "timestamp": "2026-06-25T10:00:00Z"
    }
}

# accessing nested values
print("Prediction:", prediction_response["result"]["prediction"])
print("Confidence:", prediction_response["result"]["confidence"])
print("Setosa probability:", prediction_response["result"]["probabilities"]["setosa"])

# this is exactly what your FastAPI /predict endpoint will return later
print("")
print("Full response as JSON:")
print(json.dumps(prediction_response, indent=2))
