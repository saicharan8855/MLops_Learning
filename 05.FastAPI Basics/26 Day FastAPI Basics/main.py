from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
	return {"message" : "iris Mlops API is running"}

@app.get("/models/{model_name}")
def get_model(model_name: str):
	return {"model_name": model_name, "status": "active"}

@app.get("/predict")
def predict(feature1: float, feature2: float, feature3: float, feature4: float):
    return {
        "input": [feature1, feature2, feature3, feature4],
        "prediction": "setosa"
    }
