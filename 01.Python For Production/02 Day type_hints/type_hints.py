# type hints for python 

def add_numbers(a:int, b : int) -> int:
    return a + b

def greet_user(name:str) -> str:
    return f"Hello {name}!"

def is_valid(age: int) -> bool:
    return age > 0

print(add_numbers(5,10))
print(greet_user("saicharan"))
print(is_valid(20))

# === collection types ===
from typing import List , Dict , Tuple

def get_features(data: List[float]) -> int:
    return len(data)

def get_model_info(model: str , version: float) -> Dict[str , str]:
    return {
        "model" : model ,
        "version" : str(version)
    }

def get_min_max(data : List[float]) -> Tuple[float , float]:
    return min(data) , max(data)

print(get_features([1.0 , 2.0 , 3.5 , 4.0]))
print(get_model_info("iris" , 1.0))
print(get_min_max([1.0 , 2.0 , 3.0 , 4.0 , 5.0]))


# === optonal types ===

from typing import Optional

def label(prediction: int) -> Optional[str]:
    labels = {0: "cat" , 1: " dog" , 2: " rabbit"}
    return labels.get(prediction)

print(label(1))
print(label(5))


# === Doc strings with type hints ===

def predict_iris(features : List[float]) -> Dict[str , str]:
    """"
    Predict the iris species based on the input data
    Args:
        data (float): The input data for prediction
    Returns:
        Dict[str , str]: A dictionary containing the predicted species
    """
    if len(features) != 4:
        raise ValueError(f"expected 4 features but got {len(features)}")
    
    return {
        "Prdiction" : "setosa" , 
        "status" : "success"
    }

print(predict_iris([5.1 , 3.5 , 1.4 , 0.2]))


# === Union types ===

from typing import Union

def process_age(age: Union[int , str , float]) -> str:
    return str(age)


def process_data(data: Union[float ,str]) -> str:
    return str(data)

print(process_age(20))
print(process_data(3.14))


# === List of Dicts ===

def batch_predict(data: List[Dict[str , float]]) -> List[str]:
    """
    Predict for multiple samples at once

    Args:
        samples: List of feature dictionaries
    Returns:
        List of predicted labels
    """
    result = []
    for sample in data:
        result.append("setosa")
    return result 

samples = [
    {"sepal_length": 5.1, "sepal_width": 3.5},
    {"sepal_length": 6.2, "sepal_width": 2.9},
]
print(batch_predict(samples))


# === default values with type hints ===

def create_expeirment(
        name: str,
        version: float = 1.0,
        debug: bool = False,
    ) -> Dict[str, Union[str, float, bool]]:
    
    return {
        "name" : name,
        "version" : version,
        "bebug" : debug
    }
print(create_expeirment("iris"))
print(create_expeirment("iris" , version=2.0 , debug=True))


# === type hints for loops ===

def filter_valid_features(all_samples: List[Union[float , str]] , expected_length: int) -> List[float]:
    valid_features = []
    for sample in all_samples:
        if len(sample) == expected_length:
            valid_features.append(sample)
    return valid_features

samples = [
    [5.1 , 3.5 , 1.4 , 0.2],
    [6.2 , 2.9 , 4.3],
    [7.0 , 3.2 , 4.7 , 1.4]
]

print(filter_valid_features(samples , expected_length=4))


# === nested dicts return type ===

from typing import Any

def get_model_results(
        model_name: str,
        accuracy: float,
        features: List[str]
) -> Dict[str , Any]:
    
    return {
        "model_name" : model_name,
        "metrics" : {
            "accuracy" : accuracy,
            "features_count" : len(features)
        },
        "features" : features,
        "status" : "ready" if accuracy > 0.8 else "needs improvement"
    }

print(get_model_results(
    model_name="iris-classifier",
    accuracy=0.95,
    features=["sepal_length", "sepal_width", "petal_length", "petal_width"]
))