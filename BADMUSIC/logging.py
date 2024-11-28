# Copyright (C) 2024 by Badhacker98@Github, < https://github.com/Badhacker98 >.
# Owner https://t.me/ll_BAD_MUNDA_ll

import logging
from pymongo import MongoClient
import time
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from logging.handlers import RotatingFileHandler

from config import LOG_FILE_NAME
import config 

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=5000000, backupCount=10),
        logging.StreamHandler(),
    ],
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGGERR = logging.getLogger(__name__)
boot = time.time()
mongodb = MongoCli(config.MONGO_DB_URI)
db = mongodb.Anonymous
mongo = MongoClient(config.MONGO_DB_URI)
OWNER = config.OWNER_ID
logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
logging.getLogger("pymongo").setLevel(logging.ERROR)
logging.getLogger("ntgcalls").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.basicConfig(level=logging.DEBUG)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
