# coding=utf-8
from com.magicyang import Constant
from com.magicyang.utils import Utils, Log
from com.magicyang.utils.prettytable import PrettyTable


def display_game_detail(sum_arr, box_arr):
    line_score = sum_arr[5]['rowSet']
    if len(line_score) == 0:
        Log.red("no record")
        return
    index = 12

    titles = ['', "Q1", "Q2", "Q3", "Q4"]
    while index < 22 and line_score[0][index] > 0:
        index = index + 1
        titles.append("TO" + str(index - 12))
    titles.extend(['FINAL', 'PTS_PAINT', 'PTS_2ND_CHANCE', 'PTS_OFF_TO', 'LARGEST_LEAD'])
    table = PrettyTable(titles)

    temp_index = 0
    crown_index = 0 if line_score[0][22] > line_score[1][22] else 1
    for score_obj in line_score:
        other_score = sum_arr[1]['rowSet'][temp_index]
        row = [str(score_obj[4]) + (temp_index == crown_index and '' or '0041700152'), score_obj[8],
               score_obj[9], score_obj[10], score_obj[11]]
        for i in range(12, index):
            row.append(score_obj[i])
        row.extend([score_obj[22], other_score[4], other_score[5], other_score[13], other_score[7]])
        temp_index = temp_index + 1
        table.add_row(row)

    print table

    table = PrettyTable(['', '', '', '', '',
                         "", "", "", "",
                         "", "", "", "", "", ""])

    table.header = False
    score_arr = box_arr[0]['rowSet']
    temp_team = score_arr[0][2]
    temp_index = 0
    for box_obj in score_arr:
        temp_index += 1
        if box_obj[2] != temp_team:
            table.add_row(
                ['PLAYER', 'MIN', 'PTS', "FG_PCT", "FG3_PCT",
                 "FT_PCT", "REB", "OREB", "DREB",
                 "AST", "BLK", "STL", "TOV", "PF", "+-"])
            table.mid_head_index = temp_index
            temp_team = box_obj[2]

        dnp = box_obj[8] is None
        if dnp:
            table.add_row([box_obj[5], 'DNP', '',
                           '', '', '', '', '', '', '', '', '', '', '', ''])
        else:
            table.add_row(
                [box_obj[5] + (len(box_obj[6]) > 0 and " (" + box_obj[6] + ")" or ""), box_obj[8],
                 box_obj[26],
                 Utils.make_pct(box_obj, 9, False), Utils.make_pct(box_obj, 12, False),
                 Utils.make_pct(box_obj, 15, False), box_obj[20], box_obj[18], box_obj[19],
                 box_obj[21], box_obj[23], box_obj[22], box_obj[24], box_obj[25],
                 int(box_obj[27])])

    print table


def display_team_game_log(game_arr, season, playoff):
    if len(game_arr) == 0:
        Log.red('no record')
        return

    table = PrettyTable(
        [playoff and "PLAYOFF" or "SEASON", "DATE", "MATCHUP", "WL", "PTS", "FG_PCT", "FG3_PCT",
         "FT_PCT", "REB", "OREB", "DREB",
         "AST",
         "BLK", "STL", "TOV", "PF", "GAME_ID"])
    table.color_cols = {'GAME_ID': Log.wrap_yellow}
    for game_obj in game_arr:
        table.add_row([season, game_obj[2], game_obj[3], game_obj[4], game_obj[26],
                       Utils.make_pct(game_obj, 9, point=False),
                       Utils.make_pct(game_obj, point=False),
                       Utils.make_pct(game_obj, 15, point=False), game_obj[20], game_obj[18],
                       game_obj[19],
                       game_obj[21], game_obj[23], game_obj[22], game_obj[24], game_obj[25],
                       game_obj[1]])

    print table


def display_team_stat(stat_arr, season, playoff):
    season_stat_arr = stat_arr[1]['rowSet']
    if len(season_stat_arr) == 0:
        Log.red('no record')
        return

    table = PrettyTable(
        [playoff and "PLAYOFF" or "SEASON", "PLAYER", "GP", "MIN", "PTS", "FG_PCT", "FG3_PCT",
         "FT_PCT", "REB", "OREB", "DREB",
         "AST",
         "BLK", "STL", "TOV", "PF", "+-"])

    season_stat_arr = sorted(season_stat_arr, __sort_team_stat)
    for stat_obj in season_stat_arr:
        table.add_row([season, stat_obj[2], stat_obj[3], stat_obj[7], stat_obj[27],
                       Utils.make_pct(stat_obj, 8), Utils.make_pct(stat_obj, 11),
                       Utils.make_pct(stat_obj, 14), stat_obj[19], stat_obj[17], stat_obj[18],
                       stat_obj[20], stat_obj[23], stat_obj[22], stat_obj[21], stat_obj[25],
                       stat_obj[28]])

    print table


