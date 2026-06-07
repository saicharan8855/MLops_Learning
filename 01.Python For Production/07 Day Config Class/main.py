import logging
from typing import List, Dict , Any
from config import load_config 

config = load_config()

logging.basicConfig(
    level = getattr(logging , config.log_level.upper()),
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(config.app_name)

def predict(features: List[float]) -> Dict[str , Any]:
    logger.info(f"Predicting for features: {features}")

    if len(features) != 4:
        logger.error(f"Invalid features: {len(features)}")
        return {"prediction": None, "status": "failed"}
    
    label = "setosa" if features[0] < 5.5 else "versicolor"
    logger.info(f"prediction:" {label}) 

    return {
        "prediction": label,
        "model_version" : config.model_version,
        "model_path": config.model_path,
        "status": "success"
    }

print(predict([5.1,3.5,1.4,0.2]))
print(predict([6.0,3.0,4.8,1.8]))