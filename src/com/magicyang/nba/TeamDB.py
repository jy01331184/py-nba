from com.magicyang import Constant, requests
from com.magicyang.utils import Progress, Display, Utils, Log

__TEAM_DICT = {}
__TEAM_API = "http://stats.nba.com/stats/teamdetails?TeamID={TeamID}"
__ROSTER_API = "http://stats.nba.com/stats/commonteamroster?TeamID={TeamID}&Season={Season}"
__STAT_API = "http://stats.nba.com/stats/teamplayerdashboard?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&TeamID={TeamID}&PlusMinus=N&Rank=N&Season={Season}&SeasonSegment=&SeasonType={SeasonType}&ShotClockRange=&VsConference=&VsDivision="
__GAME_LOG_API = "http://stats.nba.com/stats/teamgamelog?DateFrom=&DateTo=&LeagueID=00&Season={Season}&SeasonType={SeasonType}&TeamID={TeamID}"


def get_game_log(team_obj, season_type, sesson):
    if sesson is None:
        sesson = Utils.make_season()
    elif not Utils.validate_date(sesson):
        Log.red('illegal date! pattern is yyyy-yy as 2017-18.')
        return
    teamid = team_obj['teamId']
    Progress.mock_wait('load team game log:' + str(teamid))
    h = dict(Constant.HEADERS)
    resp = requests.get(__GAME_LOG_API.format(TeamID=teamid, Season=sesson, SeasonType=season_type),
                        params=None, headers=h, timeout=6)
    resp.raise_for_status()
    resp_json = resp.json()
    game_arr = resp_json['resultSets'][0]['rowSet']
    Progress.mock_end()
    Display.display_team_game_log(game_arr, sesson, season_type == "Playoffs")


def get_stat(team_obj, season_type, sesson):
    if sesson is None:
        sesson = Utils.make_season()
    elif not Utils.validate_date(sesson):
        Log.red('illegal date! pattern is yyyy-yy as 2017-18.')
        return
    teamid = team_obj['teamId']
    Progress.mock_wait('load team stat:' + str(teamid))
    h = dict(Constant.HEADERS)
    resp = requests.get(__STAT_API.format(TeamID=teamid, Season=sesson, SeasonType=season_type),
                        params=None,
                        headers=h, timeout=6)
    resp.raise_for_status()
    resp_json = resp.json()
    stat_arr = resp_json['resultSets']
    Progress.mock_end()
    Display.display_team_stat(stat_arr, sesson, season_type == "Playoffs")


def get_roster(team_obj, sesson):
    if sesson is None:
        sesson = Utils.make_season()
    elif not Utils.validate_date(sesson):
        Log.red('illegal date! pattern is yyyy-yy as 2017-18.')
        return
    teamid = team_obj['teamId']
    Progress.mock_wait('load team roster:' + str(teamid))
    h = dict(Constant.HEADERS)
    resp = requests.get(__ROSTER_API.format(TeamID=teamid, Season=sesson), params=None, headers=h,
                        timeout=6)
    resp.raise_for_status()
    resp_json = resp.json()
    roster_arr = resp_json['resultSets']
    Progress.mock_end()
    Display.display_team_roster(roster_arr, sesson)


def get_profile(team_obj):
    teamid = team_obj['teamId']
    team_profile = __TEAM_DICT.get(teamid)
    if team_profile is None:
        team_profile = __get_team_from_api(teamid)
    Display.display_team_profile(team_obj, team_profile)


def get_champion(team_dict):
    keys = team_dict.keys()
    result = {}
    result_time = {}

    for k in keys:
        team_obj = __TEAM_DICT.get(k)
        if team_obj is None:
            team_obj = __get_team_from_api(k)

        team_years = team_dict[k]

        cham_arr = team_obj[3]['rowSet']
        for cham_obj in cham_arr:
            cham_year = cham_obj[0]
            if cham_year in team_years >= 0:
                cham_record = result.get('NBA Championships')
                if cham_record is None:
                    result_time['NBA Championships'] = []
                    result['NBA Championships'] = 1
                else:
                    result['NBA Championships'] = result['NBA Championships'] + 1
                result_time['NBA Championships'].append(str(cham_year))
        conf_arr = team_obj[4]['rowSet']
        for conf_obj in conf_arr:
            conf_year = conf_obj[0]
            if conf_year in team_years >= 0:
                cham_record = result.get('NBA Conference Championships')
                if cham_record is None:
                    result_time['NBA Conference Championships'] = []
                    result['NBA Conference Championships'] = 1
                else:
                    result['NBA Conference Championships'] = result[
                                                                 'NBA Conference Championships'] + 1
                result_time['NBA Conference Championships'].append(str(conf_year))
    return result, result_time


def __get_team_from_api(tid):
    Progress.mock_wait('load team info:' + str(tid))
    h = dict(Constant.HEADERS)
    resp = requests.get(__TEAM_API.format(TeamID=tid), params=None, headers=h, timeout=6)
    resp.raise_for_status()
    resp_json = resp.json()
    team_arr = resp_json['resultSets']

    __TEAM_DICT[tid] = team_arr
    Progress.mock_end()
    return team_arr
