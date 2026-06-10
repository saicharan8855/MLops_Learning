import pickle
import os
from typing import List, Dict, Any

model_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "09 Day Iris Model",
    "model",
    "iris_model.pkl"
)

with open(model_path, "rb") as f:
    model = pickle.load(f)

print("model loaded successfully")

labels = {0: "setosa", 1: "versicolor", 2: "virginica"}

def predict(features: List[float]) -> Dict[str, Any]:
    if len(features) != 4:
        raise ValueError(f"Expected 4 features, got {len(features)}")

    prediction = model.predict([features])[0]
    probabilities = model.predict_proba([features])[0]
    confidence = round(float(max(probabilities)), 4)

    return {
        "prediction": labels[prediction],
        "confidence": confidence,
        "status": "success"
    }

print(predict([5.1, 3.5, 1.4, 0.2]))
print(predict([6.2, 2.9, 4.3, 1.3]))
print(predict([7.3, 3.0, 6.3, 1.8]))