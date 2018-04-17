from com.magicyang import requests, Constant
from com.magicyang.utils import Progress, Display

__GAME_SUMMARY_API = "http://stats.nba.com/stats/boxscoresummaryv2?GameID={GameID}"
__GAME_DETAIL_API = "http://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=0&EndRange=0&GameID={GameID}&RangeType=0&StartPeriod=1&StartRange=0"


def view_game_detail(gameid):
    try:
        Progress.mock_wait('load summary:' + str(gameid))
        h = dict(Constant.HEADERS)
        resp = requests.get(__GAME_SUMMARY_API.format(GameID=gameid), params=None, headers=h, timeout=6)
        resp.raise_for_status()
        resp_json = resp.json()
        sum_arr = resp_json['resultSets']

        Progress.reMock('load boxscore:' + str(gameid))
        resp = requests.get(__GAME_DETAIL_API.format(GameID=gameid), params=None, headers=h, timeout=6)
        resp.raise_for_status()
        resp_json = resp.json()
        box_arr = resp_json['resultSets']
        Progress.mock_end()
        Display.display_game_detail(sum_arr, box_arr)
    except Exception, e:
        Progress.mock_end()
        print e
    finally:
        pass