def display_team_roster(roster_arr, season):
    table = PrettyTable(["SEASON", "PLAYER", "POSITION", "JERSEY", "AGE", "EXP"])
    player_arr = roster_arr[0]['rowSet']
    if len(player_arr) == 0:
        Log.red('no roster')
        return
    for player_obj in player_arr:
        if player_obj[9] is None:
            age = ''
        else:
            age = int(player_obj[9])
        table.add_row([season, player_obj[3], player_obj[5], player_obj[4],
                       age,
                       player_obj[10]])

    if len(roster_arr[1]['rowSet']) > 0:
        coach_obj = roster_arr[1]['rowSet'][0]
        table.add_row([season, coach_obj[5], coach_obj[8], "-", "-", "-"])
    print table


def display_team_profile(base_team, team_obj):
    table = PrettyTable(
        ["NAME", "TRICODE", "CITY", "CONF",
         "DIV", "ARENA", "COACH", "OWNER", "MANAGER", "FOUNDED"])

    if len(team_obj[0]['rowSet']) == 0:
        Log.red('no team profile for ' + base_team['fullName'])
        return

    profile_obj = team_obj[0]['rowSet'][0]
    table.add_row(
        [base_team['fullName'], base_team['tricode'], base_team['city'], base_team['confName'],
         base_team['divName'], profile_obj[5], profile_obj[9], profile_obj[7], profile_obj[8],
         profile_obj[3]])
    print table

    cham_time = len(team_obj[3]['rowSet'])
    conf_cham_time = len(team_obj[4]['rowSet'])
    retired_arr = team_obj[7]['rowSet']

    table = PrettyTable(["CHAMPIONSHIP", "CONF-CHAMPIONSHIP", "TeamRetired"])
    flag = True
    num = 0
    retired_line = ''
    for retired_obj in retired_arr:
        if num % 3 > 0:
            retired_line += ','
        jersey = str.strip(str(retired_obj[3]))
        retired_line += retired_obj[1] + "-" + (
            len(jersey) > 0 and str(retired_obj[3]) or "?") + "(" + str(retired_obj[5]) + ")"
        num = num + 1
        if num % 3 == 0:
            table.add_row([flag and cham_time or '-', flag and conf_cham_time or '-', retired_line])
            retired_line = ''
            flag = False
    if len(retired_line) > 0:
        table.add_row([flag and cham_time or '-', flag and conf_cham_time or '-', retired_line])

    print table


def display_game_log(game_log_arr):
    if len(game_log_arr) == 0:
        Log.red("no record")
        return

    table = PrettyTable(
        ["DATE", "VS", "WIN", "MIN",
         "PTS", "REB", "AST", "OREB", "DREB",
         "FG_PCT", "FG3_PCT", "FT_PCT",
         "BLK", "STL", "TOV", "PF", "+-", "GAME_ID"])
    table.color_cols = {"GAME_ID": Log.wrap_yellow}
    for game_obj in game_log_arr:
        table.add_row([game_obj[3], game_obj[4], game_obj[5], game_obj[6],
                       game_obj[24], game_obj[18], game_obj[19], game_obj[16], game_obj[17],
                       Utils.make_pct(game_obj, 7, False), Utils.make_pct(game_obj, 10, False),
                       Utils.make_pct(game_obj, 13, False),
                       game_obj[21], game_obj[20], game_obj[22],
                       game_obj[23], game_obj[25], game_obj[2]])
    print table


def display_award(award_arr, cham_record, champion_detail, show_all):
    award_dict = {}
    award_detail = {}

    for award_obj in award_arr:
        award_name = award_obj[4]
        all_nba_team_num = award_obj[5]
        if all_nba_team_num is not None and len(
                all_nba_team_num) > 0 and 'null' not in all_nba_team_num:
            award_name = award_name + " " + all_nba_team_num + "th team"

        record = award_dict.get(award_name)
        if record is None:
            award_dict[award_name] = 1
        else:
            award_dict[award_name] = record + 1
        if show_all:
            detail = award_detail.get(award_name)
            if detail is None:
                detail = []
                award_detail[award_name] = detail

            month = award_obj[7]
            week = award_obj[8]

            if month is not None and len(month) > 0 and 'null' not in month:
                to_append = str.replace(str(month), 'T00:00:00', '')
            elif week is not None and len(week) > 0 and 'null' not in week:
                to_append = str.replace(str(week), 'T00:00:00', '')
            else:
                to_append = award_obj[6]
            detail.append(to_append)

    for (k, v) in cham_record.items():
        award_dict[k] = v
        if show_all:
            award_detail[k] = champion_detail.get(k)

    if len(award_dict) > 0:

        if show_all:
            table = PrettyTable(["AWARD", "TIME", "DETAIL"])
            table.color_cols = {'DETAIL': Log.wrap_yellow}
        else:
            table = PrettyTable(["AWARD", "TIME"])
        table.align = "c"
        keys = award_dict.keys()
        keys.sort(__sort_award)

        for k in keys:

            if show_all:
                init_row = True
                details = award_detail.get(k)
                write_count = 0
                if details is not None:
                    temp_detail = ''
                    array = sorted(award_detail.get(k))
                    for detail in array:
                        temp_detail = temp_detail + "  " + detail
                        write_count = write_count + 1
                        if write_count % 3 == 0:
                            table.add_row([init_row and k or '', init_row and award_dict[k] or '',
                                           temp_detail])
                            init_row = False
                            temp_detail = ''
                    if len(temp_detail) > 0:
                        table.add_row(
                            [init_row and k or '', init_row and award_dict[k] or '', temp_detail])
                        init_row = False
                if init_row is True:
                    table.add_row([k, award_dict[k], ''])

            else:
                table.add_row([k, award_dict[k]])
        print table
    else:
        Log.red("no award for this player")


