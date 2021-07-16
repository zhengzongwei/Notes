# 日志记录相关问题

import logging
import os
LOG_LEVEL = logging.INFO
LOG_MODS = ["test"]
LOG_FILE = ''

def init_log():
    if not os.path.exists(LOG_FILE):
        log_dir = os.path.dirname(LOG_FILE)
        if not os.path.dirname(LOG_FILE):
            os.makedirs(log_dir)
        os.mknod(LOG_FILE, 0600)
        os.chmod(LOG_FILE, 0666)
    
    logger = logging.getLogger("mylog")
    handler = WatchedFileHandler(LOG_FILE)
    log_formatter = ""
    logging.Formatter = log_formatter
    logger.addHandler(handler)
    logger.setLevel(LOG_LEVEL)

    return logger

logger = init_log()

def log(msg,level="WARNING"):
    global logger
    level = level.upper()

    if level == "INFO":
        logger.info(msg)
    elif level == "DEBUG":
        logger.debug(msg)
    elif level == "WARNING":
        logger.warning(msg)
    elif level == "ERROR":
        logger.error(msg)
    elif level == "CRITICAL":
        logger.critical(msg)
    else:
        logger.warning(msg)



def blog(msg, level = "WARNING",mod="storage"):
    if mod not in LOG_MODS:
         pass
    dlog(msg, level, mod)



def dlog(msg, level = "WARNING", mod="storage"):
    if mod not in LOG_MODS:
        pass
    if not MongoWriteLog(msg, level, "DEVELOPER",mod):
        msg = "[DEVELOP] [%s] " % mod + msg
        log(msg,level)