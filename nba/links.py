from datetime import datetime
from nba.aws import write_html, invoke_lambda_with_payload
from nba.static import find_links
import logging
from nba.utils import write_html_file, write_file, read_file

index_file = """<html xmlns="http://www.w3.org/1999/xhtml" >
<head>
    <title>NBA Links</title>
</head>
<body>
  <h1>NBA Games For {}</h1>
  {}
</body>
</html>"""


def find_mapped_links(date, games):
    links = find_links(date)  # find links (invoke scraper or find in local)
    link_map = map_links(games, links)  # map links to list of matchups
    return link_map


def find_all_direct_links(direct_links, links):
    if len(direct_links) == 0:
        for link in links:
            direct_links[link] = find_direct_links(link)
    else:
        for link in direct_links:
            if len(direct_links[link]) == 0:
                direct_links[link] = find_direct_links(link)
    return direct_links


def find_direct_links(link):
    return invoke_lambda_with_payload('nbabite-direct-link-finder', {'link': link})['links']


def find_and_save_direct_links(date):
    local_direct_links = read_file('nba/data/DirectLinks.json')
    direct_links = {}
    if date.strftime('%m/%d/%Y') in local_direct_links:
        direct_links = local_direct_links[date.strftime('%m/%d/%Y')]
    direct_links = find_all_direct_links(direct_links, find_links(date))
    local_direct_links[date.strftime('%m/%d/%Y')] = direct_links
    write_file('nba/data/DirectLinks.json', local_direct_links)


def find_saved_direct_links():
    today = datetime.today()
    return read_file('nba/data/DirectLinks.json')[today.strftime('%m/%d/%Y')]


def map_links(matchups, links):
    link_map = {}
    for matchup in matchups:
        for link in links:
            link_parts = link.split('/')
            link_name = link_parts[4]
            if matchup['teams'][0]['name'].lower() in link_name or matchup['teams'][1]['name'].lower() in link_name:
                link_map[link] = matchup
    return link_map


def generate_html_and_write_file(link_map):
    today = datetime.today()
    header = 'NBA Games for {}, {} {} {}'.format(today.strftime('%A'),
                                                 today.strftime("%B"), today.day,
                                                 today.year)
    index_file_str = index_file.format(header, build_links(link_map, find_saved_direct_links()))
    write_html_file('index.html', index_file_str)


def build_dynamic_html_with_scores_and_write_file(link_map):
    today = datetime.today()
    header = 'NBA Games for {}, {} {} {}'.format(today.strftime('%A'),
                                                 today.strftime("%B"), today.day,
                                                 today.year)

    index_file_str = index_file.format(header, build_links_with_scores(link_map, find_saved_direct_links()))
    write_html_file('index.html', index_file_str)


def build_direct_links(direct_links):
    all_tags = ''
    i = 1
    for stream_link in direct_links:
        tag = '<a href="{}" target="_blank">{}</a>&nbsp'.format(stream_link, i)
        all_tags += tag
        i += 1
    return all_tags


def build_links(link_map, direct_links):
    all_links = ''
    for link in link_map:
        link_str = 'href="{}"'.format(link)
        link_time = link_map[link]['time']
        link_header = '{} vs {}'.format(link_map[link]['teams'][0]['name'], link_map[link]['teams'][1]['name'])
        if link_map[link]['tv']['scope'] == 'National':
            link_tag = '<p>{} - {} - {} - Also on {}</p><br>\n'.format(link_time, link_header,
                                                                       build_direct_links(direct_links[link]),
                                                                       link_map[link]['tv'][
                                                                           'network'])
        else:
            link_tag = '<p>{} - {} - {}</p><br>\n'.format(link_time, link_header,
                                                          build_direct_links(direct_links[link]))
        all_links += link_tag
    return all_links


def build_links_with_scores(link_map, direct_links):
    all_links = ''
    for link in link_map:
        link_url = 'href="{}"'.format(link)
        if len(link_map[link]['boxscore']) > 0:
            if link_map[link]['boxscore']['status'] == 'Final':
                link_tag = build_final_score_tag(link_map[link])
            else:
                link_tag = build_in_progress_score_tag(link_map[link], direct_links[link])
        else:
            link_time = link_map[link]['time']
            link_header = '{} vs {}'.format(link_map[link]['teams'][0]['name'], link_map[link]['teams'][1]['name'])
            if link_map[link]['tv']['scope'] == 'National':
                link_tag = '<p>{} - {} - {} - Also on {}</p><br>\n'.format(link_time, link_header,
                                                                           build_direct_links(direct_links[link]),
                                                                           link_map[link]['tv'][
                                                                               'network'])
            else:
                link_tag = '<p>{} - {} - {}</p><br>\n'.format(link_time, link_header,
                                                              build_direct_links(direct_links[link]))
        all_links += link_tag
    all_links += '<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><small>Last updated at: {}</small>'.format(
        datetime.today())
    return all_links


def build_final_score_tag(matchup):
    score1 = {'name': matchup['teams'][0]['name'], 'score': matchup['boxscore']['teams'][matchup['teams'][0]['id']]}
    score2 = {'name': matchup['teams'][1]['name'], 'score': matchup['boxscore']['teams'][matchup['teams'][1]['id']]}
    return '<p>{} - {} - Final - {} vs. {}</p><br>\n'.format(score1['score'], score2['score'], score1['name'],
                                                             score2['name'])


def build_in_progress_score_tag(matchup, direct_links):
    score1 = {'name': matchup['teams'][0]['name'], 'score': matchup['boxscore']['teams'][matchup['teams'][0]['id']]}
    score2 = {'name': matchup['teams'][1]['name'], 'score': matchup['boxscore']['teams'][matchup['teams'][1]['id']]}
    if matchup['tv']['scope'] == 'National':
        link_tag = '<p>{} - {} - {} - {} vs. {} - {} - Also on {}</p><br>\n'.format(
            score1['score'], score2['score'], find_game_progress(matchup['boxscore']), score1['name'], score2['name'],
            build_direct_links(direct_links),
            matchup['tv']['network'])
    else:
        link_tag = '<p>{} - {} - {} - {} vs. {} - {} </p><br>\n'.format(score1['score'],
                                                                        score2['score'],
                                                                        find_game_progress(matchup['boxscore']),
                                                                        score1['name'],
                                                                        score2['name'],
                                                                        build_direct_links(direct_links))
    return link_tag


def find_game_progress(score):
    if score['status'] == 'Halftime':
        return 'Halftime'
    else:
        return score['time'] + ' ' + str(score['period']) + 'Q'


def print_links(link_map):
    for link in link_map:
        logging.info(
            '{} vs. {} - {} - {}'.format(link_map[link]['teams'][0]['name'], link_map[link]['teams'][1]['name'],
                                         link_map[link]['time'], link))
