#!/usr/bin/env python
# pylint: disable=missing-docstring

from nose.tools import eq_
from owm import cities
import json

def test_format_forecast():
    with open('tests/owm/testing_moscow_weather_input', 'r') as artificial_response_file:
        full_forecast_json = artificial_response_file.read()
    full_forecast = json.loads(full_forecast_json)
    three_day = cities.get_three_day_forecast(full_forecast)
    formatted = cities.format_forecast(three_day)
    actual = ''
    for line in formatted:
        actual += line
        if line != formatted[-1]:
            actual += '\n'
    with open('tests/owm/expected_moscow_weather_output', 'r') as expected_file:
        expected = expected_file.read()
    eq_(actual, expected)
