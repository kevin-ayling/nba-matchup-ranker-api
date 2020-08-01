from requests.exceptions import Timeout
from time import sleep

def call_nba_api(api_call, positional_arguments, keyword_arguments):
    failures = 1
    print('initiating call to {} with {}, {}'.format(api_call, positional_arguments, keyword_arguments))
    while True:
        try:
            resp = api_call(*positional_arguments, **keyword_arguments)
            return resp
        except Timeout as ex:
            if failures > 25:
                print("Caught {} {}s in a row from {}. Raising error and exiting.".format(failures, type(ex).__name__,
                                                                                          api_call))
                raise RuntimeError
            wait_time = failures * failures
            print("Catching {} #{} from {}, sleeping for {} and proceeding".format(type(ex).__name__, failures, api_call, '{}s'.format(wait_time)))
            sleep(wait_time)
            failures += 1
        except Exception as ex:
            print("Caught {} from {} with args: {}, {}".format(type(ex).__name__, api_call, positional_arguments,
                                                               keyword_arguments))
            print(ex)
            raise RuntimeError


def find_matchup(game_id, matchups):
    for matchup in matchups:
        if matchup['id'] == game_id:
            return matchup
    return None


def find_season(date):
    year = date.year
    if date.month > 8:
        year2 = int(date.strftime('%y')) + 1
        return '{}-{}'.format(year,year2)
    else:
        year2 = date.strftime('%y')
        return '{}-{}'.format(year-1,year2)



def print_games(matchups, date):
    print('------------------------------------------------------------------------')
    print('{} NBA Games on {}, {} {} {}'.format(len(matchups), date.strftime('%A'), date.strftime("%B"), date.day,
                                                date.year))
    print('------------------------------------------------------------------------')
    print('')
    print('------------------------------------------------------------------------')
    i = 1
    for matchup in matchups:
        print('{}. {} vs. {}'.format(i, matchup['teams'][0]['name'], matchup['teams'][1]['name']))
        print_tv_info(matchup)
        print_result(matchup)
        print_league_leader_string(matchup)
        print('   Team Score: {}, Player Score: {}, Overall: {}'.format(matchup['score']['team'],matchup['score']['player'],matchup['score']['overall']))
        print('------------------------------------------------------------------------')
        i += 1


def print_league_leader_string(matchup):
    if len(matchup['leagueleaders']) == 0:
        return
    print('   League Leaders:')
    league_leader_str = ''
    previous_leader = 0
    for leader in matchup['leagueleaders']:
        # print('   {} - {}({})'.format(leader['name'], leader['stat'], leader['rank']))
        if leader['id'] == previous_leader:
            league_leader_str += ', {}({})'.format(leader['stat'], leader['rank'])
        elif len(league_leader_str) == 0:
            league_leader_str += '   {} - {}({})'.format(leader['name'], leader['stat'], leader['rank'])
            previous_leader = leader['id']
        else:
            print(league_leader_str)
            league_leader_str = '   {} - {}({})'.format(leader['name'], leader['stat'], leader['rank'])
            previous_leader = leader['id']
    print(league_leader_str)


def print_tv_info(matchup):
    if len(matchup['tv']) == 0:
        return
    elif matchup['tv']['scope'] == 'National':
        print('   {} on {} from the {}'.format(matchup['time'], matchup['tv']['network'], matchup['venue']))
    else:
        print('   {} on {} ({}) from the {}'.format(matchup['time'], matchup['tv']['network'], matchup['tv']['scope'],
                                                    matchup['venue']))


def print_result(matchup):
    if matchup['outcome']['w_score'] == 0:
        return
    else:
        winner = ''
        loser = ''
        for team in matchup['teams']:
            if matchup['outcome']['winner'] == team['id']:
                winner = team['name']
            elif matchup['outcome']['loser'] == team['id']:
                loser = team['name']
        print('   {} def {} {} - {}'.format(winner, loser, matchup['outcome']['w_score'], matchup['outcome']['l_score']))
