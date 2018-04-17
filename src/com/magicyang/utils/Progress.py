# coding=utf-8
import sys
import threading
import time

PREFIX = ''
PROGRESS = 0


def progress(percent):
    count = percent / 4
    msg = "\r" + "%-15s" + " %3d" + "%% |"
    for i in range(0, count):
        msg += "█"
    for i in range(0, 25 - count):
        msg += " "
    msg += "|"
    sys.stdout.write(msg % (PREFIX, percent))
    sys.stdout.flush()


def prefix(prefix):
    global PREFIX
    PREFIX = prefix


def mock_wait(prefix=''):
    global PREFIX
    PREFIX = prefix
    _thread = threading.Thread(target=__mock, name="progress")
    _thread.setDaemon(True)
    _thread.start()


def reMock(prefix=''):
    global PROGRESS
    PROGRESS = 0
    global PREFIX
    PREFIX = prefix


def mock_end():
    global PROGRESS
    PROGRESS = 100
    progress(PROGRESS)
    print ''


def __mock():
    global PROGRESS
    PROGRESS = 0
    while PROGRESS <= 95:
        progress(PROGRESS)
        if PROGRESS < 50:
            PROGRESS += 3
        elif PROGRESS < 80:
            PROGRESS += 2
        else:
            PROGRESS += 1
        time.sleep(0.1)
