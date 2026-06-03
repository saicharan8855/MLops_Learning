from typing import List , Dict
from iris_package.utils import validate_features , get_label 

def predict(features: List[float]) -> Dict[str , str]:
    if features[0] < 5.5:
        label = get_label(0)
    elif features[0] < 6.5:
        label = get_label(1)
    else:
        label = get_label(2)

    return {
        "prediction": label,
        "status": "success"
    }