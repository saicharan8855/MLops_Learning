import logging 

# basic conofiguration for logging 
logging.basicConfig(
    level = logging.DEBUG,
    format = "%(asctime)s - %(levelname)s - %(message)s"
)

logging.debug("this is a debug message")
logging.info("this is an info message")
logging.warning("this is a warning message")
logging.error("this is an error message")
logging.critical("this is a critical message")


# logging levels 
# change level to WARNING and runagain

logging.basicConfig(
    level = logging.WARNING,
    format = "%(asctime)s - %(levelname)s - %(message)s"
)

logging.debug("you wont see this")
logging.info("you wont see this either")
logging.warning("you will see this ")
logging.error("you will see this ")
logging.critical("you will see this")


# named loggers 

logger = logging.getLogger("iris_model")

logging.basicConfig(
    level = logging.DEBUG,
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger.info("model logger started")
logger.debug("loading features")
logger.warning("feature count is low")
logger.error("prediction failed")


# log to a file 

import logging 
logging.basicConfig(
    level = logging.DEBUG,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    handlers = [
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)


logger = logging.getLogger("iris_model")

logger.info("application started")
logger.debug("loading features")
logger.warning("feature count is low")
logger.error("prediction failed")


# logging insisde a function 


import logging 
from typing import List , Dict , Any 

logging.basicConfig(
    level = logging.DEBUG,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    handlers = [
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger("iris_pipeline")

def validate_feature(features: List[float]) -> bool:
    logger.debug(f"validating features: {features}")

    if len(features) != 4:
        logger.error(f"invalid feature count : {len(features)}")
        raise ValueError(f"expected 4 feaatures but got {len(features)}") 
    
    logger.info("features are valid")
    return True 

def predict(features: List[float]) -> Dict[str , Any]:
    logger.info(f"starting prediction for feratures: {features}")

    try:
        validate_feature(features)
        label = "setosa" if features[0] < 5.0 else "versicolor"
        logger.info(f"prediction complete: {label}")
        return {"prediction": label , "status" : "success"}
    except ValueError as e:
        logger.error(f"prediction failed: {e}")
        return {"prediction": None , "status" : "failed" , "error":str(e)}
    

print(predict([5.1, 3.5, 1.4, 0.2]))  
print(predict([5.1, 3.5]))  


#  log levels from cconfig 


import logging 
import os 

LOG_LEVEL = os.environ.get("LOG_LEVEL" , "INFO")

logging.basicConfig(
    level = getattr(logging , LOG_LEVEL.upper())
)

logger = logging.getLogger("iris_app")

logger.debug("debug only shows if LOG_LEVEL = DEBUG")
logger.debug("app is running")
logger.warning("something to watchhj")