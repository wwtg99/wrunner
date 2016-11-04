from celery import Celery
import runner_config
import logging
from logging.handlers import TimedRotatingFileHandler


# logging
logfile = 'worker.log'
if 'LOGGER_FILE' in dir(runner_config):
    logfile = runner_config.LOGGER_FILE
loginterval = 1
if 'LOGGER_INTERVAL' in dir(runner_config):
    loginterval = runner_config.LOGGER_INTERVAL
logwhen = 'D'
if 'LOGGER_WHEN' in dir(runner_config):
    logwhen = runner_config.LOGGER_WHEN
lognum = 5
if 'LOGGER_MAX_COUNT' in dir(runner_config):
    lognum = runner_config.LOGGER_MAX_COUNT
logfor = '[%(levelname)s][%(asctime)s] %(message)s'
if 'LOGGER_FORMATTER' in dir(runner_config):
    logfor = runner_config.LOGGER_FORMATTER
handler = TimedRotatingFileHandler(logfile, interval=loginterval, when=logwhen, backupCount=lognum)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(logfor)
handler.setFormatter(formatter)
logger = logging.getLogger('main')
logger.addHandler(handler)

# celery config
if 'BROKER' in dir(runner_config):
    broker = runner_config.BROKER
else:
    broker = None
if 'BACKEND' in dir(runner_config):
    backend = runner_config.BACKEND
else:
    backend = None

app = Celery('tasks', broker=broker, backend=backend)

import tasks
