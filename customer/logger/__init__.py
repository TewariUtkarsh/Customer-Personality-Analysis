import logging
from customer.constants import *


def get_log_filename() -> str:
    """
    This function returns the Log File Name.

    Returns
    -------
    log_filename : str
        Log File Name
    """
        
    log_filename = f"log_{get_current_timestamp()}.log"
    return log_filename


os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_NAME = get_log_filename()
LOG_FILE_PATH = os.path.join(
    LOG_DIR,
    LOG_FILE_NAME
)



logging.basicConfig(
    filename= LOG_FILE_PATH,
    filemode='w',
    format='[%(asctime)s]^;%(levelname)s^;%(lineno)d^;%(filename)s^;%(funcName)s()^;%(message)s',
    level=logging.INFO
)
