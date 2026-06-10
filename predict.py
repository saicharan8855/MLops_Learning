import pickle 
from typing import List , Dict , Any

with open(r"C:\Users\sai charan\OneDrive\Desktop\MLops Learning Grind\01.Python For Production\09 Day Iris Model\model\iris_model.pkl", "rb") as f:
    model = pickle.load(f) 

print("model loaded successfully") 

labels = {0:"setosa" , 1:"versicolor",2:"virginica"}

def predict(features: List[float]) -> Dict[str,Any]:

    if len(features) !=4:
        raise ValueError(f"expected 4 but got {len(features)}")
    
    prediction = model.predict([features])[0]
    probabilities = model.predict_proba([features])[0]
    confidence = round(float(max(probabilities)) , 4)

    return {
        "predicted_label": labels[prediction],
        "confidence": confidence,  
        "status" : "success"
    }


print(predict([5.1, 3.5, 1.4, 0.2]))  
print(predict([6.2, 2.9, 4.3, 1.3]))   
print(predict([7.3, 3.0, 6.3, 1.8]))