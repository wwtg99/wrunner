import argparse
import runner_config
import json
import os


def parse_args():
    parser = argparse.ArgumentParser(prog='wwu_runner', description='Job runner based on celery')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1.0')
    parser.add_argument('mode', help='Work mode', choices=['worker', 'inspect', 'task'])
    parser.add_argument('action', help='Mode action', nargs='*')
    parser.add_argument('--workdir', help='Work directory')
    parser.add_argument('--celery-config', help='Name of celery config module.')
    parser.add_argument('--loglevel', help='Logging level for celery.', choices=['DEBUG', 'INFO', 'ERROR', 'CRITICAL', 'FATAL'])
    parser.add_argument('--logfile', help='Path to log file for celery. If no logfile is specified, stderr is used.')
    parser.add_argument('-p', '--param', help='Task param for task mode only.')
    parser.add_argument('--param-type', help='Task param type.', default='string')
    return parser.parse_args()


def worker_mode(argument):
    celery_bin = runner_config.CELERY_BIN
    cmd = [celery_bin, 'worker', '-A celery_app']
    if argument.celery_config:
        cmd.append('--config=%s' % argument.celery_config)
    if argument.loglevel:
        cmd.append('--loglevel=%s' % argument.loglevel)
    if argument.logfile:
        cmd.append('--logfile=%s' % argument.logfile)
    c = ' '.join(cmd)
    # print(c)
    os.system(c)
    return 0


def inspect_mode(argument):
    celery_bin = runner_config.CELERY_BIN
    cmd = [celery_bin, '-A celery_app', 'inspect']
    if argument.action:
        cmd.append(argument.action[0])
    if argument.celery_config:
        cmd.append('--config=%s' % argument.celery_config)
    c = ' '.join(cmd)
    # print(c)
    os.system(c)
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
        print('Run task %s' % func)
        print('Use module %s' % modu)
        print('Use function %s' % func)
        f.delay(p)
    return 0


if __name__ == '__main__':
    args = parse_args()
    if args.workdir:
        os.chdir(args.workdir)
    if args.mode == 'worker':
        re = worker_mode(args)
    elif args.mode == 'inspect':
        re = inspect_mode(args)
    elif args.mode == 'task':
        re = task_mode(args)
    else:
        re = 0
    exit(re)
