# -- read.env with python dot-env --

from dotenv import load_dotenv 
import os 

load_dotenv() 

APP_NAME = os.getenv("APP_NAME" , "Default App")
LOG_LEVEL = os.getenv("LOG_LEVEL" , "INFO")
MODEL_PATH = os.getenv("MODEL_PATH" , "models/model.pkl")
MODEL_VERSION = float(os.getenv("MODEL_VERSION" , "1.0"))
DEBUG_MODE = os.getenv("DEBUG_MODE" , False).lower() == "true"
MAX_BATCH_SIZE = int(os.getenv("MAX_BATCH_SIZE" , "16"))


print(f"app : {APP_NAME}")
print(f"Log Level : {LOG_LEVEL}")
print(f"Model Path : {MODEL_PATH}")
print(f"Model Version : {MODEL_VERSION}")
print(f"Max Batch size : {MAX_BATCH_SIZE}")

