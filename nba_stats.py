from nba.utils import print_games
from nba.games import find_games_info
from datetime import date, timedelta, datetime


def main(date_to_check):
    games = find_games_info(date_to_check)
    print_games(games, date_to_check)


if __name__ == "__main__":
    user_date = datetime(2020, 8, 1)
    main(user_date)
