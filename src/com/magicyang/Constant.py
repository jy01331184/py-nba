# coding=utf-8
VERSION = "1.0"
TOOL_NAME = "NBA MINI"
HELLO = "WELCOME TO " + TOOL_NAME + " " + VERSION
INPUT_COMMAND = ">"

COMMAND_EXIT = "qq"
COMMAND_QUIT = "q"
COMMAND_VERSION = "v"
COMMAND_PLAYER = "p"
COMMAND_GAME = "g"
COMMAND_TEAM = "t"
COMMAND_HELP = "h"
COMMAND_REFRESH = "r"

HEADERS = {
    'user-agent': (
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'),
    'Accept-Encoding': ('gzip, deflate, sdch'),
    'Accept-Language': ('en'),
    'referer': ('http://stats.nba.com/scores/'),
    'origin': ('http://stats.nba.com')
}


class CommandHandler:
    def __init__(self, name):
        self.name = name

    def handle(self, cmd):
        pass


def help():
    print "\033[31m"
    print "all supported command :"
    print "\033[35m\tp for [player]"
    print "\033[34m\tt for [team]"
    print "\033[33m\tg for [game]"
    print "\033[37m\tq for [quit]"
    print "\033[0m"


def hello():
    print "\033[0;36m"
    print "    ___       ___       ___            \033[0;31m___       ___       ___       ___"
    print "   \033[0;36m/\__\     /\  \     /\  \          \033[0;31m/\__\     /\  \     /\__\     /\  \\"
    print "  \033[0;36m/ | _|_   /  \  \   /  \  \        \033[0;31m/  L_L_   _\ \  \   / | _|_   _\ \  \\"
    print " \033[0;36m/  |/\__\ /  \ \__\ /  \ \__\      \033[0;31m/ /L \__\ /\/  \__\ /  |/\__\ /\/  \__\\"
    print " \033[0;36m\/|  /  / \ \  /  / \/\  /  /      \033[0;31m\/_/ /  / \  /\/__/ \/|  /  / \  /\/__/"
    print "   \033[0;36m| /  /   \  /  /    / /  /         \033[0;31m/ /  /   \ \__\     | /  /   \ \__\\"
    print "   \033[0;36m\/__/     \/__/     \/__/          \033[0;31m\/__/     \/__/     \/__/     \/__/      \033[1;37mver1.0\033[0m"


SORT_AWARD_KEYS = {'NBA Championships': 100, 'Hall of Fame Inductee': 99,
                   'NBA Most Valuable Player': 98,
                   'NBA Finals Most Valuable Player': 96, 'NBA Defensive Player of the Year': 95,
                   'NBA Most Improved Player': 94, 'NBA Sixth Man of the Year': 93,
                   'NBA All-Star Most Valuable Player': 92, 'NBA Player of the Month': 88,
                   'All-NBA 1th team': 84, 'All-Defensive Team 1th team': 83,
                   'All-NBA 2th team': 82, 'All-Defensive Team 2th team': 81,
                   'All-NBA 3th team': 80,
                   'NBA Rookie of the Year': 70, 'All-Rookie Team 1th team': 69,
                   'All-Rookie Team 2th team': 68}

DETAIL_AWARD_KEYS = {'NBA Championships', 'Hall of Fame Inductee',
                     'NBA Most Valuable Player',
                     'NBA Finals Most Valuable Player', 'NBA Defensive Player of the Year',
                     'NBA Most Improved Player', 'NBA Sixth Man of the Year',
                     'NBA All-Star Most Valuable Player',
                     'All-NBA 1th team', 'All-Defensive Team 1th team',
                     'All-NBA 2th team', 'All-Defensive Team 2th team',
                     'All-NBA 3th team',
                     'NBA Rookie of the Year', 'All-Rookie Team 1th team',
                     'All-Rookie Team 2th team'}

__TEAM_COLOR = {"ATL": "\033[0;91m🐦 ", "BKN": "\033[0;90m🕸 "}


def get_team_col(name):
    val = __TEAM_COLOR.get(name)
    return (val is None and name or val + name) + "\033[0m"
