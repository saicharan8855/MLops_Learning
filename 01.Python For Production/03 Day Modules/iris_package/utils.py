from typing import List 

def validate_features(features: List[float]) -> bool:
    if len(features) != 4:
        raise ValueError(f"expected length is 4 but got {len(features)}")
    return True

def get_label(prediction: int) -> str:
    labels = {0: "setosa" , 1: "versicolor" , 2: "virginica"}
    return labels.get(prediction , "unknown")