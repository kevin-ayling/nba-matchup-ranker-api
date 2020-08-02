from nba_api.stats.endpoints import leaguestandings, homepageleaders, commonteamroster, leaguegamefinder, scoreboardv2, leaguegamelog, teamgamelog, teamgamelogs, teaminfocommon
from nba.utils import call_nba_api
import json
import requests
import os.path
from os import path

league_leader_categories = ['Points', 'Rebounds', 'Assists', 'Defense', 'Clutch', 'Playmaking', 'Efficiency',
                            'Fast Break', 'Scoring Breakdown']


def find_league_leaders(season):
    static_leaders = {}
    if path.isfile('nba/data/HomePageLeaders.json'):
        with open('nba/data/HomePageLeaders.json') as json_file:
            static_leaders = json.load(json_file)
            if season in static_leaders:
                return static_leaders[season]
    league_leaders = {}
    for category in league_leader_categories:
        league_leaders[category] = []
        leaders = call_nba_api(homepageleaders.HomePageLeaders,
                               ['Season', '00', 'Player', 'All Players', season,
                                'Regular Season',
                                category], {}).get_normalized_dict()
        league_leaders[category] = leaders['HomePageLeaders']
        static_leaders[season] = league_leaders
    with open('nba/data/HomePageLeaders.json', 'w') as outfile:
        json.dump(static_leaders, outfile, default=str)
    return league_leaders


def find_standings(season):
    static_standings = {}
    if path.isfile('nba/data/LeagueStandings.json'):
        with open('nba/data/LeagueStandings.json') as json_file:
            static_standings = json.load(json_file)
            if season in static_standings:
                return static_standings[season]['Standings']
    static_standings[season] = call_nba_api(leaguestandings.LeagueStandings, ['00', season, 'Regular Season'],
                                            {}).get_normalized_dict()
    with open('nba/data/LeagueStandings.json', 'w') as outfile:
        json.dump(static_standings, outfile, default=str)
    return static_standings[season]['Standings']


def find_teams(season):
    if path.isfile('nba/data/LeagueTeams{}.json'.format(season)):
        with open('nba/data/LeagueTeams{}.json'.format(season)) as json_file:
            return json.load(json_file)
    else:
        league_teams = {}
        standings = find_standings(season)
        for team in standings:
            team_resp = call_nba_api(commonteamroster.CommonTeamRoster, [team['TeamID'], season],
                                     {}).get_normalized_dict()
            league_teams[team['TeamID']] = team_resp['CommonTeamRoster']
        with open('nba/data/LeagueTeams{}.json'.format(season), 'w') as outfile:
            json.dump(league_teams, outfile, default=str)
        return league_teams


def find_scoreboard(date):
    scoreboard_resp = {}
    if path.isfile('nba/data/LeagueScoreBoard.json'):
        with open('nba/data/LeagueScoreBoard.json') as json_file:
            static_games = json.load(json_file)
            if date.strftime('%m/%d/%Y') in static_games:
                return static_games[date.strftime('%m/%d/%Y')]
    scoreboard_resp[date.strftime('%m/%d/%Y')] = call_nba_api(scoreboardv2.ScoreboardV2, [0, date.strftime('%Y-%m-%d'), '00'],
                                   {}).get_normalized_dict()

    with open('nba/data/LeagueScoreBoard.json', 'w') as outfile:
        json.dump(scoreboard_resp, outfile, default=str)
    return scoreboard_resp[date.strftime('%m/%d/%Y')]


def find_static_games(date):
    static_games = {}
    if path.isfile('nba/data/LeagueGames.json'):
        with open('nba/data/LeagueGames.json') as json_file:
            static_games = json.load(json_file)
            if date.strftime('%m/%d/%Y') in static_games:
                return static_games[date.strftime('%m/%d/%Y')]
    gamefinder_resp = call_nba_api(leaguegamefinder.LeagueGameFinder, [],
                                   {"league_id_nullable": "00", "player_or_team_abbreviation": "T",
                                    "date_from_nullable": date.strftime('%m/%d/%Y'),
                                    "date_to_nullable": date.strftime('%m/%d/%Y')})
    if len(gamefinder_resp.get_normalized_dict()['LeagueGameFinderResults']) == 0:
        return []
    static_games[date.strftime('%m/%d/%Y')] = gamefinder_resp.get_normalized_dict()['LeagueGameFinderResults']
    with open('nba/data/LeagueGames.json', 'w') as outfile:
        json.dump(static_games, outfile, default=str)
    return static_games[date.strftime('%m/%d/%Y')]

#
# def find_team_matchup_history(season, team_id):
#     teamgames = call_nba_api(teamgamelog.TeamGameLog, [], {'season': season, 'season_type_all_star': 'Regular Season', 'team_id': team_id, 'league_id_nullable': '00'}).get_normalized_dict()
#     allteamgames = call_nba_api(teamgamelogs.TeamGameLogs, [], {}).get_normalized_dict()
#     print("hi")


def find_common_team_info(season):
    static_team_info = {}
    if path.isfile('nba/data/LeagueTeamInfo.json'):
        with open('nba/data/LeagueTeamInfo.json') as json_file:
            static_team_info = json.load(json_file)
            if season in static_team_info:
                return static_team_info[season]
    standings = find_standings(season)
    teaminfo = {}
    for team in standings:
        teaminfo[team['TeamID']] = call_nba_api(teaminfocommon.TeamInfoCommon, [], {'league_id': '00','team_id' :team['TeamID'], 'season_type_nullable': 'Regular Season', 'season_nullable':season}).get_normalized_dict()
    static_team_info[season] = teaminfo
    with open('nba/data/LeagueTeamInfo.json', 'w') as outfile:
        json.dump(static_team_info, outfile, default=str)
    return teaminfo


def find_tv_data(year):
    static_tv_info = {}
    if path.isfile('nba/data/LeagueTVInfo.json'):
        with open('nba/data/LeagueTVInfo.json') as json_file:
            static_tv_info = json.load(json_file)
            if str(year) in static_tv_info:
                return static_tv_info[str(year)]
    static_tv_info[year] = requests.get(
        'http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/{}/league/00_full_schedule.json'.format(year)).json()
    with open('nba/data/LeagueTVInfo.json', 'w') as outfile:
        json.dump(static_tv_info, outfile, default=str)
    return static_tv_info[year]
