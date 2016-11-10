import subprocess
import signal


def popen(cmd):
    """
    Run cmd by subprocess.

    :param cmd:
    :return:
    """
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def handle_signal(signalnum, frame):
        child.send_signal(signalnum)
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    child.wait()
    return child.communicate()

