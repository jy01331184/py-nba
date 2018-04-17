# coding=utf-8
import sys

from com.magicyang import Handlers, Constant
from com.magicyang.utils import Log, Utils

if __name__ == '__main__':
    Constant.hello()
    Handlers.init()
    while True:
        cmd = raw_input(Constant.INPUT_COMMAND)
        Handlers.handle(cmd)
