from nba.games import find_matchups
from datetime import datetime
from nba.utils import get_games_str, get_games_str_sns
from nba.static import find_links
from nba.links import generate_html_and_write_to_s3, map_links, print_links
from nba.twilio import send_sms, send_alert
import schedule
import time
import logging
import time


def job():
    try:
        start = time.time() # start timer
        today = datetime.today()
        logging.info('running find_matchups for {}'.format(today.strftime('%Y-%m-%d')))
        games = find_matchups(today) #get matchups
        games_str_sns = get_games_str_sns(games, today) #get summary of matchups
        logging.info(games_str_sns)
        send_sms(games_str_sns) #send summary to phone numbers
        links = find_links(today) #find links (invoke scraper or find in local)
        link_map = map_links(games, links) #map links to list of matchups
        generate_html_and_write_to_s3(link_map) #update static s3 site with links
        print_links(link_map)
        end = time.time() # stop timer
        logging.info('SUCCESSFUL RUN FOR {} - Executed in {}'.format(today.strftime('%Y-%m-%d'), end - start))
    except Exception as e:
        logging.error(e)
        logging.exception('failure')
        send_alert('Failure in daily script.')


def main():
    logging.basicConfig(filename='cron.log', level=logging.INFO)
    logging.info('--------- STARTING UP SCRIPT ---------------')
    # schedule.every(10).seconds.do(job)
    schedule.every().day.at("10:30").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
