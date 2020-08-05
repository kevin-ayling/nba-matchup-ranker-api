from nba.games import find_matchups
from datetime import datetime
from nba.utils import get_games_str
from nba.aws import write_sns
import schedule
import time
import logging
import time


def job():
    try:
        today = datetime.today()
        logging.info('running find_matchups for {}'.format(today.strftime('%Y-%m-%d')))
        start = time.time()
        games_str = get_games_str(find_matchups(today), today)
        logging.info(games_str)
        end = time.time()
        logging.info('SUCCESSFUL RUN FOR {} - Executed in {}'.format(today.strftime('%Y-%m-%d'), end - start))
        write_sns('Successful run of daily script.\n https://bit.ly/watchnba20')
    except:
        write_sns('Failure in daily script.')


def main():
    logging.basicConfig(filename='test.log', level=logging.INFO)
    # schedule.every(10).seconds.do(job)
    schedule.every().day.at("10:30").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
