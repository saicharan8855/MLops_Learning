""" import logging 

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
logger.error("prediction failed") """


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