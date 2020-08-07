from nba.games import find_matchups_and_save
from datetime import datetime
from nba.utils import get_games_str, get_games_str_sns
from nba.links import generate_html_and_write_file, print_links, find_mapped_links, \
    build_dynamic_html_with_scores_and_write_file, find_and_save_direct_links
from nba.twilio import send_sms, send_alert
from nba.scores import find_box_scores_and_return_matchups, all_final
from nba.static import find_static_matchups
import schedule
import time
import logging
import time
import os
import threading


def daily_job():
    try:
        start = time.time()  # start timer
        today = datetime.today()
        logging.info('running find_matchups for {}'.format(today.strftime('%Y-%m-%d')))
        games = find_matchups_and_save(today)  # get matchups and write to local file
        games_str_sns = get_games_str_sns(games, today)  # get summary of matchups
        logging.info(games_str_sns)
        send_sms(games_str_sns)  # send summary to phone numbers
        link_map = find_mapped_links(today, games)  # get links for games
        find_and_save_direct_links(today)
        generate_html_and_write_file(link_map)  # update static s3 site with links
        logging.info('updating index.html at {}'.format(datetime.now()))
        os.system('./copy_index.sh')
        print_links(link_map)
        end = time.time()  # stop timer
        logging.info('SUCCESSFUL RUN FOR {} - Executed in {}'.format(today.strftime('%Y-%m-%d'), end - start))
    except Exception as e:
        logging.error(e)
        send_alert('Failure in daily script.')


def find_direct_links_and_save():
    logging.info('Running Link finder')
    links_start = time.time()  # start timer
    today = datetime.today()
    find_and_save_direct_links(today)
    links_stop = time.time()
    logging.info(
        'SUCCESSFUL LINKS RUN FOR {} - Executed in {}'.format(today.strftime('%Y-%m-%d'), links_stop - links_start))


def find_scores_and_write_to_ec2():
    today = datetime.today()
    while 1:
        matchups = find_box_scores_and_return_matchups(today)
        link_map = find_mapped_links(today, matchups)
        build_dynamic_html_with_scores_and_write_file(link_map)
        os.system('./copy_index.sh')
        logging.info('updating index.html at {}'.format(datetime.now()))
        if all_final(matchups):
            break
        time.sleep(60)
        # break
    logging.info('All matchups final. Stopped running jobs to get scores')


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def main():
    logging.basicConfig(filename='cron.log', level=logging.INFO)
    logging.info('--------- STARTING UP SCRIPT ---------------')
    # daily_job()
    # find_direct_links_and_save()
    # find_scores_and_write_to_ec2()
    schedule.every().day.at("10:30").do(run_threaded, daily_job)
    schedule.every().day.at("12:45").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("13:00").do(run_threaded, find_scores_and_write_to_ec2)
    schedule.every().day.at("13:15").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("13:45").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("14:15").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("14:45").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("15:15").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("15:45").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("16:15").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("16:45").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("17:15").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("17:45").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("18:15").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("18:45").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("19:15").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("19:45").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("20:15").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("20:45").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("21:15").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("21:45").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("22:15").do(run_threaded, find_direct_links_and_save)
    schedule.every().day.at("22:45").do(run_threaded, find_direct_links_and_save)
    while True:
        schedule.run_pending()
        time.sleep(1)
#
#
# if __name__ == '__main__':
#     main()
