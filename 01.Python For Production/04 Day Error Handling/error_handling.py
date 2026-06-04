# --- basic error handling  ---

def divide(a: int , b: int) -> float:
    try:
        result = a/b
        return result
    except ZeroDivisionError:
        print("error : cannot divide by zero")
        return 0.0
print("-"*10)
print("1." , divide(10,5))
print("2." , divide(10,0))
print("-"*10)


# --- multiple except blocks ---

def parse_feature(feature: str) -> float:
    try:
        value = float(feature)
        return value
    except ValueError:
        print(f"error : cannot convert {feature} to float")
        return 0.0
    except TypeError:
        print(f"error : feature must be a string or integer , got {type(feature)}")
        return 0.0
    
print("-"*10)
print("3." , parse_feature("3.14"))
print("4." , parse_feature("abc"))
print("5." , parse_feature(None))
print("-"*10)



# --- raising own errors ---


from typing import List

def validate_features(features: List[float]) -> bool:
    if not isinstance(features , list):
        raise TypeError(f"features must be a list , got {type(features).__name__}")
    
    if len(features) != 4:
        raise ValueError(f"features must contain 4 elements , got {len(features)}")
    
    if not all(isinstance(f , (int , float)) for f in features):
        raise TypeError("All features must be numeric")
    return True

print("-"*10)
try:
    validate_features([5.0,3.0,1.0,2.0])
    print("6. valid features")
except (TypeError , ValueError) as e:
    print("6. validation error:" , e)

try:
    validate_features([5.0,2.0])
    print("7. valid features")
except (TypeError , ValueError) as e:
    print("7. validation error:" , e)

try:
    validate_features([1.0,"abc",3.0,4.0])
    print("valid features")
except (TypeError , ValueError) as e:
    print("8. validation error:" , e)
print("-"*10)



# --- "finally" block ---

def load_file(path: str) -> str:
    file =  None
    try:
        file = open(path , "r") 
        content =  file.read()
        return content
    except FileNotFoundError:
        print(f"9. error : file {path} not found")
        return ""
    finally:
        if file:
            file.close()
            print(f"9. closed file {path}")

print("-"*10)
print(load_file("abcdef.csv"))  # file doesnt exist
print("-"*10)



# --- custom exception classes --- 


print("-"*10)
class InvalidFeaturesError(Exception):
    "raised when iris features are invalid"
    pass 
class ModelNotFoundError(Exception):
    "raised when a model file is not found"
    pass 

def predict(features: List[float]) -> str:
    if len(features) != 4:
        raise InvalidFeaturesError(
            f"features must contain 4 elements , got {len(features)}"
        )
    return "setosa"

def load_model(path: str) -> str:
    import os
    if not os.path.exists(path):
        raise ModelNotFoundError(f"11. model file {path} not found")
    return "model loaded"

try:
    predict([5.0,3.0])
    print("10. prediction successful")
except InvalidFeaturesError as e:    
    print("10. prediction error:" , e) 

try:
    load_model("abcd.pkl")
    print("11. model loaded successfully")
except ModelNotFoundError as e:
    print("11. model loading error:" , e)
print("-"*10)
    



