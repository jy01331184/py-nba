import sys

from com.magicyang import Constant
from com.magicyang.handlers import SundryHandlers
from com.magicyang.utils import Log
from com.magicyang.nba import DB, PlayerDB

# from .. import Constant
# from .. import utils
from com.magicyang.utils.prettytable import PrettyTable

STATE = None  # 1->SELECT_PLAYER
SELECT_PLAYER = []

CMD_PROFILE = " "
CMD_ADVANCED = "-ss"
CMD_ADVANCED_PLAYOFF = "-sp"
CMD_SEASON = "-s"
CMD_SEASON_ALL = "-sa"
CMD_PLAYOFF = "-p"
CMD_PLAYOFF_ALL = "-pa"
CMD_DRAFT = "-dr"
CMD_AWARD = "-a"
CMD_AWARD_ALL = "-aa"
CMD_GAME_LOG = "-l"
CMD_GAME_PLAYOFF_LOG = "-lp"
CMD_GAME_ALLSTAR_LOG = "-la"
args = None


def select_cmd(cmd):
    try:
        _select = int(cmd)
        return SELECT_PLAYER[_select]
    except Exception, e:
        print e.message


class PlayerHandler(Constant.CommandHandler):
    def handle(self, cmd):
        from com.magicyang import Handlers
        global STATE
        if STATE is not None:
            if cmd == Constant.COMMAND_QUIT:
                Log.magenta("player mode:")
                STATE = None
                return True
            elif cmd == Constant.COMMAND_EXIT:
                Log.red("bye~")
                sys.exit(1)
            else:
                obj = select_cmd(cmd)
                if obj is not None:
                    handle_state(obj)
                    STATE = None
            return True
        elif cmd == Constant.COMMAND_PLAYER:  # quit
            Log.magenta("player mode:")
            Handlers.set_current(self)
            return True
        elif cmd == Constant.COMMAND_QUIT:
            Handlers.set_current(None)
            return True
        elif cmd == Constant.COMMAND_EXIT:
            Log.red("bye~")
            sys.exit(1)
        elif cmd == Constant.COMMAND_REFRESH:
            Log.magenta('refresh base data')
            DB.init(True)
            return True
        elif cmd == Constant.COMMAND_HELP:
            help()
            return True
        else:
            cmds = str.split(cmd, ' ')
            length = len(cmds)
            if length == 0:
                Log.red('no command!')
            else:
                player_name = cmds[0]
                if length >= 2:
                    if not cmds[1].startswith('-'):
                        lastname = cmds[1]
                        result = DB.player(player_name, lastname)
                        postfix = (length >= 3 and cmds[2] or CMD_PROFILE)
                        global args
                        args = (length >= 4 and cmds[3] or None)
                        handle_base_profile(result, postfix)
                    else:
                        postfix = cmds[1]
                        if postfix == SundryHandlers.CMD_GAME_DETAIL:
                            SundryHandlers.game_detail(player_name)
                        else:
                            global args
                            args = (length >= 3 and cmds[2] or None)
                            result = DB.player(firstname=player_name)
                            handle_base_profile(result, postfix)
                else:
                    result = DB.player(firstname=player_name)
                    handle_base_profile(result, CMD_PROFILE)
            return True


def handle_base_profile(result, state):
    if result is None or len(result) == 0:
        Log.red("no result")
    elif len(result) > 1:
        Log.yellow("input the index to select one exact player (from 0..n)")
        table = PrettyTable(["name", "team", "index"])
        global SELECT_PLAYER
        SELECT_PLAYER = result
        global STATE
        STATE = state

        index = 0
        for obj in result:
            table.add_row([obj[2], obj[10], index])
            index = index + 1
        print table
    else:
        STATE = state
        handle_state(result[0])
        STATE = None


