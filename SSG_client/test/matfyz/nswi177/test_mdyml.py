#!/usr/bin/env python3
# pylint: disable=missing-docstring

from nose.tools import eq_

from matfyz.nswi177.mdyml import load_markdown_with_yaml_header


def test_empty_header():
    (header, content) = load_markdown_with_yaml_header([
        '---',
        '---',
        'This is content.',
    ])
    eq_(header, {})
    eq_(content, 'This is content.')


def test_missing_header():
    (header, content) = load_markdown_with_yaml_header([
        'This is content.',
    ])
    eq_(header, {})
    eq_(content, 'This is content.')


def test_normal_input():
    (header, content) = load_markdown_with_yaml_header([
        '---',
        'title: My title',
        '---',
        'This is content.',
    ])
    eq_(header, {
        'title': 'My title',
    })
    eq_(content, 'This is content.')
