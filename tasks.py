from celery_app import app
import time
import datetime
import utils


@app.task
def sendmail(mail):
    """
    For test.
    :param mail:
    :return:
    """
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
        res = utils.popen(c)
        print(res)
    return res


@app.task
def backup_pgsql(args):
    """
    Backup postgresql database by pg_dump.

    dbname: database to dump, required
    pg_dump: path for pg_dump, optional
    output: output file, use {date} or {datetime} to represent current date or datetime, optional
    format: output format, optional
    jobs: job number, optional
    data-only: dump data only
    blobs: include large objects
    clean: drop database before recreating
    create: include commands to create database
    schema: dump named schemas only, string or list, optional
    exclude-schema: do not dump named schemas, string or list, optional
    table: dump named tables only, string or list, optional
    exclude-table: do not dump named tables, string or list, optional
    no-privileges: do not dump privileges
    host: database server host, optional
    port: database server port, optional
    username: database server username, optional
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
    res = utils.popen(c)
    return res


@app.task
def backup_mysql(args):
    """
    Backup mysql by mysqldump.

    mysqldump: path for mysqldump, optional
    ignore-table: do not dump the specified table, string or list, optional
    host: database server host, optional
    port: database server port, optional
    user: database server user, optional
    database: database to dump, all databases if not specified, optional
    output: output file, use {date} or {datetime} to represent current date or datetime, optional
    :param args:
    :return:
    """
    c = []
    dump_bin = args['mysqldump'] if 'mysqldump' in args else 'mysqldump'
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
    res = utils.popen(c)
    return res


@app.task
def export_docker(args):
    """
    Export docker container.

    container: container to export, required
    docker: path for docker, optional
    output: output file, use {date} or {datetime} to represent current date or datetime, optional
    :param args:
    :return:
    """
    c = []
    dump_bin = args['docker'] if 'docker' in args else 'docker'
    c.append(dump_bin)
    if 'output' in args:
        outf = args['output']
        if outf.find('{date}') >= 0:
            outf = outf.replace('{date}', datetime.datetime.now().strftime('%Y-%m-%d'))
        elif outf.find('{datetime}') >= 0:
            outf = outf.replace('{datetime}', datetime.datetime.now().strftime('%y-%m-%d-%H-%M-%S'))
        c.append('--output=%s' % outf)
    c.append(args['container'])
    c = ' '.join(c)
    print('Run command %s' % c)
    res = utils.popen(c)
    return res
