from flask import Flask
from nba.utils import get_games_str
from nba.games import find_matchups
from nba.aws import write_sns
from datetime import datetime

app = Flask(__name__)


@app.route('/ping')
def hello():
    return "healthy"


@app.route('/date/<date>')
def date(date):
    user_date = datetime.strptime(date, '%m-%d-%y')
    games = find_matchups(user_date)
    return get_games_str(games,user_date)

@app.route('/daily')
def daily():
    today = datetime.today()
    games = find_matchups(today)
    return get_games_str(games,today)

if __name__ == '__main__':
    app.run()