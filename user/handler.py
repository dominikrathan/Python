#!/usr/bin/env python3

"""
Methods dealing with the user cache file, which contains the current user's
API key and his benchmarked cities.
"""

import os
import sys
import json
from owm import cities

CACHE_BASE = os.path.expanduser("~/.cache/my_owm/")
CACHE_USER_JSON = os.path.join(CACHE_BASE, 'user.json')

def register_key(api_key):
    """
    Save the given key in the user cache file.
    """
    if not os.path.exists(CACHE_USER_JSON):
        if not os.path.exists(CACHE_BASE):
            os.mkdir(CACHE_BASE)
    user = {
        'api_key': api_key
    }
    user_json = json.dumps(user)
    with open(CACHE_USER_JSON, 'w') as user_file:
        user_file.write(user_json + '\n')

def add_benchmarked_city(city_id):
    """
    Add the given city ID to current user's benchmarked cities.
    """
    if not os.path.exists(CACHE_USER_JSON):
        print('No API key registered yet')
        sys.exit(1)
    with open(CACHE_USER_JSON, 'r') as user_file:
        user_cache_content = user_file.read()

    if not user_cache_content:
        print('No API key registered yet')
        sys.exit(1)
    user = json.loads(user_cache_content)

    try:
        city_id_int = int(city_id)
    except ValueError:
        print("""City ID has to be an integer
No city ID added to cache""")
        sys.exit(2)

    if not 'benchmarked_cities' in user:
        user['benchmarked_cities'] = []

    if city_id in user['benchmarked_cities']:
        print('The city with ID ' + city_id + ' is already in cache')
        sys.exit(3)

    found = False
    city_list = cities.get_city_list()
    cities_dict = json.loads(city_list)
    for city in cities_dict:
        if city_id_int == (city['id']):
            found = True
            user['benchmarked_cities'].append(city_id)
            break

    if found:
        user_json = json.dumps(user)
        with open(CACHE_USER_JSON, 'w') as user_file:
            user_file.write(user_json + '\n')
    else:
        print('This is not a valid city ID: ' + city_id)
        print('No city ID added to cache')
        sys.exit(3)

def remove_benchmarked_city(city_id):
    """
    Remove the given city ID from current user's benchmarked cities.
    """
    if not os.path.exists(CACHE_USER_JSON):
        raise Exception('No API key yet registered')
    with open(CACHE_USER_JSON, 'r') as user_file:
        user = json.loads(user_file.read())

    if not 'benchmarked_cities' in user:
        print('No benchmarked city yet')
        sys.exit(3)

    if not city_id in user['benchmarked_cities']:
        print('No benchmarked city with this ID')
        sys.exit(3)

    user['benchmarked_cities'].remove(city_id)

    user_json = json.dumps(user)
    with open(CACHE_USER_JSON, 'w') as user_file:
        user_file.write(user_json + '\n')
