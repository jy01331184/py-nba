import sys

from com.magicyang import Constant
from com.magicyang.utils import Log, Display
from com.magicyang.nba import DB, PlayerDB, TeamDB, GameDB

# from .. import Constant
# from .. import utils
from com.magicyang.utils.prettytable import PrettyTable

STATE = None  # 1->SELECT_PLAYER

CMD_GAME_DETAIL = "-d"
SELECT_TEAMS = []
args = None


def game_detail(gameid):
    GameDB.view_game_detail(gameid)
