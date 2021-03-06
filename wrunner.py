#! /bin/python
import argparse
import runner_config
import json
import os
import utils


def parse_args():
    parser = argparse.ArgumentParser(prog='wwu_runner', description='Job runner based on celery')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1.0')
    parser.add_argument('mode', help='Work mode', choices=['worker', 'inspect', 'beat', 'task', 'log'])
    parser.add_argument('action', help='Mode action', nargs='*')
    parser.add_argument('--workdir', help='Work directory')
    parser.add_argument('--celery', help='Path of celery executable.')
    parser.add_argument('--celery-config', help='Name of celery config module.')
    parser.add_argument('--loglevel', help='Logging level for celery.', choices=['DEBUG', 'INFO', 'ERROR', 'CRITICAL', 'FATAL'])
    parser.add_argument('--logfile', help='Path to log file for celery. If no logfile is specified, stderr is used.')
    parser.add_argument('-B', '--beat', action="store_true", help='Also run the celery beat periodic task scheduler for worker mode.')
    parser.add_argument('-s', '--schedule', help='Schedule file for celery beat for beat mode.')
    parser.add_argument('-p', '--param', help='Task param for task mode only.')
    parser.add_argument('--param-type', help='Task param type, default string.', default='string')
    parser.add_argument('-f', '--follow', action="store_true", help='Follow log tail for log mode.')
    return parser.parse_args()


def worker_mode(argument):
    celery_bin = runner_config.CELERY_BIN
    c = [celery_bin, 'worker', '-A celery_app']
    if argument.celery_config:
        c.append('--config=%s' % argument.celery_config)
    if runner_config.LOGGER_LEVEL:
        c.append('--loglevel=%s' % runner_config.LOGGER_LEVEL)
    else:
        c.append('--loglevel=INFO')
    if runner_config.LOGGER_FILE:
        c.append('--logfile=%s' % runner_config.LOGGER_FILE)
    if argument.beat:
        c.append('--beat')
    c = ' '.join(c)
    utils.popen(c)
    return 0


def inspect_mode(argument):
    celery_bin = runner_config.CELERY_BIN
    c = [celery_bin, '-A celery_app', 'inspect']
    if argument.action:
        c.append(argument.action[0])
    if argument.celery_config:
        c.append('--config=%s' % argument.celery_config)
    c = ' '.join(c)
    os.system(c)
    return 0


def beat_mode(argument):
    celery_bin = runner_config.CELERY_BIN
    cmd = [celery_bin, 'beat', '-A celery_app']
    if argument.celery_config:
        cmd.append('--config=%s' % argument.celery_config)
    if runner_config.LOGGER_LEVEL:
        cmd.append('--loglevel=%s' % runner_config.LOGGER_LEVEL)
    if runner_config.LOGGER_FILE:
        cmd.append('--logfile=%s' % runner_config.LOGGER_FILE)
    if argument.schedule:
        cmd.append('--schedule=%s' % argument.schedule)
    c = ' '.join(cmd)
    utils.popen(c)
    return 0


def task_mode(argument):
    actions = argument.action
    if len(actions) == 1:
        modu = 'tasks'
        func = actions[0]
    elif len(actions) > 1:
        modu = actions[0]
        func = actions[1]
    else:
        print('No action provided!')
        return 0
    module = __import__(modu)
    f = getattr(module, func)
    p = argument.param
    ptype = argument.param_type
    if p and ptype == 'json':
        p = json.loads(p)
    if callable(f):
        print('Send task %s.%s' % (modu, func))
        print('Use params %s' % argument.param)
        f.delay(p)
    return 0


def log_mode(argument):
    logf = 'worker.log'
    if 'LOGGER_FILE' in dir(runner_config):
        logf = runner_config.LOGGER_FILE
    follow = False
    if argument.follow:
        follow = True
    if os.path.exists(logf):
        if follow:
            c = 'tail -f %s' % logf
            utils.popen(c)
        else:
            fh = open(logf)
            for l in fh:
                print(l)
            fh.close()
    else:
        print('Log file %s does not exists!' % logf)
    return 0


if __name__ == '__main__':
    args = parse_args()
    # global params
    if args.workdir:
        os.chdir(args.workdir)
    if args.logfile:
        runner_config.LOGGER_FILE = args.logfile
    if args.loglevel:
        runner_config.LOGGER_LEVEL = args.loglevel
    if args.celery:
        runner_config.CELERY_BIN = args.celery
    # mode
    if args.mode == 'worker':
        re = worker_mode(args)
    elif args.mode == 'inspect':
        re = inspect_mode(args)
    elif args.mode == 'beat':
        re = beat_mode(args)
    elif args.mode == 'task':
        re = task_mode(args)
    elif args.mode == 'log':
        re = log_mode(args)
    else:
        re = 0
    exit(re)
