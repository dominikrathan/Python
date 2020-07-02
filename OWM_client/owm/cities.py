#!/usr/bin/env python3

"""
Methods dealing with requests to OWM and cities file
"""

import gzip
import os
import json
import sys
import requests

CACHE_BASE = os.path.expanduser("~/.cache/my_owm/")
CACHE_USER_JSON = os.path.join(CACHE_BASE, 'user.json')
CACHE_CITY_LIST_JSON = os.path.join(CACHE_BASE, "cities.json")

def request_not_ok():
    """
    Notifies that the request was not succesful
    """
    print('The HTTP request to OWM was not succesful')
    print('Please check your internet connection and ensure the registered API key is valid')
    sys.exit(1)

def get_full_forecast(city_id):
    """
    Gets a weather forecast for the city with given id as a JSON string.
    """
    api_key = get_api_key()

    full_forecast_request = requests.get("""
    https://api.openweathermap.org/data/2.5/forecast?id={id}&appid={key}""".format(
        id=city_id,
        key=api_key
    ))

    if not full_forecast_request.ok:
        request_not_ok()

    return full_forecast_request.json()

def get_three_day_forecast(full_forecast):
    """
    Gets a dictionary with the city and a three-day forecast from a full forecast.
    {'city' : city_name, 'list' : list_of_weather_forecast}
    """
    days_at_twelve = 3
    take_first = False
    forecast = {'list':[]}

    city = full_forecast['city']['name']
    forecast['city'] = city

    meta = full_forecast['list'][0]['dt_txt'].split()
    time = meta[1]
    hours_now = int(time[:2])
    if hours_now > 12:
        days_at_twelve = days_at_twelve - 1
        take_first = True

    if take_first:
        forecast['list'].append(full_forecast['list'][0])

    for forec in full_forecast['list']:
        if '12:00:00' in forec['dt_txt']:
            forecast['list'].append(forec)
            days_at_twelve = days_at_twelve - 1
            if days_at_twelve == 0:
                break

    return forecast

def format_forecast(three_day_forecast):
    """
    Gets a formatted forecast as a list.
    """
    f_forecast = []

    first = three_day_forecast['list'][0]
    f_first = '{city}: {desc}, {temp}°C'.format(
        city=three_day_forecast['city'],
        desc=first['weather'][0]['description'],
        temp=round(first['main']['temp']-273.15)
    )
    f_forecast.append(f_first)

    for i in range(1, 3):
        forec = three_day_forecast['list'][i]
        meta = forec['dt_txt'].split()
        f_forec = ' {date}: {desc}, {temp}°C'.format(
            date=meta[0],
            desc=forec['weather'][0]['description'],
            temp=round(forec['main']['temp']-273.15)
        )
        f_forecast.append(f_forec)

    return f_forecast

def print_format_forecast(f_forecast):
    """
    Prints a formatted forecast line by line.
    """
    for f_forec in f_forecast:
        print(f_forec)

def print_cities_weather():
    """
    Prints a formatted forecast line by line for every city in cache.
    Printing new line between every two consecutive cities' forecasts.
    """
    try:
        with open(CACHE_USER_JSON, 'r') as user_file:
            user = json.loads(user_file.read())
    except FileNotFoundError:
        print('Add benchmarked cities to show weather.')
        print('See help option.')
        return

    if not 'benchmarked_cities' in user:
        print('Add some benchmarked cities first before calling the forecast.')
        return

    if len(user['benchmarked_cities']) == 0:
        message = """The list of benchmarked cities is empty.
Add some first before calling the forecast."""
        print(message)
        return

    for city_id in user['benchmarked_cities']:
        full = get_full_forecast(city_id)
        three_day = get_three_day_forecast(full)
        formatted = format_forecast(three_day)
        print_format_forecast(formatted)
        # Printing an extra new line after every city except the last one:
        if city_id != user['benchmarked_cities'][-1]:
            print()

def format_city(city_file):
    """
    Formats the city information for a given JSON city description.

    The format is as follows: ID COUNTRY NAME
    """
    try:
        return '{id} {country} {name}'.format(
            id=city_file['id'],
            country=city_file['country'],
            name=city_file['name']
        ) + '\n'
    except UnicodeEncodeError:
        pass

def format_cities(cities_file):
    """
    Formats cities in a given JSON file list.
    """
    for city_file in cities_file['list']:
        formatted_city = format_city(city_file)
        print(formatted_city)

def get_api_key():
    """
    Gets the user's API key located in the user json file.
    """
    with open(CACHE_USER_JSON, 'r') as user_file:
        user = json.loads(user_file.read())
        if not 'api_key' in user:
            print('No API key registered yet, see -h for help')
            sys.exit(1)
        return user['api_key']

def get_city_list():
    """
    Gets the city list.
    Downloads the list if not present yet.
    """
    try:
        with open(CACHE_CITY_LIST_JSON, 'r') as cities:
            return cities.read()
    except FileNotFoundError:
        result = requests.get('http://bulk.openweathermap.org/sample/city.list.json.gz')
        if not result.ok:
            request_not_ok()
        content = gzip.decompress(result.content).decode('utf-8')
        with open(CACHE_CITY_LIST_JSON, 'w') as cities:
            cities.write(content)
        return content

def get_search_result_by_name(city_name):
    """
    Get result of search action by city name
    """
    city_list = get_city_list()
    result = ''
    cities = json.loads(city_list)
    for city in cities:
        if city_name.lower() in city['name'].lower():
            result += format_city(city)
    return result

def get_search_result_by_id(city_id):
    """
    Get result of search action by city id
    """
    city_list = get_city_list()
    cities = json.loads(city_list)
    for city in cities:
        if int(city_id) == (city['id']):
            return format_city(city)

    errmess = 'A logical error. The test for validity of city ID being added must have gone wrong.'
    raise Exception(errmess)
# handler.remove_benchmarked_city(city_id)
# return 'This is not a valid city ID: ' + city_id + '\nIt was removed from benchmarked cities\n'

def search(city_name):
    """
    Prints all of the cities whose name contains the given string.
    """
    print(get_search_result_by_name(city_name), end='')

def list_all_cities():
    """
    List all of the benchmarked cities.
    """
    if not os.path.exists(CACHE_USER_JSON):
        print('No API key registered yet')
        print('See help option.')
        return
    with open(CACHE_USER_JSON, 'r') as user_file:
        user = json.loads(user_file.read())

    if not 'benchmarked_cities' in user:
        print('No benchmarked city yet')
        return

    if len(user['benchmarked_cities']) == 0:
        print('No benchmarked city in cache')
        return

    for city_id in user['benchmarked_cities']:
        city = get_search_result_by_id(city_id)
        print(city, end='')
