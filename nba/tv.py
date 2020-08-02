from nba.static import find_tv_data
from datetime import datetime, timedelta

nba_month_map_2020 = {
    9: {'month': 'September', 'number': 0},
    10: {'month': 'October', 'number': 1},
    11: {'month': 'November', 'number': 2},
    12: {'month': 'December', 'number': 3},
    1: {'month': 'January', 'number': 4},
    2: {'month': 'February', 'number': 5},
    3: {'month': 'March', 'number': 6},
    7: {'month': 'July', 'number': 7},
    8: {'month': 'August', 'number': 8}
}

nba_brdcst_map = {
    'natl': 'National',
    'can': 'Cananda',
    'home': 'Home',
    'away': 'Away'
}


def find_tv_info(matchups, date):
    if date <= datetime.today() - timedelta(days=1): return
    schedule = find_tv_data(find_tv_year(date))
    for matchup in matchups:
        month = int(matchup['date'].split('/')[0])
        if 'lscd' not in schedule:
            print('debug: TV info not available')
            break
        tvgames = schedule['lscd'][nba_month_map_2020[month]['number']]['mscd']['g']
        for game in tvgames:
            if game['gid'] == matchup['id']:
                matchup['time'] = game['stt']
                matchup['venue'] = '{} in {}'.format(game['an'], game['ac'])
                matchup['tv'] = {'network': game['bd']['b'][0]['disp'],
                                 'scope': nba_brdcst_map[game['bd']['b'][0]['scope']]}


def find_tv_year(date):
    if date.month > 8:
        return date.year
    else:
        return date.year - 1
