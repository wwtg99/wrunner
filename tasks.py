from celery_app import app
from celery_app import logger
import time
import os
import datetime


@app.task
def sendmail(mail):
    print('sending mail to %s...' % mail['to'])
    time.sleep(2.0)
    print('mail sent.')
    return 'return from ' + mail['to']


@app.task
def cmd(args):
    """
    Run command.
    :param args: command
    :return:
    """
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


@app.task
def backup_pgsql(args):
    """
    Backup postgresql database by pg_dump.
    :param args:
    :return:
    """
    c = []
    dump_bin = args['pg_dump'] if 'pg_dump' in args else 'pg_dump'
    c.append(dump_bin)
    if 'output' in args:
        outf = args['output']
        if outf.find('{date}') >= 0:
            outf = outf.replace('{date}', datetime.datetime.now().strftime('%Y-%m-%d'))
        elif outf.find('{datetime}') >= 0:
            outf = outf.replace('{datetime}', datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S'))
        c.append('--file=%s' % outf)
    if 'format' in args:
        c.append('--format=%s' % args['format'])
    if 'jobs' in args:
        c.append('--jobs=%s' % args['jobs'])
    if 'data-only' in args:
        c.append('-a')
    if 'blobs' in args:
        c.append('-b')
    if 'clean' in args:
        c.append('-c')
    if 'create' in args:
        c.append('-C')
    if 'schema' in args:
        schema = args['schema']
        if isinstance(schema, list):
            for s in schema:
                c.append('--schema=%s' % s)
        else:
            c.append('--schema=%s' % schema)
    if 'exclude-schema' in args:
        nschema = args['exclude-schema']
        if isinstance(nschema, list):
            for s in nschema:
                c.append('--exclude-schema=%s' % s)
        else:
            c.append('--exclude-schema=%s' % nschema)
    if 'table' in args:
        tb = args['table']
        if isinstance(tb, list):
            for s in tb:
                c.append('--table=%s' % s)
        else:
            c.append('--table=%s' % tb)
    if 'exclude-table' in args:
        ntb = args['exclude-table']
        if isinstance(ntb, list):
            for s in ntb:
                c.append('--exclude-table=%s' % s)
        else:
            c.append('--exclude-table=%s' % ntb)
    if 'no-privileges' in args:
        c.append('-x')
    if 'host' in args:
        c.append('--host=%s' % args['host'])
    if 'port' in args:
        c.append('--port=%s' % args['port'])
    if 'username' in args:
        c.append('--username=%s' % args['username'])
    c.append('-w')  # no password
    dbname = args['dbname']
    c.append(dbname)
    c = ' '.join(c)
    print('Run command %s' % c)
    f = os.popen(c)
    res = f.read()
    return res


@app.task
def backup_mysql(args):
    """
    Backup mysql by mysqldump.
    :param args:
    :return:
    """
    c = []
    dump_bin = args['pg_dump'] if 'pg_dump' in args else 'mysqldump'
    c.append(dump_bin)
    if 'ignore-table' in args:
        ntb = args['ignore-table']
        if isinstance(ntb, list):
            for s in ntb:
                c.append('--ignore-table=%s' % s)
        else:
            c.append('--ignore-table=%s' % ntb)
    if 'host' in args:
        c.append('--host=%s' % args['host'])
    if 'port' in args:
        c.append('--port=%s' % args['port'])
    if 'user' in args:
        c.append('--user=%s' % args['user'])
    if 'database' in args:
        c.append(args['database'])
    else:
        c.append('--all-databases')
    if 'output' in args:
        outf = args['output']
        if outf.find('{date}') >= 0:
            outf = outf.replace('{date}', datetime.datetime.now().strftime('%Y-%m-%d'))
        elif outf.find('{datetime}') >= 0:
            outf = outf.replace('{datetime}', datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S'))
        c.append(' > %s' % outf)
    c = ' '.join(c)
    print('Run command %s' % c)
    f = os.popen(c)
    res = f.read()
    return res
