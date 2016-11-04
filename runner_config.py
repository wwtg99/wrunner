# celery config
CELERY_BIN = 'celery'
BROKER = 'redis://localhost:6379/3'
BACKEND = 'redis://localhost:6379/3'
# log
LOGGER_FILE = 'worker.log'
LOGGER_MAX_COUNT = 5
LOGGER_INTERVAL = 1
LOGGER_WHEN = 'D'
LOGGER_FORMATTER = '[%(levelname)s][%(asctime)s] %(message)s'
