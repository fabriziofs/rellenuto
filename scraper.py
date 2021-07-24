# Created by: Fabrizio Fasanando at 04-07-2020

import requests
import lxml.html as html
import os
import fnmatch

HOME_URL = 'https://animanga.es/ver-naruto-sin-relleno-ar-3508/'
SHIPPUDEN_TABLES = '//table[position() > 5]'
EPISODE_NUMBER = '//table[position() > 5]/tbody/tr[position() > 1]/td[1]/text()'
EPISODE_VALUE = '//table[position() > 5]/tbody/tr[position() > 1]/td[3]/text()'
SEASON_TITLE = '//h3[@id = contains(.,"Naruto Shippuden")]'

PATH = '/home/fabrizio/MEGA/Naruto Shippuden/'


def check_episodes(episodes):
    """Check from a list of integers if there are all the episodes."""
    not_listed = []
    try:
        for episode in episodes:
            if int(episode) not in range(1, 501):
                not_listed.append(episode)
        if not_listed:
            raise ValueError(f'There are episodes not listed: {not_listed}')
        else:
            print('All episodes are listed.')
    except ValueError as ve:
        print(ve)


def check_response(link):
    '''Check the response of a GET request.'''
    try:
        response = requests.get(link)
        if response.status_code == 200:
            no_parsed = response.content.decode('utf-8')
            parsed = html.fromstring(no_parsed)
            return parsed
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def get_episodes_number():
    parsed = check_response(HOME_URL)

    episodes_numbers = parsed.xpath(EPISODE_NUMBER)
    check_episodes(episodes_numbers)
    return episodes_numbers


def get_episodes_types():
    parsed = check_response(HOME_URL)

    episodes_types = parsed.xpath(EPISODE_VALUE)
    return episodes_types


def merge_episodes_data(numbers, types):
    ''' Mix the number with the type of an episode. Return a list of tuples with this form:
    (num,type)'''
    merged_list = list(zip(numbers, types))
    return merged_list


def change_episode_name(merged_list):
    '''Change the episode name if that episode is not a main episode.'''
    with os.scandir(PATH) as episodes:
        for episode in episodes:
            if ('Historia' in episode.name) or ('Relleno' in episode.name):
                print(f'{episode.name} already categorized')
                continue
            elif fnmatch.fnmatch(episode.name, '*-*'):
                # Split th episodes numbers when an episode have 1 caps in one.
                episode_n2 = episode.name[9:-4].replace('0', '')
                for episode_info_number, episode_info_type in merged_list:
                    if episode_n2 == episode_info_number:
                        new_name = f'{PATH}{episode.name[:-4]}({episode_info_type[:-1]}).mp4'
                        os.rename(episode.path, new_name)
            else:
                episode_n = episode.name[3:6].replace('0', '')
                for episode_info_number, episode_info_type in merged_list:
                    if episode_n == episode_info_number:
                        new_name = f'{PATH}{episode.name[:-4]}({episode_info_type[:-1]}).mp4'
                        os.rename(episode.path, new_name)


def run():
    numbers = get_episodes_number()
    types = get_episodes_types()
    merged_list = merge_episodes_data(numbers, types)
    change_episode_name(merged_list)


if __name__ == '__main__':
    run()
