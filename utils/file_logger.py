import sys

orig_stdout = sys.stdout
orig_stderr = sys.stderr
logfile = None
errfile = None

# important to log to file while script is still running
buffer_size = 10


def init(name):
    global logfile, errfile

    log_filename = 'logs/%s__logs.txt' % (name)
    err_filename = 'logs/%s__err.txt' % (name)
    logfile = file(log_filename, 'w', buffer_size)
    errfile = file(err_filename, 'w', buffer_size)
    sys.stdout = logfile
    sys.stderr = errfile


def close():
    sys.stdout = orig_stdout
    sys.stderr = orig_stderr
    logfile.close()
    errfile.close()
