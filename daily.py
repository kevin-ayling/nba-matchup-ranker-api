from nba.games import find_matchups
from datetime import datetime
from nba.utils import get_games_str
import schedule
import time
import logging
import time


def job():
    today = datetime.today()
    logging.info('running find_matchups for {}'.format(today.strftime('%Y-%m-%d')))
    start = time.time()
    games_str = get_games_str(find_matchups(today), today)
    logging.info(games_str)
    end = time.time()
    logging.info('SUCCESSFUL RUN FOR {} - Executed in {}'.format(today.strftime('%Y-%m-%d'), end - start))


def main():
    logging.basicConfig(filename='test.log', level=logging.INFO)
    schedule.every(30).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
