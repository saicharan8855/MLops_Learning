import pickle
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

app = FastAPI()

# --- Load model ONCE when the server starts, not per-request ---
try:
    with open("iris_model.pkl", "rb") as f:
        model = pickle.load(f)
    print("Model loaded successfully")
except FileNotFoundError:
    model = None
    print("WARNING: Model file not found - server starting without it")


labels = {0: "setosa", 1: "versicolor", 2: "virginica"}


class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

    @field_validator("sepal_length", "sepal_width", "petal_length", "petal_width")
    @classmethod
    def must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Feature values must be positive")
        return value


class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    status: str


@app.get("/")
def home():
    return {"message": "Iris MLOps API is running", "model_loaded": model is not None}


@app.get("/health")
def health_check():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionResponse)
def predict(features: IrisFeatures):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not available")

    try:
        input_data = [[
            features.sepal_length,
            features.sepal_width,
            features.petal_length,
            features.petal_width
        ]]

        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]
        confidence = round(float(max(probabilities)), 4)

        return PredictionResponse(
            prediction=labels[prediction],
            confidence=confidence,
            status="success"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
