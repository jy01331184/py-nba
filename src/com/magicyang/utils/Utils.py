from datetime import date, datetime

import re

from com.magicyang.nba import DB


def get_age(data_str):
    birthday = datetime.datetime.strptime(data_str, '%Y-%m-%d')
    today = date.today()
    try:
        birthday = birthday.replace(year=today.year)
    except ValueError:
        # raised when birth date is February 29
        # and the current year is not a leap year
        birthday = birthday.replace(year=today.year, day=birthday.day - 1)
    if birthday > today:
        return today.year - birthday.year - 1
    else:
        return today.year - birthday.year


def make_draft(obj):
    if obj[26] == 'Undrafted':
        return 'Undrafted'

    msg = obj[26]

    if obj[27] == '':
        msg += " without pick"
    else:
        msg += " round:" + obj[27] + " overall:" + obj[
            28]

    return msg


def make_height(obj):
    return obj["heightMeters"] + "m"


def make_weight(obj):
    return obj["weightKilograms"] + "kg"


def make_team_name(obj):
    team = DB.team(obj['teamId'])
    if team is not None:
        return team['fullName']
    return ''


def make_pct(obj, base=9, point=True):
    if obj[base] is None:
        return ''

    if point:
        return "{:>4.1f}/{:<4.1f}{:>5.1f}%".format(obj[base], obj[base + 1], (obj[base + 2] * 100))
    else:
        return "{:>2.0f}/{:<2.0f}{:>5.1f}%".format(obj[base], obj[base + 1], (obj[base + 2] * 100))


def make_season():
    year = datetime.now().year
    next_year = year + 1

    return str(year) + "-" + str(next_year % 100)


def validate_date(m_date):
    pattern = re.compile(r'\d\d\d\d-\d\d')
    return pattern.match(m_date)
