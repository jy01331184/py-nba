import json
import urllib2
import shelve

import os

from com.magicyang import requests, Constant
from com.magicyang.utils import Progress

__DB_VERSION = 1
__LOADED = False
__TEAM = {}
__TEAM_SHORT = {}
__TEAM_NAMES = {}
__PLAYER_DICT = {}
__PLAYER_FIRST_NAME_DICT = {}
__PLAYER_LAST_NAME_DICT = {}
__PLAYER_API = "http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=0&LeagueID=00&Season=2017-18"
__TEAM_API = "http://data.nba.net/data/10s/prod/v1/2017/teams.json"
__DB_FILE = ""
__DB_PLAYERS_KEY = "players"
__DB_TEAMS_KEY = "teams"
__DB_VERSION_KEY = "db_ver"


def init(force=False):
    global __LOADED
    if not __LOADED or force:
        global __DB_FILE
        __DB_FILE = os.path.dirname(os.path.realpath(__file__)) + "/nba"

        s = shelve.open(__DB_FILE)
        old_ver = s.get(__DB_VERSION_KEY)
        if old_ver is None or __DB_VERSION > old_ver:
            s[__DB_PLAYERS_KEY] = None
            s[__DB_TEAMS_KEY] = None
            s[__DB_VERSION_KEY] = __DB_VERSION_KEY
        s.close()

        Progress.mock_wait('loading players')
        __get_players(force)
        Progress.prefix('loading teams')
        __get_teams(force)
        Progress.mock_end()
        __LOADED = True


def __get_teams(force):
    if force:
        __get_teams_from_api()
    else:
        s = shelve.open(__DB_FILE)
        teams_array = s.get(__DB_TEAMS_KEY)
        s.close()
        if teams_array is not None and len(teams_array) > 0:
            __make_team_dict(teams_array)
        else:
            __get_teams_from_api()


def __get_teams_from_api():
    response = urllib2.urlopen(__TEAM_API, timeout=5)
    json_str = response.read()
    json_object = json.loads(json_str)
    teams_array = json_object["league"]["standard"]
    __make_team_dict(teams_array)
    s = shelve.open(__DB_FILE)
    s[__DB_TEAMS_KEY] = teams_array
    s.close()


def __get_players(force):
    if force:
        __get_players_from_api()
    else:
        s = shelve.open(__DB_FILE)
        players_array = s.get(__DB_PLAYERS_KEY)
        s.close()
        if players_array is not None and len(players_array) > 0:
            __make_player_dict(players_array)
        else:
            __get_players_from_api()


def __get_players_from_api():
    s = shelve.open(__DB_FILE)
    h = dict(Constant.HEADERS)
    resp = requests.get(__PLAYER_API, params=None, headers=h, timeout=10)
    resp.raise_for_status()
    resp_json = resp.json()

    players_array = resp_json["resultSets"][0]["rowSet"]
    __make_player_dict(players_array)
    s[__DB_PLAYERS_KEY] = players_array
    s.close()


def __make_team_dict(teams_array):
    for team_object in teams_array:
        __TEAM_SHORT[str.lower(str(team_object['tricode']))] = team_object
        __TEAM[team_object['teamId']] = team_object
        names = str.split(str(team_object['fullName']), ' ')

        for name in names:
            team_arr = __TEAM_NAMES.get(str.lower(name))
            if team_arr is None:
                team_arr = []
                __TEAM_NAMES[str.lower(name)] = team_arr

            team_arr.append(team_object)


def __make_player_dict(players_array):
    for player_object in players_array:
        full_name = str.lower(str(player_object[2])).split(" ")
        first_name = full_name[0]
        if len(full_name) > 1:
            last_name = full_name[1]
        else:
            last_name = ""

        if __PLAYER_FIRST_NAME_DICT.get(first_name) is None:
            __PLAYER_FIRST_NAME_DICT[first_name] = []
        __PLAYER_FIRST_NAME_DICT[first_name].append(player_object)

        if __PLAYER_LAST_NAME_DICT.get(last_name) is None:
            __PLAYER_LAST_NAME_DICT[last_name] = []
        __PLAYER_LAST_NAME_DICT[last_name].append(player_object)


def team(id):
    return __TEAM.get(id)


def team_by_name(name=None):
    init()
    result = []
    if name is not None:
        name = str.lower(name)
        temp = __TEAM_SHORT.get(name)
        if temp is not None:
            result.append(temp)
        temp = __TEAM_NAMES.get(name)
        if temp is not None:
            result.extend(temp)
    return result


def player(firstname=None, lastname=None):
    try:
        init()
        result = []

        if firstname is not None and lastname is None:
            firstname = str.lower(firstname)
            temp = __PLAYER_FIRST_NAME_DICT.get(firstname)
            if temp is not None:
                result.extend(temp)
            temp = __PLAYER_LAST_NAME_DICT.get(firstname)
            if temp is not None:
                result.extend(temp)
        elif lastname is not None and firstname is None:
            lastname = str.lower(lastname)
            temp = __PLAYER_LAST_NAME_DICT.get(lastname)
            if temp is not None:
                result.extend(temp)
            temp = __PLAYER_FIRST_NAME_DICT.get(lastname)
            if temp is not None:
                result.extend(temp)
        elif firstname is not None and lastname is not None:
            firstname = str.lower(firstname)
            lastname = str.lower(lastname)
            temp = __PLAYER_FIRST_NAME_DICT.get(firstname)
            if temp is not None:
                for obj in temp:
                    if str.lower(str(obj[2])) == (firstname + " " + lastname):
                        result.append(obj)
        return sorted(result, __sort_base)
    except Exception, e:
        print e
    finally:
        pass


def __sort_base(x, y):
    return x[3] - y[3]
