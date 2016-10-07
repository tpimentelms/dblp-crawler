import time
import random


class Timer(object):
    start = None

    def __init__(self):
        self.start = time.time()

    def get_time(self):
        end = time.time()
        return end - self.start

    def print_time(self):
        time = self.get_time()
        print 'Time:', time


def start_print_progress(interval, typestr, initial_count=0):
    print_progress.timer = Timer()
    print_progress.count = initial_count
    print_progress.interval = interval
    print_progress.typestr = typestr


def print_progress(maxcount):
    if (print_progress.count % print_progress.interval) == 0:
        print 'Processed %d %s of %d (Took: %lfs).' % (print_progress.count, print_progress.typestr, maxcount, print_progress.timer.get_time())
        print_progress.timer = Timer()
    print_progress.count += 1
print_progress.count = 0
print_progress.interval = 0
maxcount = 0
print_progress.typestr = None
print_progress.timer = Timer()
