import requests
import lxml.html as html
import logging
import datetime
import json
import csv

player_goals_link = ''
player_name = ''
match_days = ''
goals_per_match = ''
top_scorers = []
global_player = ''
fields = ('name', 'J-1', 'J-2', 'J-3', 'J-4', 'J-5', 'J-6', 'J-7', 'J-8',
          'J-9', 'J-10', 'J-11', 'J-12', 'J-13', 'J-14', 'J-15', 'J-16', 'J-17')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_url():
    global player_goals_link, player_name, match_days, goals_per_match

    with open('config.json', 'r') as file:
        config = json.load(file)
        player_goals_link = config['player_goals_link']
        player_name = config['player_name']
        match_days = config['match_days']
        goals_per_match = config['goals_per_match']

        return config['home_url']


def make_petition(url):
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError(f'Server status code: {response.status_code}')

    html_home = response.content.decode('utf-8')
    return html.fromstring(html_home)


def parse_home():
    global global_player
    try:
        logging.info('Initializing download.')
        url = get_url()

        logging.info('Getting data.')
        html_var = make_petition(url)

        logging.info('Parsing data.')
        list_players = list(html_var.xpath(player_goals_link))

        # parse_goals_per_player(f'https://ligamx.net{list_players[0]}')
        for player in list_players:
            row = parse_goals_per_player(f'https://ligamx.net{player}')
            row.insert(0, global_player)
            top_scorers.append(row)

        save_csv()
        logging.info(f'Download process has finished.')
    except ValueError as ve:
        print(ve)


def parse_goals_per_player(url):
    global global_player
    html_var = make_petition(url)

    global_player = html_var.xpath(player_name)[0]

    logging.info(f'Getting details from {global_player}.')

    match_day = html_var.xpath(match_days)

    goals = html_var.xpath(goals_per_match)

    result = list(zip(match_day, goals))

    return sort_goles(result)


# fill match days with 0 goles
def sort_goles(list):
    match_days_list = ('J-1', 'J-2', 'J-3', 'J-4', 'J-5', 'J-6', 'J-7', 'J-8',
                       'J-9', 'J-10', 'J-11', 'J-12', 'J-13', 'J-14', 'J-15', 'J-16', 'J-17')
    new_list = []

    logging.info(f'Sorting details from {global_player}')

    for match_day in match_days_list:

        for nested in list:
            if(match_day in nested):
                new_list.append(int(nested[1]))
                list.pop(0)  # delete current element(first element)
            else:
                new_list.append(0)
            break  # skip iteration to just search in the first element

    return new_list


def save_csv():
    logging.info(f'Saving data into top_scorers.csv')
    with open('top_scorers.csv', 'w', newline='', encoding='utf-8') as f:
        write = csv.writer(f)

        write.writerow(fields)
        write.writerows(top_scorers)


def run():
    parse_home()


if __name__ == '__main__':
    run()
