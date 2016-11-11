from celery import Celery
import runner_config


taskname = 'tasks'
if 'CELERY_NAME' in dir(runner_config):
    taskname = runner_config.CELERY_NAME
celeryconf = 'celeryconfig'
if 'CELERY_CONFIG_MODULE' in dir(runner_config):
    celeryconf = runner_config.CELERY_CONFIG_MODULE

app = Celery(taskname)
app.config_from_object(celeryconf)

import tasks
