# celery config
CELERY_BIN = 'celery'
CELERY_NAME = 'tasks'
CELERY_CONFIG = 'celeryconfig'
# log
LOGGER_FILE = 'worker.log'
LOGGER_MAX_COUNT = 5
LOGGER_INTERVAL = 1
LOGGER_WHEN = 'D'
LOGGER_FORMATTER = '[%(levelname)s][%(asctime)s] %(message)s'
