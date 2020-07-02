#!/usr/bin/env python3

"""
my_owm - Open weather map wrapper for
the NSWI177 course at MFF CUNI.
"""

import sys
import argparse
from user import handler
from owm import cities

def main():
    """
    Entry point of the whole program.

    Only parses command-line arguments and executes the right callback.
    """

    args = argparse.ArgumentParser(description='OWM')
    args_sub = args.add_subparsers(help='Select what to do')
    args.set_defaults(action='help')
    args_help = args_sub.add_parser('help', help='Show this help.')
    args_help.set_defaults(action='help')

    args_register = args_sub.add_parser(
        'register',
        help='Register your API key'
    )

    args_register.set_defaults(action='register')
    args_register.add_argument(
        dest='api_key',
        help='Your API key to OWM'
    )

    args_search = args_sub.add_parser(
        'search',
        help='Search for a city'
    )

    args_search.set_defaults(action='search')
    args_search.add_argument(
        dest='city_name',
        help='City you want to search for'
    )

    args_add = args_sub.add_parser(
        'add',
        help='Add a city by its ID to your benchmarked cities'
    )
    args_add.set_defaults(action='add')
    args_add.add_argument(
        dest='city_id',
        help='City\'s ID'
    )

    args_rm = args_sub.add_parser(
        'rm',
        help='Remove a city from your benchmarked cities'
    )
    args_rm.set_defaults(action='rm')
    args_rm.add_argument(
        dest='city_id',
        help='Remove a city by its ID from your benchmarked cities'
    )

    args_list = args_sub.add_parser(
        'list',
        help='List all benchmarked cities and the weather there'
    )
    args_list.set_defaults(action='list')

    if len(sys.argv) == 1:
        cities.print_cities_weather()
    else:
        config = args.parse_args()
        if config.action == 'help':
            args.print_help()
        elif config.action == 'register':
            handler.register_key(config.api_key)
        elif config.action == 'search':
            cities.search(config.city_name)
        elif config.action == 'add':
            handler.add_benchmarked_city(config.city_id)
        elif config.action == 'rm':
            handler.remove_benchmarked_city(config.city_id)
        elif config.action == 'list':
            cities.list_all_cities()
        else:
            raise Exception("Unknown action")

if __name__ == '__main__':
    main()
