from nba.utils import print_games
from nba.games import find_games_info
from datetime import datetime


def date_handler(event, context):
    user_date = datetime.strptime(event['date'], '%m/%d/%y')
    games = find_games_info(user_date)
    print_games(games, user_date)
    return games


if __name__ == "__main__":
    x = date_handler({'date': '08/02/20'}, {})
    print(x)