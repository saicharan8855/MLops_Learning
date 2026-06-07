from dataclasses import dataclass 
from dotenv import load_dotenv
import os

load_dotenv() 

@dataclass
class AppConfig:
    app_name: str
    log_level: str
    model_path: str
    model_version: float
    debug_mode: bool 
    max_batch_size: int 

def load_config() -> AppConfig:
    return AppConfig(
        app_name=os.getenv("APP_NAME", "Default App"),
        log_level=os.getenv("LOG_LEVEL"),
        model_path=os.getenv("MODEL_PATH"),
        model_version=float(os.getenv("MODEL_VERSION", 1.0)),
        debug_mode=os.getenv("DEBUG_MODE", "False").lower() == "true",
        max_batch_size=int(os.getenv("MAX_BATCH", 32))
    ) 

config = load_config()
print(config)
print(f"App name: {config.app_name}")
print(f"Debug mode: {config.debug_mode}")
print(f"Max batch size: {config.model_version}")