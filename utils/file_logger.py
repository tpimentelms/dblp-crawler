import sys
import logging

orig_stdout = sys.stdout
orig_stderr = sys.stderr
logfile = None
errfile = None

# important to log to file while script is still running
buffer_size = 10


def log_to_stdout():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def init_test(author):
    global logfile, errfile

    log_filename = 'results/%s__logs.txt' % (author)
    err_filename = 'results/%s__err.txt' % (author)
    logfile = file(log_filename, 'w', buffer_size)
    errfile = file(err_filename, 'w', buffer_size)
    sys.stdout = logfile
    sys.stderr = errfile


def close():
    sys.stdout = orig_stdout
    sys.stderr = orig_stderr
    logfile.close()
    errfile.close()
