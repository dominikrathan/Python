#!/usr/bin/env python
# pylint: disable=missing-docstring

from nose.tools import eq_
from owm import cities

def test_search_for_city_by_name():
    actual = cities.get_search_result_by_name('prague')
    with open('tests/owm/expected_prague', 'r') as expected_file:
        expected = expected_file.read()
    eq_(actual, expected)

def test_search_for_city_by_id():
    actual = cities.get_search_result_by_id('3067696')
    expected = '3067696 CZ Prague\n'
    eq_(actual, expected)
