from celery_app import app
from celery_app import logger
import time
import os


@app.task
def sendmail(mail):
    print('sending mail to %s...' % mail['to'])
    time.sleep(2.0)
    print('mail sent.')
    return 'return from ' + mail['to']


@app.task
def cmd(args):
    c = None
    if isinstance(args, str):
        c = args
    else:
        if 'cmd' in args:
            c = args['cmd']
    res = ''
    if c:
        print('run command %s' % c)
        logger.info('run command %s' % c)
        f = os.popen(c)
        res = f.read()
        logger.info(res)
    return res