def __sort_award(x, y):
    x_pri = Constant.SORT_AWARD_KEYS.get(x)
    y_pri = Constant.SORT_AWARD_KEYS.get(y)
    if x_pri is not None and y_pri is None:
        return -1
    elif x_pri is None and y_pri is not None:
        return 1
    elif x_pri is None and y_pri is None:
        return cmp(x, y)
    else:
        return -x_pri + y_pri


def __sort_team_stat(x, y):
    if x[27] > y[27]:
        return -1
    elif x[27] < y[27]:
        return 1
    else:
        return 0


def display_base_profile(obj):
    table = PrettyTable(
        ["FIRSTNAME", "LASTNAME", "TEAM", "POSITION", "HEIGHT", "WEIGHT", "BIRTHDAY", "JERSEY",
         "DRAFT",
         ])
    table.align = "c"
    table.add_row([obj[1], obj[2], obj[18], obj[14],
                   obj[10], obj[11],
                   obj[6][0:10], obj[13], Utils.make_draft(obj)
                   ])
    print table


def display_single_draft(obj):
    table = PrettyTable(
        ["NAME", "YEAR", "ROUND", "PICK", "OVERALL", "TEAM", "FROM"])
    table.align = "c"
    table.add_row([obj[1], obj[2], obj[3], obj[4],
                   obj[5], obj[9],
                   obj[10]
                   ])
    print table


def display_player_stat(obj, career, playoff=False):
    table = PrettyTable(
        [playoff is True and "PLAYOFF" or "SEASON", "TEAM", "GP", "MIN", "PTS", "REB", "OREB",
         "DREB"
            , "AST", "BLK", "STL", "TOV", "PF"
         ])

    for season_obj in reversed(obj):
        table.add_row([season_obj[1], season_obj[4], season_obj[6], season_obj[8], season_obj[26],
                       season_obj[20], season_obj[18],
                       season_obj[19], season_obj[21], season_obj[23],
                       season_obj[22], season_obj[24], season_obj[25]])

    for season_obj in career:
        table.add_row(["career", "", season_obj[3], season_obj[5], season_obj[23],
                       season_obj[17], season_obj[15],
                       season_obj[16], season_obj[18], season_obj[19],
                       season_obj[20], season_obj[21], season_obj[22]])

    print table


def display_player_advanced_stat(arr, playoff=False):
    table = PrettyTable(
        [playoff is True and "PLAYOFF" or "SEASON", "TEAM", "PIE", "USG%", "TS%", "EFG%", "OFFRTG",
         "DEFRTG", "NETRTG",
         "REB%", "OREB%", "DREB%"
            , "AST%", "AST RATIO", "AST/TO", "TO RATIO", "PACE"
         ])
    for stat_obj in arr:
        table.add_row(
            [stat_obj[1], stat_obj[3], stat_obj[24] * 100, stat_obj[22] * 100, stat_obj[21] * 100,
             stat_obj[20] * 100, stat_obj[10], stat_obj[11], stat_obj[12], stat_obj[18] * 100,
             stat_obj[16] * 100, stat_obj[17] * 100, stat_obj[13] * 100,
             stat_obj[15], stat_obj[14], stat_obj[19], stat_obj[23]])

    print table


def display_player_stat_all(obj, career, playoff=False):
    table = PrettyTable(
        [playoff is True and "PLAYOFF" or "SEASON", "TEAM", "GP", "MIN", "PTS", "FG_PCT", "FG3_PCT",
         "FT_PCT", "REB", "OREB", "DREB",
         "AST", "BLK", "STL", "TOV", "PF"
         ])

    for season_obj in reversed(obj):
        table.add_row([season_obj[1], season_obj[4], season_obj[6], season_obj[8], season_obj[26],
                       Utils.make_pct(season_obj), Utils.make_pct(season_obj, 12),
                       Utils.make_pct(season_obj, 15), season_obj[20],
                       season_obj[18],
                       season_obj[19], season_obj[21], season_obj[23],
                       season_obj[22], season_obj[24], season_obj[25]])

    for season_obj in career:
        table.add_row(["career", "", season_obj[3], season_obj[5], season_obj[23],
                       Utils.make_pct(season_obj, 6), Utils.make_pct(season_obj, 9),
                       Utils.make_pct(season_obj, 12),
                       season_obj[15],
                       season_obj[16], season_obj[17], season_obj[18], season_obj[19],
                       season_obj[20], season_obj[21], season_obj[22]])
    print table
