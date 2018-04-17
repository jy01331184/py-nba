import datetime

from com.magicyang import requests, Constant
from com.magicyang.nba import TeamDB
from com.magicyang.utils import Progress, Display, Log, Utils

__STAT_API = "http://stats.nba.com/stats/playercareerstats?PlayerId={PlayerId}&PerMode=PerGame"
__PROFILE_API = "http://stats.nba.com/stats/commonplayerinfo?PlayerID={PlayerId}"
__DRAFT_API = "http://stats.nba.com/stats/drafthistory?LeagueID=00&Season={Season}&OverallPick={OverallPick}"
__AWARD_API = "http://stats.nba.com/stats/playerawards?PlayerID={PlayerId}"
__GAME_LOG_API = "http://stats.nba.com/stats/playergamelog?PlayerID={PlayerId}&Season={Season}&SeasonType={SeasonType}"
__STAT_ADVANCED_API = "http://stats.nba.com/stats/playerdashboardbyyearoveryear?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID={PlayerId}&PlusMinus=Y&Rank=N&Season={Season}&SeasonSegment=&SeasonType={SeasonType}&ShotClockRange=&Split=yoy&VsConference=&VsDivision="
__PLAYER_STAT_DICT = {}
__PLAYER_PROFILE_DICT = {}


def get_player_stat_advanced(player_obj, playoff=False):
    pid = player_obj[0]

    try:
        Progress.mock_wait('load player advanced stat')
        h = dict(Constant.HEADERS)
        resp = requests.get(__STAT_ADVANCED_API.format(PlayerId=pid, Season=Utils.make_season(),
                                                       SeasonType=(
                                                           playoff and 'Playoffs' or 'Regular Season')),
                            params=None, headers=h, timeout=5)
        resp.raise_for_status()
        Progress.mock_end()
        resp_json = resp.json()
        stat_arr = resp_json['resultSets'][1]['rowSet']
        Display.display_player_advanced_stat(stat_arr, playoff)
    except Exception, e:
        Progress.mock_end()
        print e
    finally:
        pass


def get_player_log(player_obj, m_date, season_type):
    pid = player_obj[0]

    if m_date is None:
        m_date = Utils.make_season()
    elif not Utils.validate_date(m_date):
        Log.red('illegal date! pattern is yyyy-yy as 2017-18.')
        return

    try:
        Progress.mock_wait('load player game log')
        h = dict(Constant.HEADERS)
        resp = requests.get(
            __GAME_LOG_API.format(PlayerId=pid, Season=m_date, SeasonType=season_type), params=None,
            headers=h, timeout=6)
        resp.raise_for_status()
        resp_json = resp.json()
        log_arr = resp_json['resultSets'][0]['rowSet']
        Progress.mock_end()

        Display.display_game_log(log_arr)
    except Exception, e:
        Progress.mock_end()
        print e
    finally:
        pass


def get_player_award(player_obj, show_all=False):
    pid = player_obj[0]
    try:
        Progress.mock_wait('load player award')
        h = dict(Constant.HEADERS)
        resp = requests.get(__AWARD_API.format(PlayerId=pid), params=None, headers=h, timeout=6)
        resp.raise_for_status()
        resp_json = resp.json()
        award_arr = resp_json['resultSets'][0]['rowSet']

        teams = __get_player_teams(pid)

        Progress.mock_end()
        champion_record, champion_detail = TeamDB.get_champion(teams)

        Display.display_award(award_arr, champion_record, champion_detail, show_all)
    except Exception, e:
        Progress.mock_end()
        print e
    finally:
        pass


def __get_player_teams(pid):
    obj = __PLAYER_STAT_DICT.get(pid)
    result = {}
    if obj is None:
        Progress.reMock('load player\'s team')
        h = dict(Constant.HEADERS)
        resp = requests.get(__STAT_API.format(PlayerId=pid), params=None, headers=h, timeout=5)
        resp.raise_for_status()
        Progress.mock_end()
        resp_json = resp.json()
        __PLAYER_STAT_DICT[pid] = resp_json
        obj = resp_json
    season_arr = obj['resultSets'][2]['rowSet']
    for season_obj in season_arr:
        tid = season_obj[3]
        year = season_obj[1] == '1999-00' and 2000 or int(season_obj[1][0:2] + season_obj[1][5:])
        record = result.get(tid)
        if record is None:
            record = []
            result[tid] = record
        record.append(year)
    return result


def get_player_draft(player_obj):
    pid = player_obj[0]
    json_obj = get_player_profile(player_obj, False)
    player_obj = json_obj["resultSets"][0]["rowSet"][0]
    season = player_obj[26]
    draft_pick = player_obj[28]

    if season == 'Undrafted':
        Log.red("un drafted")
    else:
        Progress.mock_wait('load player draft')
        h = dict(Constant.HEADERS)
        resp = requests.get(
            __DRAFT_API.format(PlayerId=pid, Season=season, OverallPick=draft_pick, ), params=None,
            headers=h,
            timeout=5)
        resp.raise_for_status()
        Progress.mock_end()
        resp_json = resp.json()
        draft_obj = resp_json['resultSets'][0]['rowSet'][0]
        Display.display_single_draft(draft_obj)


def get_player_profile(player_obj, display=True):
    pid = player_obj[0]
    obj = __PLAYER_PROFILE_DICT.get(pid)
    if obj is None:
        try:
            Progress.mock_wait('load player profile')
            h = dict(Constant.HEADERS)
            resp = requests.get(__PROFILE_API.format(PlayerId=pid), params=None, headers=h,
                                timeout=5)
            resp.raise_for_status()
            Progress.mock_end()
            resp_json = resp.json()
            __PLAYER_PROFILE_DICT[pid] = resp_json
            obj = resp_json
            if display:
                __handle_profile(resp_json)
                # finally:
                #     pass
        except Exception, e:
            Progress.mock_end()
            print e
    else:
        if display:
            __handle_profile(obj)
    return obj


def get_player_stat(player_obj, showall=False, playoff=False):
    pid = player_obj[0]

    obj = __PLAYER_STAT_DICT.get(pid)

    if obj is None:
        try:
            Progress.mock_wait('load player stat')
            h = dict(Constant.HEADERS)
            resp = requests.get(__STAT_API.format(PlayerId=pid), params=None, headers=h, timeout=5)
            resp.raise_for_status()
            Progress.mock_end()
            resp_json = resp.json()
            __PLAYER_STAT_DICT[pid] = resp_json
            __handle_stat(resp_json, showall, playoff)
        except Exception, e:
            Progress.mock_end()
            print e
        finally:
            pass

    else:
        __handle_stat(obj, showall, playoff)


def __handle_stat(resp_json, showall, playoff):
    if playoff:
        lst_obj = resp_json['resultSets'][2]['rowSet']
        career = resp_json['resultSets'][3]['rowSet']
        if showall:
            Display.display_player_stat_all(lst_obj, career, playoff)
        else:
            Display.display_player_stat(lst_obj, career, playoff)
    else:
        lst_obj = resp_json['resultSets'][0]['rowSet']
        career = resp_json['resultSets'][1]['rowSet']
        if showall:
            Display.display_player_stat_all(lst_obj, career, playoff)
        else:
            Display.display_player_stat(lst_obj, career, playoff)


def __handle_profile(resp_json):
    Display.display_base_profile(resp_json["resultSets"][0]["rowSet"][0])
