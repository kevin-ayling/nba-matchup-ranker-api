from nba.players import find_player_league_leader_info
from nba.static import find_teams, find_standings


def find_team_name(team_id, season):
    standings = find_standings(season)
    for team in standings:
        if team['TeamID'] == team_id:
            return team['TeamName']


# input: teamId - number
# output: playoffRank - number (1-15)
def find_team_playoff_ranking(team_id, season):
    standings = find_standings(season)
    for team in standings:
        if team['TeamID'] == team_id:
            return team['PlayoffRank']


# input: teamId - number
# output:
# leaders =
#   [{
#     'id': player_id,
#     'name': player_name,
#     'stat': category,
#     'rank': rank
#   }]
def find_team_league_leader_info(team_id, season):
    teams = find_teams(season)
    leaders = []
    if isinstance(team_id, int):
        if team_id in teams:
            pass
        else:
            team_id = str(team_id)
    for player in teams[team_id]:
        leaders.extend(find_player_league_leader_info(player['PLAYER_ID'], season))
    return leaders
