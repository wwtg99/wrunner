from datetime import timedelta

BROKER_URL = 'redis://localhost:6379/3'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/3'

CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True

CELERYBEAT_SCHEDULE = {
    'pg_dump': {
        'task': 'tasks.backup_pgsql',
        'schedule': timedelta(seconds=60),
        'args': (dict(dbname='test1', output='pgsql-{datetime}.sql'), )
    },
    'mysql_dump': {
        'task': 'tasks.backup_mysql',
        'schedule': timedelta(seconds=20),
        'args': (dict(database='test', output='mysql-{datetime}.sql'), )
    }
}
