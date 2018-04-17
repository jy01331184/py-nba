import sys

from com.magicyang import Constant
from com.magicyang.handlers import SundryHandlers
from com.magicyang.utils import Log, Display
from com.magicyang.nba import DB, PlayerDB, TeamDB

# from .. import Constant
# from .. import utils
from com.magicyang.utils.prettytable import PrettyTable

STATE = None  # 1->SELECT_PLAYER

CMD_PROFILE = " "
CMD_ROSTER = "-r"
CMD_STAT = "-s"
CMD_STAT_PLAYOFF = "-p"
CMD_GAME_LOG = "-l"
CMD_GAME_LOG_PLAYOFF = "-lp"
SELECT_TEAMS = []
args = None


def select_cmd(cmd):
    try:
        _select = int(cmd)
        return SELECT_TEAMS[_select]
    except Exception, e:
        print e.message


class TeamHandler(Constant.CommandHandler):
    def handle(self, cmd):

        from com.magicyang import Handlers
        global STATE
        if STATE is not None:
            if cmd == Constant.COMMAND_QUIT:
                Log.blue("team mode:")
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
        elif cmd == Constant.COMMAND_TEAM:  # quit
            Log.blue("team mode:")
            Handlers.set_current(self)
            return True
        elif cmd == Constant.COMMAND_QUIT:
            Handlers.set_current(None)
            return True
        elif cmd == Constant.COMMAND_EXIT:
            Log.red("bye~")
            sys.exit(1)
        elif cmd == Constant.COMMAND_REFRESH:
            Log.blue('refresh base data')
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
                team_name = cmds[0]
                if length >= 2:
                    postfix = cmds[1]
                    if postfix == SundryHandlers.CMD_GAME_DETAIL:
                        SundryHandlers.game_detail(team_name)
                    else:
                        global args
                        args = (length >= 3 and cmds[2] or None)
                        result = DB.team_by_name(team_name)
                        handle_base_profile(result, postfix)

                else:
                    result = DB.team_by_name(team_name)
                    handle_base_profile(result, CMD_PROFILE)
            return True


def handle_base_profile(result, state):
    if result is None or len(result) == 0:
        Log.red("no result")
    elif len(result) > 1:
        Log.yellow("input the index to select one exact team (from 0..n)")
        table = PrettyTable(["name", "tricode", "conf", "index"])
        global SELECT_TEAMS
        SELECT_TEAMS = result
        global STATE
        STATE = state
        index = 0
        for obj in result:
            table.add_row([obj['fullName'], obj['tricode'], obj['confName'], index])
            index = index + 1
        print table
    else:
        global STATE
        STATE = state
        handle_state(result[0])
        STATE = None


def handle_state(obj):
    if STATE == CMD_PROFILE:
        TeamDB.get_profile(obj)
    elif STATE == CMD_ROSTER:
        TeamDB.get_roster(obj, args)
    elif STATE == CMD_STAT:
        TeamDB.get_stat(obj, "Regular Season", args)
    elif STATE == CMD_STAT_PLAYOFF:
        TeamDB.get_stat(obj, "Playoffs", args)
    elif STATE == CMD_GAME_LOG:
        TeamDB.get_game_log(obj, "Regular Season", args)
    elif STATE == CMD_GAME_LOG_PLAYOFF:
        TeamDB.get_game_log(obj, "Playoffs", args)
    else:
        Log.red("unkown cmd:" + STATE)


def help():
    Log.blue("  team info:")
    Log.yellow("    \033[33minput\033[0m team name for team info. \033[7mE.g.\033[0m gsw or warriors")
    Log.blue("  detail info:")
    Log.yellow("    \033[33m-r \033[0m for team roster. \033[7mE.g.\033[0m gsw -r")
    Log.yellow("      \033[0m  for 2014-15 season's roster. \033[7mE.g.\033[0m gsw -r 2014-15")
    Log.yellow("    \033[33m-s \033[0m for team stat. \033[7mE.g.\033[0m gsw -s")
    Log.yellow("      \033[0m  for 2014-15 season's stat. \033[7mE.g.\033[0m gsw -s 2014-15")
    Log.yellow("    \033[33m-p \033[0m for team playoff stat. \033[7mE.g.\033[0m gsw -p")
    Log.yellow("      \033[0m  for 2014-15 season's playoff stat. \033[7mE.g.\033[0m gsw -p 2014-15")

    Log.blue("  game info:")
    Log.yellow("    \033[33m-l \033[0m for team game log. \033[7mE.g.\033[0m gsw -l")
    Log.yellow("      \033[0m  for 2014-15 season's team game log. \033[7mE.g.\033[0m gsw -l 2014-15")
    Log.yellow("    \033[33m-lp\033[0m for team playoff game log. \033[7mE.g.\033[0m gsw -lp")
    Log.yellow("      \033[0m  for 2014-15 season's team playoff game log. \033[7mE.g.\033[0m gsw -lp 2014-15")

    Log.red("  global:")
    Log.yellow("    \033[33m-d\033[0m  for game detail stat,type gameid -d. \033[7mE.g.\033[0m 0041600405 -d")

    Log.blue("\n  FOR NBA STAT TERMS,LEARN FROM https://stats.nba.com/help/glossary/")