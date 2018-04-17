from com.magicyang import Constant
from com.magicyang.handlers import CommonHandlers, PlayerHandlers, TeamHandlers, GameHandlers

COMMAND_HANDLER = {}
CURRENT_HANDLER = None
NONE_HANDLER = CommonHandlers.NoneCommandHandler("none")


def init():
    base_handler = CommonHandlers.BaseCommandHandler("base")
    player_handler = PlayerHandlers.PlayerHandler("player")
    game_handler = GameHandlers.GameHandler("game")
    team_handler = TeamHandlers.TeamHandler("team")
    COMMAND_HANDLER[Constant.COMMAND_VERSION] = base_handler
    COMMAND_HANDLER[Constant.COMMAND_EXIT] = base_handler
    COMMAND_HANDLER[Constant.COMMAND_QUIT] = base_handler
    COMMAND_HANDLER[Constant.COMMAND_HELP] = base_handler
    COMMAND_HANDLER[Constant.COMMAND_PLAYER] = player_handler
    COMMAND_HANDLER[Constant.COMMAND_TEAM] = team_handler
    COMMAND_HANDLER[Constant.COMMAND_GAME] = game_handler
    # global CURRENT_HANDLER
    # CURRENT_HANDLER = game_handler


def set_current(curr):
    global CURRENT_HANDLER
    CURRENT_HANDLER = curr
    if CURRENT_HANDLER is None:
        print "Main Menu"


def handle(cmd):
    if len(cmd) > 0:
        if CURRENT_HANDLER is None:
            handler = COMMAND_HANDLER.get(cmd)
            if handler is not None:
                handler.handle(cmd)
            else:
                NONE_HANDLER.handle(cmd)
        else:
            if not CURRENT_HANDLER.handle(cmd):
                NONE_HANDLER.handle(cmd)
