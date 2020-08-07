from nba_api.stats.endpoints import boxscoresummaryv2
from nba.static import find_static_matchups
from nba.games import save_matchups
import logging


def find_box_scores_and_return_matchups(user_date):
    scores = 0
    matchups = find_static_matchups(user_date)
    for matchup in matchups:
        if len(matchup['boxscore']) > 0:
            if matchup['boxscore']['status'] == 'Final':
                scores += 1
                pass
        try:
            # 0021901262
            # box_score = boxscoresummaryv2.BoxScoreSummaryV2('0021901262').get_normalized_dict()
            box_score = boxscoresummaryv2.BoxScoreSummaryV2(game_id=matchup['id']).get_normalized_dict()
            matchup['boxscore'] = find_score_info(box_score)
            scores += 1
        except Exception as e:
            logging.debug('no score available for game')
    save_matchups(matchups, user_date)
    logging.info('found {} box scores for {} matchups'.format(scores, len(matchups)))
    return matchups


def all_final(matchups):
    for matchup in matchups:
        if len(matchup['boxscore']) > 0:
            if matchup['boxscore']['status'] == 'Final':
                pass
        else:
            return False
    return True


def find_score_info(box_score):
    score = {'status': box_score['GameSummary'][0]['GAME_STATUS_TEXT'],
             'teams': {box_score['LineScore'][0]['TEAM_ID']: box_score['LineScore'][0]['PTS'],
                       box_score['LineScore'][1]['TEAM_ID']: box_score['LineScore'][1]['PTS']},
             'time': box_score['GameSummary'][0]['LIVE_PC_TIME'].strip(),
             'period': box_score['GameSummary'][0]['LIVE_PERIOD']}
    return score