def handle_state(obj):
    if STATE == CMD_PROFILE:
        PlayerDB.get_player_profile(obj)
    elif STATE == CMD_SEASON:
        PlayerDB.get_player_stat(obj)
    elif STATE == CMD_SEASON_ALL:
        PlayerDB.get_player_stat(obj, True)
    elif STATE == CMD_PLAYOFF:
        PlayerDB.get_player_stat(obj, playoff=True)
    elif STATE == CMD_PLAYOFF_ALL:
        PlayerDB.get_player_stat(obj, True, playoff=True)
    elif STATE == CMD_DRAFT:
        PlayerDB.get_player_draft(obj)
    elif STATE == CMD_AWARD:
        PlayerDB.get_player_award(obj)
    elif STATE == CMD_AWARD_ALL:
        PlayerDB.get_player_award(obj, True)
    elif STATE == CMD_GAME_LOG:
        PlayerDB.get_player_log(obj, args, "Regular Season")
    elif STATE == CMD_GAME_PLAYOFF_LOG:
        PlayerDB.get_player_log(obj, args, "Playoffs")
    elif STATE == CMD_GAME_ALLSTAR_LOG:
        PlayerDB.get_player_log(obj, args, "All Star")
    elif STATE == CMD_ADVANCED:
        PlayerDB.get_player_stat_advanced(obj)
    elif STATE == CMD_ADVANCED_PLAYOFF:
        PlayerDB.get_player_stat_advanced(obj, True)
    else:
        Log.red("unkown cmd:" + STATE)


def help():
    Log.magenta("  player info:")

    Log.magenta(
        "    \033[33minput\033[0m player name for profile. \033[7mE.g.\033[0m lebron or lebron james")
    Log.magenta("    \033[33m-d\033[0m  for draft info. \033[7mE.g.\033[0m lebron -dr")
    Log.magenta("    \033[33m-a\033[0m  for award info. \033[7mE.g.\033[0m lebron -a")
    Log.magenta("    \033[33m-aa\033[0m for award detailed info. \033[7mE.g.\033[0m lebron -aa")
    Log.magenta("  stat info:")

    Log.magenta(
        "    \033[33m-s\033[0m  for season stat. \033[7mE.g.\033[0m lebron -s or lebron james -s")
    Log.magenta(
        "    \033[33m-sa\033[0m for season all detailed stat. \033[7mE.g.\033[0m lebron -sa")
    Log.magenta("    \033[33m-p\033[0m  for playoff stat. \033[7mE.g.\033[0m lebron -p")
    Log.magenta(
        "    \033[33m-pa\033[0m for playoff all detailed stat. \033[7mE.g.\033[0m lebron -pa")
    Log.magenta("    \033[33m-ss\033[0m for senior season stat. \033[7mE.g.\033[0m lebron -ss")
    Log.magenta("    \033[33m-sp\033[0m for senior playoff stat. \033[7mE.g.\033[0m lebron -sp")

    Log.magenta("  game log info:")
    Log.magenta("    \033[33m-l\033[0m  for game log. \033[7mE.g.\033[0m lebron -l")
    Log.magenta(
        "    \033[33m  \033[0m  for 2014-15 season's game log. \033[7mE.g.\033[0m lebron -l 2014-15")

    Log.magenta("    \033[33m-lp\033[0m for playoff game log. \033[7mE.g.\033[0m lebron -lp")
    Log.magenta(
        "    \033[33m   \033[0m for 2014-15 playoff's game log. \033[7mE.g.\033[0m lebron -lp 2014-15")

    Log.magenta("    \033[33m-la\033[0m for allstar game log. \033[7mE.g.\033[0m lebron -la")
    Log.magenta(
        "    \033[33m   \033[0m for 2014-15 allstar's game log. \033[7mE.g.\033[0m lebron -la 2014-15")
    Log.red("  global:")
    Log.yellow("    \033[33m-d \033[0m for game detail stat,type gameid -d. \033[7mE.g.\033[0m 0041600405 -d")

    Log.magenta("\n  FOR NBA STAT TERMS,LEARN FROM https://stats.nba.com/help/glossary/")
