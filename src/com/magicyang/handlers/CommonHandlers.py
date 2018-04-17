from com.magicyang import Constant
from com.magicyang.utils import Log


# from .. import Constant
# from .. import utils


class BaseCommandHandler(Constant.CommandHandler):
    def handle(self, cmd):
        if cmd == Constant.COMMAND_QUIT or cmd == Constant.COMMAND_EXIT:  # quit
            Log.red("bye~")
            quit(1)
        elif cmd == Constant.COMMAND_VERSION:
            Log.red(Constant.VERSION)
        elif cmd == Constant.COMMAND_HELP:
            Constant.help()


class NoneCommandHandler(Constant.CommandHandler):
    def handle(self, cmd):
        Log.red("no command '" + cmd + "'. type h for help")
