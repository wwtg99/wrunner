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

taskname = 'tasks'
if 'CELERY_NAME' in dir(runner_config):
    taskname = runner_config.CELERY_NAME
celeryconf = 'celeryconfig'
if 'CELERY_CONFIG' in dir(runner_config):
    celeryconf = runner_config.CELERY_CONFIG

app = Celery(taskname)
app.config_from_object(celeryconf)

import tasks
